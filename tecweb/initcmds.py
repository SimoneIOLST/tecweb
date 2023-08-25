from gestione.models import ImmaginiMacchina, Mezzo



def erase_db():
    print("Cancello il DB")
    ImmaginiMacchina.objects.all().delete()
    Mezzo.objects.all().delete()

def init_db():
    
    if len(Mezzo.objects.all()) != 0:
        return

    macchinadict = {
        "moto": [False, False],
        "prezzo" : [51900, 215000],
        "marca" : ["Mercedes-Benz", "Mercedes-Benz"],
        "modello" : ["SL", "SL"],
        "kilometraggio" : [88500, 80],
        "colore" : ["grigio", "bianco"],
        "data_fabbricazione": ['2014-07-01', '2022-07-01'],
        "num_proprietari": [2, 1]
    }

    

    for i in range(2):
        m = Mezzo()
        for k in macchinadict:
            if k == "moto":
                    m.moto = macchinadict[k][i]
            if k == "prezzo":
                    m.prezzo = macchinadict[k][i]
            if k == "marca":
                    m.marca = macchinadict[k][i]
            if k == "modello":
                m.modello = macchinadict[k][i]
            if k == "kilometraggio":
                    m.kilometraggio = macchinadict[k][i]
            if k == "colore":
                    m.colore = macchinadict[k][i]
            if k == "data_fabbricazione":
                    m.data_fabbricazione = macchinadict[k][i]
            if k == "num_proprietari":
                    m.num_proprietari = macchinadict[k][i]
                
        m.save()


    print("DUMP DB")
    print(Mezzo.objects.all()) #controlliamo