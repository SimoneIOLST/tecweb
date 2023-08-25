from .models import Mezzo, ImmaginiMacchina, Accessorio, ImmaginiAccessorio, Venditore
from django.views.generic import DetailView, ListView, CreateView
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect


class MezzoListView(ListView):
    model = Mezzo
    template_name="gestione/listaMezzi.html"


class MezzoDetailView(DetailView):
    model = Mezzo
    template_name = 'gestione/dettagliMezzo.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['immagini_mezzo'] = ImmaginiMacchina.objects.filter(car_id=self.object.id)
        context['venditore'] = self.object.venditore
        return context
    
class AccListView(ListView):
    model = Accessorio
    template_name="gestione/listaAcc.html"


class AccDetailView(DetailView):
    model = Accessorio
    template_name = "gestione/dettagliAcc.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['immagini_acc'] = ImmaginiAccessorio.objects.filter(acc_id_id=self.object.id)
        context['venditore'] = self.object.venditore
        return context
    
class CreateMezzoView(CreateView):
    model = Mezzo
    template_name = "gestione/creaMezzo.html"
    model = Mezzo
    fields = "__all__"
        
    def form_valid(self, form):
        response = super().form_valid(form)
        return redirect(reverse_lazy('gestione:immmac-crea', kwargs={'car_id': self.object.pk}))

    def get_success_url(self):
        return reverse('gestione:mezzo-list')  # Redirect back to MezzoListView


class CreateImmaginiMacchinaView(CreateView):
    model = ImmaginiMacchina
    fields = "__all__" # Replace with the actual fields
    template_name = 'gestione/creaImmMacc.html'  # Replace with your template name
    
    def get_context_data(self, **kwargs):
            print("trig")
            context = super().get_context_data(**kwargs)
            context['car_id'] = self.kwargs['car_id']
            return context


    def form_valid(self, form):
            print("Fronte File:", self.request.FILES.get('fronte'))
            print("Interni File:", self.request.FILES.get('interni'))
            print("Retro File:", self.request.FILES.get('retro'))
            
            form.instance.car_id_id = self.kwargs['car_id']
            return super().form_valid(form)
        
    def get_success_url(self):
        return reverse('gestione:mezzo-list')  # Redirect back to MezzoCreateView