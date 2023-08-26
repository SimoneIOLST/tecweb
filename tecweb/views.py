from django.http import JsonResponse
from django.shortcuts import render, redirect
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
    zipped_mezzi = get_mezzi()
    lista_fav = []

    zipped_acc = get_accessori()
    marche = Mezzo.objects.values_list('marca', flat=True).distinct()

    ctx={"marche": marche,
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

    if("kmin" in filtri.keys()):
        kmin = filtri["kmmin"]
        if(kmin != ''):
            ric_com &= Q(prezzo__gte=int(kmin))

        kmax=filtri["mezzo-prezzomax"]
        if(kmax != ''):
            kmax=int(kmax)
            if(kmax > 1000):
                ric_com &= Q(prezzo__lte=kmax)

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
