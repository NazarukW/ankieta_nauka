import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Pytanie


class PytanieModelTests(TestCase):

    def test_pytanie_zostalo_opublikowane_z_data_z_przyszlosci(self):
        """
        ostatnio_opublikowane() zwraca False jeśli data_publ jest z przyszłości
        """
        time = timezone.now() + datetime.timedelta(days=30)
        przyszle_pytanie = Pytanie(data_publ=time)
        self.assertIs(przyszle_pytanie.ostatnio_opublikowane(), False)

    def test_pytanie_zostalo_opublikowane_wiecej_niz_dzien_temu(self):
        """
        ostatnio_opublikowane() zwraca False jeśli pytanie zostało opublikowane więcej niż dzień temu
        """
        czas = timezone.now() - datetime.timedelta(days=1, seconds=1)
        stare_pytanie = Pytanie(data_publ=czas)
        self.assertIs(stare_pytanie.ostatnio_opublikowane(), False)

    def test_pytanie_zostalo_opublikowane_mniej_niz_dzien_temu(self):
        """
        ostatnio_opublikowane() zwraca True jeśli pytanie zostało opublokowane mniej niż dzień temu
        """
        czas = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        nowe_pytanie = Pytanie(data_publ=czas)
        self.assertIs(nowe_pytanie.ostatnio_opublikowane(), True)


def nowa_ankieta(pytanie_tekst, dni):
    """
    Tworzy pytanie z danym tekstem (pytanie_text) o z przesunięciem o dni. dni są ujemne dla pytań opubikowanych
    dawno i dodatnie dla pytań, które mają być opublikowane
    """
    czas = timezone.now() + datetime.timedelta(days=dni)
    return Pytanie.objects.create(pytanie_tekst=pytanie_tekst, data_publ=czas)


class PytanieIndexViewTest(TestCase):
    def test_brak_ankiet(self):
        """
        Wyświetla odpowiednią informację, jeśli nie ma ankiet do wyświetlenia
        """
        response = self.client.get(reverse("ankiety:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Brak ankiet do wyświetlenia.")
        self.assertQuerysetEqual(response.context["lista_ostatnich_pytan"], [],)

    def test_pytania_z_przeszlosci(self):
        """
        Pytania z datą publikacji z przeszłości są wyświetlane na stronie index
        """
        pytanie = nowa_ankieta(pytanie_tekst="przeszłe ankiety", dni=-30)
        response = self.client.get(reverse("ankiety:index"))
        self.assertQuerysetEqual(
            response.context["lista_ostatnich_pytan"],
            [pytanie],
        )

    def test_pytania_z_przyszlosci(self):
        """
        Pytania z datą publikacji z przyszłości nie są wyświetlane na stronie index
        """
        nowa_ankieta(pytanie_tekst="przyszłe ankiety", dni=30)
        response = self.client.get(reverse("ankiety:index"))
        self.assertContains(response, "Brak ankiet do wyświetlenia.")
        self.assertQuerysetEqual(
            response.context["lista_ostatnich_pytan"], [],
        )

    def test_pytanie_z_przeszlosci_i_przyszlosci(self):
        """
        Jeśli są dwa pytania, jedno z przyszłości i jedno z przeszłości to jest wyświetlane tylko to z przeszłosci
        """
        pytanie = nowa_ankieta(pytanie_tekst="przeszłe ankiety", dni=-30)
        nowa_ankieta(pytanie_tekst="przyszłe ankiety", dni=30)
        response = self.client.get(reverse("ankiety:index"))
        self.assertQuerysetEqual(
            response.context["lista_ostatnich_pytan"],
            [pytanie],
        )

    def test_dwa_pytania_z_przeszlosci(self):
        """
        Strona domowa może wyświetlać wiele pytań
        """
        pytanie1 = nowa_ankieta(pytanie_tekst="przeszłe ankiety1", dni=-30)
        pytanie2 = nowa_ankieta(pytanie_tekst="przeszłe ankiety2", dni=-3)
        response = self.client.get(reverse("ankiety:index"))
        self.assertQuerysetEqual(
            response.context["lista_ostatnich_pytan"],
            [pytanie2, pytanie1],
        )


class PytanieDetaleViewTests(TestCase):
    def test_pytanie_nieopublikowane(self):
        """
        Próba wyswietlenia szczegółów ankiety nieopublikowanej (z przyszłości) zwraca 404 not found
        """
        przyszle_pytanie = nowa_ankieta(pytanie_tekst="Ankieta z przyszłości", dni=5)
        url = reverse("ankiety:szczegóły", args=(przyszle_pytanie.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_pytanie_opublikowane(self):
        """
        Widok szczegółów opublikowanej ankiety (data_publ z przeszłości) wyświetla pytanie ankiety
        """
        pytanie_przeszle = nowa_ankieta(pytanie_tekst="Ankieta z przeszłości", dni=-5)
        url = reverse("ankiety:szczegóły", args=(pytanie_przeszle.id,))
        response = self.client.get(url)
        self.assertContains(response, pytanie_przeszle.pytanie_tekst)
