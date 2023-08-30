from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from gestione.models import *
from django.db.models import Q
from .forms import NewUserForm
from django.contrib.auth import login, authenticate
from django.contrib.auth import views as auth_views
from django.contrib import messages
from django.views import View
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from .rec_sys import recommend_mezzi
from django.views.generic.edit import CreateView

def get_mezzi():
    imm_mezzi = ImmaginiMacchina.objects.all()
    info_mezzi = Mezzo.objects.all()
    zipped_mezzi = zip(imm_mezzi, info_mezzi)
    return  zipped_mezzi

def get_accessori():
    imm_acc = ImmaginiAccessorio.objects.all()
    info_acc = Accessorio.objects.all()
    zipped_acc = zip(imm_acc, info_acc)
    return zipped_acc

def home_page(request):
    zipped_mezzi = get_mezzi()
    zipped_acc = get_accessori()

    marche = Mezzo.objects.values_list('marca', flat=True).distinct()

    ctx={"marche": marche,
        "zipped_mezzi": zipped_mezzi,
        "zipped_acc": zipped_acc,
    }
    storage = messages.get_messages(request)
    storage.used = True
    return render(request, template_name="home.html", context=ctx)

def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registrazione avvenuta con successo" )
			return redirect("/home")
		messages.error(request, "Registrazione fallita, errore nel compilare il form")
	form = NewUserForm()
	return render (request=request, template_name="register.html", context={"register_form":form})

class CustomLoginView(View):
    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            try:
                venditore = Venditore.objects.get(venditore=user)
                return redirect('gestione:dashboard')
            except:                
                return redirect( reverse('authHome_page'))
        else:
            login_url = reverse('home')
            messages.error(request, 'Credenziali login non valide')

        return redirect(login_url)

class CustomLogoutView(auth_views.LogoutView):
    next_page = reverse_lazy('home')

    def dispatch(self, request, *args, **kwargs):
        messages.success(request, 'Logout eseguito con successo')
        return super().dispatch(request, *args, **kwargs)


@login_required      
def authHome_page(request):
    info_mezzo = recommend_mezzi(request.user)
    imm_ord = []
    for i in info_mezzo:
        print(ImmaginiMacchina.objects.filter(car_id = i.id)[0].fronte.url)
        imm_ord.append(ImmaginiMacchina.objects.filter(car_id = i.id)[0])

    zipped_mezzi = zip(imm_ord, info_mezzo)

    zipped_acc = get_accessori()
    marche = Mezzo.objects.values_list('marca', flat=True).distinct()

    ctx={
        "marche": marche,
        "zipped_mezzi": zipped_mezzi,
        "zipped_acc": zipped_acc,
        "req": request,
    }
    return render(request, 'authHome.html', ctx)

def get_filtered_mezzi(request):
    filtri = {key: value for key, value in request.GET.items()}
    #/Q è usato per fare un filtro di ricerca complesso
    ric_com = Q()

    #FILTRO MARCHE
    marche_sel = filtri["marca"].split(',')
    ric_com &= Q(marca__in=marche_sel)

    #FILTRO MOTO/MACCHINA/TUTTO
    moto=None
    tipo_mezzo = filtri.pop('tipo_mezzo', None)
    if tipo_mezzo == "moto":
        moto=True
    elif tipo_mezzo == "auto":
        moto=False

    if(moto != None):
        if(moto):
            ric_com &= Q(moto=True)
        else:
            ric_com &= Q(moto=False)

    #FILTRO USATO/NUOVO/TUTTO
    us=None
    new_used = filtri.pop('new_used', None)
    if new_used == "u":
        us=True
    elif new_used == "n":
        us=False

    if(us != None):
        if(us):
            ric_com &= Q(num_proprietari__gte=1)
        else:
            ric_com &= Q(num_proprietari=0)

    
    #FILTRO SUL COSTO
    min=filtri["mezzo-prezzomin"]
    if(min != ''):
        ric_com &= Q(prezzo__gte=int(min))
        

    max=filtri["mezzo-prezzomax"]
    if(max != ''):
        max=int(max)
        if(max > 1000):
            ric_com &= Q(prezzo__lte=max)

    #FILTRO SUI KM
    if("kmmin" in filtri.keys()):
        kmin = filtri["kmmin"]
        if(kmin != ''):
            ric_com &= Q(kilometraggio__gte=int(kmin))

        
        kmax=filtri["kmmax"]
        if(kmax != ''):
            kmax=int(kmax)
            if(kmax > 1000):
                ric_com &= Q(kilometraggio__lte=kmax)

    #FILTRO SULLA DATA
    if("date" in filtri.keys()):
        date = filtri["date"]
        if(date != ''):
            ric_com &= Q(data_fabbricazione__gt=date)

    queryset = Mezzo.objects.filter(ric_com)
    id_sel = []
    for i in queryset:
        id_sel.append(i.id)

    imm_query = ImmaginiMacchina.objects.filter(car_id__in=id_sel)
    zipped_mezzi = zip(imm_query, queryset)

    if(len(queryset) == 0):
        return JsonResponse({'result_html': ''})

    result_html = render_to_string('filteredMezzi.html', {'queryset': zipped_mezzi})
    return JsonResponse({'result_html': result_html})

