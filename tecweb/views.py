from django.http import HttpResponse
from django.shortcuts import render

def home_page(request):
    lista=range(1,39)
    num_acc=range(1,39)
    ctx = {"lista": lista, "num_acc": num_acc}
    return render(request, template_name="base.html", context=ctx)

