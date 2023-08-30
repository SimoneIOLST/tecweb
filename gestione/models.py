from django.db import models
from django.db.models import Model
from django.contrib.auth.models import User

class Venditore(Model):
    cf = models.CharField(max_length=16, primary_key=True)
    nome = models.CharField(max_length=50)
    iban = models.CharField(max_length=34)
    telefono = models.CharField(max_length=16)
    pec = models.CharField(max_length=40, null=True)
    mail = models.CharField(max_length=319)
    indirizzo = models.CharField(max_length=50)
    citta = models.CharField(max_length=50)
    provincia = models.CharField(max_length=50)
    venditore = models.ForeignKey(to=User, on_delete=models.CASCADE, unique=False)

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

class FavouriteMezzo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mezzo = models.ForeignKey(Mezzo, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'mezzo')
        verbose_name_plural = "Mezzi favoriti"

class FavouriteAccessorio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    acc = models.ForeignKey(Accessorio, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'acc')
        verbose_name_plural = "Accessori favoriti"

class OggettoCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mezzo = models.ForeignKey('Mezzo', on_delete=models.CASCADE, null=True)
    accessorio = models.ForeignKey('Accessorio', on_delete=models.CASCADE, null=True)

class Carrello(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(OggettoCart, related_name='cerrello')

    def add_to_cart(self, item_type, item_id):
        try:
            if item_type == 'mezzo':
                item = Mezzo.objects.get(pk=item_id)
                cart_item, created = OggettoCart.objects.get_or_create(user=self.user, mezzo=item)
            elif item_type == 'accessorio':
                item = Accessorio.objects.get(pk=item_id)
                cart_item, created = OggettoCart.objects.get_or_create(user=self.user, accessorio=item)
            
            self.items.add(cart_item)
            
            return True
        except (Mezzo.DoesNotExist, Accessorio.DoesNotExist):
            return False

    def remove_from_cart(self, item_type=None, item_id=None):
        try:
            if item_type == 'mezzo':
                item = Mezzo.objects.get(pk=item_id)
                cart_item = OggettoCart.objects.filter(user=self.user, mezzo=item).first()
            elif item_type == 'accessorio':
                item = Accessorio.objects.get(pk=item_id)
                cart_item = OggettoCart.objects.filter(user=self.user, accessorio=item).first()

            if cart_item:
                cart_item.delete()
            return True
        except:
            return False
        
    def get_items(self):
        return self.items.all()

    def get_costo_tot(self):
        costo_tot=0
        for item in self.get_items():
            if(item.mezzo):
                costo_tot += item.mezzo.prezzo
            else:
                costo_tot += item.accessorio.prezzo
        return costo_tot
    
    class Meta:
        verbose_name_plural = "Carrelli"

class Spedizione(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    via = models.TextField()
    citta = models.CharField(max_length=50)
    CAP = models.CharField(max_length=20)
    stato = models.CharField(max_length=50)
    is_appuntamento = models.BooleanField()
    dataora = models.DateTimeField()

    class Meta:
        verbose_name_plural = "Spedizioni"
