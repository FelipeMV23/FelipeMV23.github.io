from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from usuarios.forms import FormularioPaciente, FormularioEspecialista
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.models import User
from usuarios.models import Perfil
from toma_de_hora.models import HoraMedica

#inicio de sesión y registro de usuario paciente
def iniciar_sesion(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('inicio')
        else:
            messages.error(request, 'Nombre de usuario o contraseña no válidos')
    return render(request, 'navegacion/iniciar_sesion.html')

def registrar_paciente(request):
    if request.method == 'POST':
        form = FormularioPaciente(request.POST)
        if form.is_valid():
            user = form.save()
            if user:  # Verifica si el usuario se ha guardado
                username = form.cleaned_data.get('username')
                messages.success(request, f'Usuario {username} creado con éxito.')
                return redirect('iniciar_sesion')
            else:
                messages.error(request, 'Error al registrar el usuario.')
        else:
            messages.error(request, 'Formulario inválido. Revisa los errores.')
    else:
        form = FormularioPaciente()

    return render(request, 'navegacion/registrar_paciente.html', {'form': form})

# Verificar si el usuario es administrador
def admin_check(user):
    return user.is_superuser

#inicio de sesión y registro de usuario especialista
def registrar_especialista(request):
    if request.method == 'POST':
        form = FormularioEspecialista(request.POST)
        if form.is_valid():
            user = form.save()
            if user:
                username = form.cleaned_data.get('username')
                messages.success(request, f'Especialista {username} registrado con éxito.')
                return redirect('inicio')
            else:
                messages.error(request, 'Error al registrar el especialista.')
        else:
            messages.error(request, 'Formulario inválido. Revisa los errores.')
    else:
        form = FormularioEspecialista()

    return render(request, 'navegacion/registrar_especialista.html', {'form': form})

#Cerrar sesion
@login_required
def cerrar_sesion(request):
    logout(request)
    return redirect('inicio')

@login_required
def perfil_usuario(request):
    perfil = Perfil.objects.get(user=request.user)
    perfil.rut = formatear_rut(perfil.rut)
    # Obtener las horas tomadas por el paciente
    horas_tomadas = HoraMedica.objects.filter(patient=perfil)

    # Formatear las horas en un formato más amigable
    horas_tomadas_formateadas = [
        f"{hora.date} a las {hora.time} con Dr(a). {hora.specialist_first_name} {hora.specialist_last_name}" 
        for hora in horas_tomadas
    ]

    return render(request, "perfil_usuario/perfiles.html", {
        "perfiles": perfil,
        "rut": perfil.rut,
        "horas": horas_tomadas  # Cambié esto para asegurarte de que el ID es correcto
    })

@login_required
def editar_perfil(request):
    if request.method == 'POST':
        user = request.user
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')

        # Actualizar los campos que se envían
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        if email:
            user.email = email
        
        user.save()
        return redirect('perfil_usuario')  # Redirige a la página de perfil después de guardar los cambios
    
    return render(request, 'perfil_usuario/perfiles.html')

def formatear_rut(rut):
    # Elimina los caracteres no numéricos (puntos y guion)
    rut_limpio = rut.replace('.', '').replace('-', '')
    
    try:
        # Convierte la parte numérica del RUT a entero
        formatted_rut_body = "{:,}".format(int(rut_limpio[:-1])).replace(",", ".")
        formatted_rut_dv = rut_limpio[-1]  # Obtiene el dígito verificador
    except ValueError:
        # Manejo de error si no se puede convertir a entero
        return None  # O puedes devolver el RUT original o un mensaje de error

    return f"{formatted_rut_body}-{formatted_rut_dv}"


