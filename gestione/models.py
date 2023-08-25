from django.db import models


from django.db import models
from django.db.models import Model
# Create your models here.

class Venditore(Model):
    cf = models.CharField(max_length=16, primary_key=True)
    iban = models.CharField(max_length=34)
    telefono = models.CharField(max_length=16)
    pec = models.CharField(max_length=40, null=True)
    mail = models.CharField(max_length=319)
    indirizzo = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "Venditori"

class Mezzo(Model):
    vin = models.CharField(max_length=17, unique=True)
    moto = models.BooleanField()
    marca = models.CharField(max_length=20)
    modello = models.CharField(max_length=35)
    prezzo = models.PositiveIntegerField()
    data_fabbricazione = models.DateField()
    kilometraggio = models.PositiveIntegerField()
    colore = models.CharField(max_length=15)
    num_proprietari = models.PositiveSmallIntegerField()
    venditore = models.ForeignKey(to=Venditore, on_delete=models.CASCADE, unique=False)

    class Meta:
        verbose_name_plural = "Mezzi"

class ImmaginiMacchina(Model):
    def uploadTo(istance, filename):
        return f"{istance.car_id.id}/{filename}"
    
    car_id = models.OneToOneField(to=Mezzo, on_delete=models.CASCADE, primary_key=True, unique=True)
    fronte = models.ImageField(upload_to = uploadTo)
    retro = models.ImageField(upload_to = uploadTo, null=True, blank=True)
    interni = models.ImageField(upload_to = uploadTo, null=True, blank=True)
    
    class Meta:
        verbose_name_plural = "Immagini Macchine"

class Accessorio(Model):
    per_moto = models.BooleanField()
    nome = models.CharField(max_length=20)
    descrizione = models.TextField(max_length=500)
    prezzo = models.FloatField()
    venditore = models.ForeignKey(to=Venditore, on_delete=models.CASCADE, unique=False)

    class Meta:
        verbose_name_plural = "Accessori"

class ImmaginiAccessorio(Model):
    def uploadTo(istance, filename):
        return f"accessori/{istance.acc_id.id}/{filename}"
    
    acc_id = models.OneToOneField(to=Accessorio, on_delete=models.CASCADE, primary_key=True, unique=True)
    foto1 = models.ImageField(upload_to = uploadTo)
    foto2 = models.ImageField(upload_to = uploadTo, null=True, blank=True)
    foto3 = models.ImageField(upload_to = uploadTo, null=True, blank=True)
    
    class Meta:
        verbose_name_plural = "Immagini Accessori"