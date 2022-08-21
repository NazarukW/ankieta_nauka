from django.db import models
import datetime
from django.utils import timezone

# Create your models here.

class Pytanie(models.Model):
    pytanie_tekst = models.CharField(max_length=200)
    data_publ = models.DateTimeField("data opublikowania ankiety")
    
    def __str__(self):
        return self.pytanie_tekst
        
    def ostatnio_opublikowane(self):
        teraz = timezone.now()
        return teraz - datetime.timedelta(days=1) <= self.data_publ <= teraz


class Wybory(models.Model):
    pytanie = models.ForeignKey(Pytanie, on_delete=models.CASCADE)
    wybory_tekst = models.CharField(max_length=200)
    glosy = models.IntegerField(default=0)
    
    def __str__(self):
        return self.wybory_tekst
    