def get_filtered_acc(request):
    filtri = {key: value for key, value in request.GET.items()}
    #/Q è usato per fare un filtro di ricerca complesso
    ric_com = Q()

    #FILTRO MOTO/MACCHINA/TUTTO
    moto=None
    tipo_acc = filtri.pop('tipo_acc', None)
    if tipo_acc == "moto":
        moto=True
    elif tipo_acc == "auto":
        moto=False

    if(moto != None):
        if(moto):
            ric_com &= Q(per_moto=True)
        else:
            ric_com &= Q(per_moto=False)

    #FILTRO SUL COSTO
    min=filtri["acc-prezzomin"]
    if(min != ''):
        ric_com &= Q(prezzo__gte=int(min))

    max=filtri["acc-prezzomax"]
    if(max != ''):
        max=float(max)
        if(max > 1.0):
            ric_com &= Q(prezzo__lte=max)

    queryset = Accessorio.objects.filter(ric_com)
    id_sel = []
    for i in queryset:
        id_sel.append(i.id)
    
    imm_query = ImmaginiAccessorio.objects.filter(acc_id__in=id_sel)
    zipped_acc = zip(imm_query, queryset)

    if(len(queryset) == 0):
        return JsonResponse({'result_html': ''})

    result_html = render_to_string('filteredAcc.html', {'queryset': zipped_acc})
    return JsonResponse({'result_html': result_html})


@login_required
def add_to_favorites(request, object_type, object_id):
    user = request.user
    try:
        if object_type == "mezzo":
            mezzo = Mezzo.objects.get(id=object_id)
            FavouriteMezzo.objects.get_or_create(user=user, mezzo=mezzo)
        elif object_type == "accessorio":
            accessorio = Accessorio.objects.get(id=object_id)
            FavouriteAccessorio.objects.get_or_create(user=user, acc=accessorio)
        return JsonResponse({"message": "Prodotto aggiunto alla tua lista dei preferiti!"})
    except (Mezzo.DoesNotExist, Accessorio.DoesNotExist):
        return JsonResponse({"message": "Object not found"}, status=404)
    
@login_required
def remove_from_favorites(request, object_type, object_id):
    user = request.user
    try:
        if object_type == "mezzo":
            mezzo = Mezzo.objects.get(id=object_id)
            FavouriteMezzo.objects.filter(user=user, mezzo=mezzo).delete()
        elif object_type == "accessorio":
            accessorio = Accessorio.objects.get(id=object_id)
            FavouriteAccessorio.objects.filter(user=user, acc=accessorio).delete()
        return JsonResponse({"message": "Prodotto rimosso dalla tua lista dei preferiti!"})
    except (Mezzo.DoesNotExist, Accessorio.DoesNotExist):
        return JsonResponse({"message": "Object not found"}, status=404)
    
@login_required
def favorite_objects(request):
    user = request.user
    fav_mezz = FavouriteMezzo.objects.filter(user=user).select_related('mezzo')
    fav_acc = FavouriteAccessorio.objects.filter(user=user).select_related('acc')
    
    mezz_id_sel = []
    for i in fav_mezz:
        mezz_id_sel.append(i.mezzo.id)
    info_mezzi = Mezzo.objects.filter(id__in=mezz_id_sel)
    imm_query = ImmaginiMacchina.objects.filter(car_id__in=mezz_id_sel)
    zipped_mezzi = zip(imm_query, info_mezzi)

    acc_id_sel = []
    for i in fav_acc:
        acc_id_sel.append(i.id)
    
    info_acc = Accessorio.objects.filter(id__in=acc_id_sel)
    imm_query = ImmaginiAccessorio.objects.filter(acc_id__in=acc_id_sel)
    zipped_acc = zip(imm_query, info_acc)

    context = {
        'zipped_mezzi': zipped_mezzi,
        'zipped_acc': zipped_acc,
    }
    return render(request, 'favList.html', context)

@login_required
def add_to_cart(request, object_type, object_id):
    user_cart, created = Carrello.objects.get_or_create(user=request.user)
    succ=user_cart.add_to_cart(object_type, object_id)
    if(succ):
        return JsonResponse({"message": "Prodotto aggiunto al carrello!"})
    return JsonResponse({"message": "Errore nell'aggiunta al carrello!"})

@login_required
def remove_from_cart(request, object_type=None, object_id=None):
    user_cart, created = Carrello.objects.get_or_create(user=request.user)
    succ=user_cart.remove_from_cart(object_type, object_id)
    if(succ):
        return JsonResponse({"message": "Prodotto rimosso dal carrello!"})
    return JsonResponse({"message": "Errore nella rimozione dal carrello!"})

@login_required
def view_cart(request):
    try:
        cart = Carrello.objects.get(user=request.user)
    except Carrello.DoesNotExist:
        cart = None

    context = {
        'cart': cart,
    }
    return render(request, 'cart.html', context)

def mezzo_in_carr(user):
    try:
        carrello = Carrello.objects.get(user=user)
        return carrello.items.filter(mezzo__isnull=False).exists()
    except Carrello.DoesNotExist:
        return False

class SpedCreateView(CreateView):
    model = Spedizione
    template_name = "spedizione.html"
    fields = "__all__"
        
    def form_valid(self, form):
        response = super().form_valid(form)
        return redirect('authHome_page')

    def get_success_url(self):
        return reverse('authHome_page')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_id'] = self.request.user.id
        print(context["user_id"])
        context['poss_app'] = mezzo_in_carr(self.request.user.id)
        return context