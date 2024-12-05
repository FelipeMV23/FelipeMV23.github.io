#toma_de_hora/models.py
from django.db import models
from usuarios.models import Perfil

class HoraMedica(models.Model):
    patient = models.ForeignKey(Perfil, on_delete=models.CASCADE, limit_choices_to={'user_type': 'patient'},related_name='toma_hora_horamedica')
    specialist = models.ForeignKey(Perfil, on_delete=models.CASCADE, limit_choices_to={'user_type': 'specialist'}, related_name='specialist_horamedica')
    date = models.DateField()
    time = models.TimeField()
    patient_rut = models.CharField(max_length=12, blank=True, null=True)
    specialist_rut = models.CharField(max_length=12, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Almacenar los RUTs antes de guardar la cita
        self.patient_rut = self.patient.rut
        self.specialist_rut = self.specialist.rut
        super().save(*args, **kwargs)

    @property
    def patient_first_name(self):
        return self.patient.user.first_name

    @property
    def patient_last_name(self):
        return self.patient.user.last_name

    @property
    def specialist_first_name(self):
        return self.specialist.user.first_name

    @property
    def specialist_last_name(self):
        return self.specialist.user.last_name


    def __str__(self):
        return f"Cita de {self.patient.user.first_name} {self.patient.user.last_name} con {self.specialist.user.first_name} {self.specialist.user.last_name} el {self.date} a las {self.time}"