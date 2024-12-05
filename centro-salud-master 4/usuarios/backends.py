from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from usuarios.models import Perfil
from django.db.models import Q

class RUTAuthenticationBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Intenta buscar por RUT, nombre de usuario o correo electrónico
            user = User.objects.filter(
                Q(username=username) | 
                Q(email=username) | 
                Q(perfil__rut=username)  # Relacionamos el RUT con el perfil del usuario
            ).distinct().first()

            # Verifica si se encontró el usuario
            if user and user.check_password(password):
                profile = user.perfil  # Accede al perfil del usuario
                # Aquí puedes agregar lógica para restringir el acceso según el tipo de usuario
                if profile.user_type == 'patient':  # Solo permite acceso a pacientes, por ejemplo
                    return user
                # Agrega más condiciones para otros tipos de usuarios si es necesario
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None