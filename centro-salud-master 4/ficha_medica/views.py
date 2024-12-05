#ficha_medica/views.py
from django.http import Http404
from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404, redirect
from toma_de_hora.models import HoraMedica
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from usuarios.models import Perfil
from django.shortcuts import render, get_object_or_404, redirect
from toma_de_hora.forms import FormularioHoraMedica
from django.core.exceptions import ValidationError
from ficha_medica.models import FichaMedica
from .forms import FichaMedicaForm


@login_required
def listar_hora(request, id=None):
    form = None
    # Filtra las horas médicas solo del especialista logueado
    horas_medicas = HoraMedica.objects.filter(specialist__user=request.user)

    try:
        if id:
            hora = get_object_or_404(HoraMedica, id=id)
        else:
            hora = None

        # Si hay una hora médica y no hay ficha médica, crear una nueva ficha
        ficha = None
        if hora:
            ficha = FichaMedica.objects.filter(hora_medica=hora).first()  # Buscar la ficha médica relacionada

        if request.method == 'POST':
            # Si ya existe una ficha, la editamos; si no, la creamos
            if ficha:
                form = FichaMedicaForm(request.POST, instance=ficha)
            else:
                form = FichaMedicaForm(request.POST)

            if form.is_valid():
                ficha_medica = form.save(commit=False)
                ficha_medica.hora_medica = hora  # Asignamos la hora médica si existe
                ficha_medica.save()
                messages.success(request, 'La ficha médica ha sido guardada correctamente.')
                return redirect('listar_hora')  # Redirige a la misma página después de guardar
            else:
                messages.error(request, 'Por favor corrige los errores en el formulario.')
        else:
            # Si el método es GET, mostramos el formulario para crear o editar la ficha médica
            if ficha:
                form = FichaMedicaForm(instance=ficha)  # Para editar
            else:
                form = FichaMedicaForm()  # Para crear

    except Exception as e:
        messages.error(request, f"Ocurrió un error inesperado: {str(e)}")

    return render(request, 'ficha_medica/listar_fichas.html', {
        'form': form,
        'horas': horas_medicas,
        'hora': hora,  # Pasamos la hora médica actual
        'ficha': ficha,  # Pasamos la ficha médica actual si existe
    })

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


 # Suponiendo que tienes un formulario para editar

def editar_hora(request, id):
    hora = get_object_or_404(HoraMedica, id=id)
    perfil_hora = get_object_or_404(Perfil, id=hora.patient.id)  # Usamos el `id` del paciente en lugar del `id` de la cita

    if request.method == 'POST':
        form = FormularioHoraMedica(request.POST, instance=hora)
        if form.is_valid():
            form.save()
            return redirect('listar_hora')
    else:
        form = FormularioHoraMedica(instance=hora)

    return render(request, 'listar_fichas.html', {'form': form})


from django.http import JsonResponse

@login_required
def crear_ficha_medica(request, hora_id):
    hora = get_object_or_404(HoraMedica, id=hora_id)
    ficha_medica, created = FichaMedica.objects.get_or_create(hora_medica=hora)

    if request.method == 'POST':
        form = FichaMedicaForm(request.POST, instance=ficha_medica)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': form.errors.as_json()})
    else:
        form = FichaMedicaForm(instance=ficha_medica)

    context = {
        'form': form,
        'hora': hora,
    }
    return render(request, 'ficha_medica/crear_ficha_medica.html', context)
