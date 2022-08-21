from django.urls import path
from . import views

app_name = "ankiety"
urlpatterns = [
    #np /ankiety/
    path("", views.IndexView.as_view(), name="index"),
    #np /ankiety/5
    path("<int:pk>/", views.DetaleView.as_view(), name="szczegóły"),
    #np /ankiety/5/wyniki/
    path("<int:pk>/wyniki/", views.WynikiView.as_view(), name="wyniki_glosowania"),
    #np /ankiety/5/glosy
    path("<int:pytanie_id>/glosy/", views.glosy, name="glosy_dla_pytania"),
]
