from .models import Mezzo, ImmaginiMacchina, Accessorio, ImmaginiAccessorio, Venditore
from django.views.generic import DetailView, ListView, CreateView
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
from .forms import MezzoForm

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
    form_class = MezzoForm
        
    def form_valid(self, form):
        response = super().form_valid(form)
        return redirect(reverse_lazy('gestione:IM-crea', kwargs={'car_id': self.object.pk}))

    def get_success_url(self):
        return reverse('gestione:mezzo-list')  


class CreateImmaginiMacchinaView(CreateView):
    model = ImmaginiMacchina
    fields = "__all__" 
    template_name = 'gestione/creaImmMacc.html' 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['car_id'] = self.kwargs['car_id']
        return context


    def form_valid(self, form):
        form.instance.car_id_id = self.kwargs['car_id']
        return super().form_valid(form)
        
    def get_success_url(self):
        return reverse('gestione:mezzo-list')
    
class CreateAccView(CreateView):
    model = Accessorio
    template_name = "gestione/creaAccessorio.html"
    fields = "__all__"
        
    def form_valid(self, form):
        response = super().form_valid(form)
        return redirect(reverse_lazy('gestione:IA-crea', kwargs={'acc_id': self.object.pk}))

    def get_success_url(self):
        return reverse('gestione:acc-list')  


class CreateImmaginiAccessorioView(CreateView):
    model = ImmaginiAccessorio
    fields = "__all__" 
    template_name = 'gestione/creaImmAcc.html' 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['acc_id'] = self.kwargs['acc_id']
        return context


    def form_valid(self, form):
        form.instance.acc_id_id = self.kwargs['acc_id']
        return super().form_valid(form)
        
    def get_success_url(self):
        return reverse('gestione:acc-list')