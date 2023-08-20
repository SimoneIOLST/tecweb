from django.http import HttpResponse
from django.shortcuts import render

def home_page(request):
    lista=range(1,39)
    ctx = {"lista": lista}
    return render(request, template_name="base.html", context=ctx)