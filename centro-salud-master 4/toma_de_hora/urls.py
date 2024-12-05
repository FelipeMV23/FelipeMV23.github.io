from django.urls import path
from . import views
from toma_de_hora import views

urlpatterns = [
    path('toma-de-hora/', views.toma_de_hora, name='toma_de_hora'),
    path('horas-disponibles/', views.horas_disponibles, name='horas_disponibles'),
    path('eliminar-hora/<int:hora_id>/', views.eliminar_hora, name='eliminar_hora'),
]
