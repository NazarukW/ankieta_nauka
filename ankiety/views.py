from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .models import Pytanie, Wybory

# Create your views here.


class IndexView(generic.ListView):
    template_name = "ankiety/index.html"
    context_object_name = "lista_ostatnich_pytan"

    def get_queryset(self):
        """Zwraca listę ostatnich pięciu pytań. Nie pokazuje tych co mają byśopublikowane w przyszłości"""
        return Pytanie.objects.filter(
            data_publ__lte=timezone.now()
        ).order_by("-data_publ")[:5]


class DetaleView(generic.DetailView):
    model = Pytanie
    template_name = "ankiety/detale.html"

    def get_queryset(self):
        """
        Nie wyświetla ankiet, które nie są jeszcze opublikowane
        """
        return Pytanie.objects.filter(data_publ__lte=timezone.now())

    
class WynikiView(generic.DetailView):
    model = Pytanie
    template_name = "ankiety/wyniki.html"


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
    
