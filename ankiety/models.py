from django.db import models

# Create your models here.

class Pytanie(models.Model):
    pytanie_tekst = models.CharField(max_length=200)
    data_publ = models.DateTimeField("data opublikowania ankiety")


class Wybory(models.Model):
    pytanie = models.ForeignKey(Pytanie, on_delete=models.CASCADE)
    wybory_tekst = models.CharField(max_length=200)
    glosy = models.IntegerField(default=0)
    
