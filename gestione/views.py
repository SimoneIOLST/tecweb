from django.shortcuts import render
from .models import Mezzo, ImmaginiMacchina, Accessorio, ImmaginiAccessorio
from django.views.generic import DetailView, ListView


class MezzoListView(ListView):
    model = Mezzo
    template_name="gestione/listaMezzi.html"


class MezzoDetailView(DetailView):
    model = Mezzo
    template_name = 'gestione/dettagliMezzo.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['immagini_mezzo'] = ImmaginiMacchina.objects.filter(car_id=self.object.id)
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
        return context