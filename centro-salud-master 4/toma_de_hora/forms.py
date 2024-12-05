# toma_de_hora/forms.py
from django import forms
from .models import HoraMedica
from usuarios.models import Perfil
from datetime import datetime, timedelta

class FormularioHoraMedica(forms.ModelForm):
    class Meta:
        model = HoraMedica
        fields = ['specialist', 'date', 'time']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(FormularioHoraMedica, self).__init__(*args, **kwargs)

        # Limitar la selección solo a especialistas
        self.fields['specialist'].queryset = Perfil.objects.filter(user_type='specialist')

        # Modificar la representación del queryset para incluir nombre y RUT
        self.fields['specialist'].label_from_instance = lambda obj: f"{obj.user.first_name} {obj.user.last_name} - RUT: {obj.rut}"

        # Definir los campos de fecha y hora
        self.fields['date'] = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
        self.fields['time'] = forms.ChoiceField(choices=[], required=True)

        # Obtener la fecha desde el formulario
        date = self.data.get('date') if 'date' in self.data else self.initial.get('date')

        if date:
            try:
                # Si estamos en modo edición, mostrar la hora actual seleccionada
                if self.instance and self.instance.pk:
                    current_time = self.instance.time.strftime("%H:%M")
                    self.fields['time'].choices = self._get_available_times(date) + [(current_time, current_time)]
                else:
                    self.fields['time'].choices = self._get_available_times(date)
            except (ValueError, TypeError):
                pass  # Manejo de errores

    def _get_available_times(self, date):
        """Devuelve los tiempos disponibles en base a la fecha seleccionada."""
        times = []
        start_time = datetime.strptime("08:00", "%H:%M")
        end_time = datetime.strptime("19:00", "%H:%M")

        # Generar intervalos de 45 minutos
        while start_time < end_time:
            appointment_time = start_time.strftime("%H:%M")
            times.append((appointment_time, appointment_time))  # Formato para choices
            start_time += timedelta(minutes=45)

        # Filtrar los tiempos que ya están ocupados
        appointments = HoraMedica.objects.filter(date=date)  # Usar el modelo HoraMedica
        booked_times = [appointment.time.strftime("%H:%M") for appointment in appointments]

        # Eliminar los tiempos ocupados
        available_times = [time for time in times if time[0] not in booked_times]

        return available_times  # Retornar una lista de tuples para choices
