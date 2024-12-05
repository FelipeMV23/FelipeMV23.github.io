from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from toma_de_hora.forms import FormularioHoraMedica
from toma_de_hora.models import HoraMedica
from django.utils import timezone
from django.http import JsonResponse
from django.contrib import messages

from usuarios.models import Perfil

@login_required
def toma_de_hora(request):
    if request.method == 'POST':
        form = FormularioHoraMedica(request.POST, user=request.user)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user.perfil
            appointment.save()  # Guardamos la cita

            # Mensaje de éxito
            messages.success(request, 
                             f'Hora tomada con éxito: {appointment.patient_first_name} {appointment.patient_last_name} (RUT: {appointment.patient.rut}) con {appointment.specialist_first_name} {appointment.specialist_last_name} (RUT: {appointment.specialist.rut}) el {appointment.date} a las {appointment.time}')
            return redirect('toma_de_hora')  # Redirigir al inicio después de tomar la cita
    else:
        form = FormularioHoraMedica(user=request.user)

    return render(request, 'tomar_hora/tomar_hora.html', {'form': form})

def horas_disponibles(request):
    date_str = request.GET.get('date')
    date = timezone.datetime.strptime(date_str, '%Y-%m-%d').date()
    occupied_times = HoraMedica.objects.filter(date=date).values_list('time', flat=True)

    # Generar todas las horas disponibles
    available_times = []
    start_time = timezone.datetime.now().replace(hour=8, minute=0, second=0)
    end_time = timezone.datetime.now().replace(hour=19, minute=0, second=0)

    while start_time < end_time:
        if start_time.time() not in occupied_times:
            available_times.append(start_time.time().strftime('%H:%M'))
        start_time += timezone.timedelta(minutes=45)

    return JsonResponse({'times': available_times})

from django.shortcuts import get_object_or_404, redirect
from .models import HoraMedica

@login_required
def eliminar_hora(request, hora_id):
    if request.method == 'POST':
        hora = get_object_or_404(HoraMedica, id=hora_id)
        hora.delete()
        messages.success(request, f"Hora {hora_id} eliminada con éxito.")

    return redirect('perfil_usuario')

