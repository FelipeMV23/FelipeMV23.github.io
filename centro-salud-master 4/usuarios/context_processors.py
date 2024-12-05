from usuarios.models import Perfil

def user_profile(request):
    if request.user.is_authenticated:
        try:
            perfil = request.user.perfil
            return {'perfil': perfil}
        except Perfil.DoesNotExist:
            return {'perfil': None}
    return {'perfil': None}