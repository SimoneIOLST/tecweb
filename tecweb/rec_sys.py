from collections import Counter
from gestione.models import *

def recommend_mezzi(user):
    favorite_mezzi = FavouriteMezzo.objects.filter(user=user).values_list('mezzo', flat=True)
    favorite_marche = Mezzo.objects.filter(id__in=favorite_mezzi).values_list('marca', flat=True)
    
    brand_counts = Counter(favorite_marche) 

    recommended_mezzi = []

    marche_sort = sorted(brand_counts.items(), key=lambda x: x[1], reverse=True)

    for brand, _ in marche_sort:
        recommended_mezzi.extend(Mezzo.objects.filter(marca=brand).exclude(id__in=favorite_mezzi))
    
    lista=[]
    for i in recommended_mezzi:
        lista.append(i.id)
    non_recommended_mezzi =[]
    non_recommended_mezzi = Mezzo.objects.exclude(id__in=lista)
    
    recommended_mezzi += non_recommended_mezzi

    return recommended_mezzi
