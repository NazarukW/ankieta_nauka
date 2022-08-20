from django.urls import path
from . import views

app_name = "ankiety"
urlpatterns = [
    #np /ankiety/
    path("", views.index, name="index"),
    #np /ankiety/5
    path("<int:pytanie_id>/", views.detale, name="szczegóły"),
    #np /ankiety/5/wyniki/
    path("<int:pytanie_id>/wyniki/", views.wyniki, name="wyniki_glosowania"),
    #np /ankiety/5/glosy
    path("<int:pytanie_id>/glosy/", views.glosy, name="glosy_dla_pytania"),
]
