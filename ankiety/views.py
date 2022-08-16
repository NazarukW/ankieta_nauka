from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Pytanie

# Create your views here.

def index(request):
    lista_ostatnich_pytan = Pytanie.objects.order_by("data_publ")[:5]
    context = {
        "lista_ostatnich_pytan": lista_ostatnich_pytan,
    }
    return render(request, "ankiety/index.html", context)
    
def detale(request, pytanie_id):
    return HttpResponse(f"Patrzysz na pytanie nr {pytanie_id}")
    
def wyniki(request, pytanie_id):
    return HttpResponse(f"Patrzysz na wyniki pytania nr {pytanie_id}")
    
def glosy(request, pytanie_id):
    return HttpResponse(f"Patrzysz na głosy pytania nr {pytanie_id}")
    
