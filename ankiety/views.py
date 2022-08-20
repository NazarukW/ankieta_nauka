from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader
from .models import Pytanie, Wybory

# Create your views here.

def index(request):
    lista_ostatnich_pytan = Pytanie.objects.order_by("data_publ")[:5]
    context = {
        "lista_ostatnich_pytan": lista_ostatnich_pytan,
    }
    return render(request, "ankiety/index.html", context)
    
def detale(request, pytanie_id):
    pytanie = get_object_or_404(Pytanie, pk=pytanie_id)
    return render(request, "ankiety/detale.html", {"pytanie": pytanie})
    
def wyniki(request, pytanie_id):
    pytanie = get_object_or_404(Pytanie, pk=pytanie_id)
    return render(request, "ankiety/wyniki.html", {"pytanie": pytanie})
    
def glosy(request, pytanie_id):
    pytanie = get_object_or_404(Pytanie, pk=pytanie_id)
    try:
        wybrana_odpowiedz = pytanie.wybory_set.get(pk=request.POST["wybory"])
    except (KeyError, Wybory.DoesNotExist):
        #ponownie wyświetla formę z pytaniem
        return render(request, "ankiety/detale.html", {
            "pytanie": pytanie,
            "error_message": "Nie wybrałeś żadnej odpowiedzi",
        })
    else:
        wybrana_odpowiedz.glosy += 1
        wybrana_odpowiedz.save()
        return HttpResponseRedirect(reverse("ankiety:wyniki_glosowania", args=(pytanie.id,)))
    
