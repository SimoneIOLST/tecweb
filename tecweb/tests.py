from django.test import TestCase, Client
from gestione.models import *


# Create your tests here.
#class TestStruttura(TestCase):
#    def setUp(self):
#        Venditore.objects.create(cf="prova", iban="ibandiprova", telefono="123456789", pec="prova@pec.it", 
#                                 mail="mail@mail.it", indirizzo="indprova", citta="cittaprova", nome="perfavore", provincia="MO")
#        Accessorio.objects.create(per_moto=True, descrzione ="ciao", venditore_id="prova", nome="Pippo Paperino", prezzo = 5.9)
#
#    def test_if_structure_has_info(self):
#        a = Accessorio.objects.get(nome="Pippo Paperino")
#        self.assertEqual(get_structure_info(self, 1), (200, a))
#
#    def test_if_structure_is_not_there(self):
#        Accessorio.objects.get(nome="Pippo Paperino").delete()
#        self.assertEqual(
#            get_structure_info(self, 1), (404, "La struttura selezionata non esiste.")
#        )
#
#    def tearDown(self):
#        Accessorio.objects.all().delete()


c = Client()
response = c.post(
    "/login",
    {"password": "Password123!", "username": "IOLST"}
)

print("\n", response)
#per via del redirect
if response.status_code != 301:
    print("Non esiste l'utente IOLST\n")
else:
    print("Utente IOLST trovato\n")


response = c.get("/gestione/listaacc/")
if response.status_code == 200:
    print("La risposta è corretta")
    if('gestione/listaAcc.html' in response.template_name):
        print("Template corretto")
    else:
        print("Errore nei template caricati")
else:
    print("Codice risposta errato")


response = c.get("/gestione/listamezzi/")
print(response.template_name)
print(response.status_code)
if response.status_code == 200:
    print("La risposta è corretta")
    if('gestione/listaAcc.html' in response.template_name):
        print("Template corretto")
    else:
        print("Errore nei template caricati")
else:
    print("Codice risposta errato")