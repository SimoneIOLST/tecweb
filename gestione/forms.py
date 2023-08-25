from django import forms
from .models import Mezzo

class MezzoForm(forms.ModelForm):
    class Meta:
        model = Mezzo
        fields = "__all__"  

    data_fabbricazione = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
