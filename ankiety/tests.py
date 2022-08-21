import datetime

from django.test import TestCase
from django.utils import timezone

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
