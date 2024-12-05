from django.urls import path
from usuarios import views

urlpatterns = [
    path('registrar-paciente/', views.registrar_paciente, name='registrar_paciente'),
    path('registrar-especialista/', views.registrar_especialista, name='registrar_especialista'),
    path('iniciar-sesion/', views.iniciar_sesion, name='iniciar_sesion'),
    path('cerrar-sesion/', views.cerrar_sesion, name='cerrar_sesion'),
    path('perfil-usuario/', views.perfil_usuario, name='perfil_usuario'),
    path('editar-perfil/', views.editar_perfil, name='editar_perfil')
]
