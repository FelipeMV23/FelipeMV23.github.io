#ficha_medica/urls.py
from django.urls import path
from usuarios.views import perfil_usuario
from .views import listar_hora, editar_hora, crear_ficha_medica

urlpatterns = [
    path('perfil-usuario/', perfil_usuario, name='perfil_usuario'),
    path('fichas/listar-hora/<int:id>/', listar_hora, name='listar_hora'),
    path('listar-hora/', listar_hora, name='listar_hora'),
    path('editar-hora/<int:id>/', editar_hora, name='editar_hora'),
    path('crear-ficha-medica/<int:hora_id>/', crear_ficha_medica, name='crear_ficha_medica')
]