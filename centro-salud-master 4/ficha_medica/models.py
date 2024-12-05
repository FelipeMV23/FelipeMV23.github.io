#ficha_medica/models.py
from django.db import models
from toma_de_hora.models import HoraMedica  # Importar el modelo HoraMedica
from django.core.validators import RegexValidator

class FichaMedica(models.Model):
    # Regex for validating phone numbers (example format: +56912345678)
    phone_validator = RegexValidator(regex=r'^\+?[0-9]{7,15}$', message="El teléfono debe ser un número entre 7 y 15 dígitos.")

    hora_medica = models.OneToOneField(HoraMedica, on_delete=models.CASCADE, related_name='ficha_medica')
    telefono_contacto = models.CharField(max_length=15, validators=[phone_validator], help_text="Formato: +56912345678 o 912345678.")
    correo_electronico = models.EmailField(help_text="Ingrese un correo electrónico válido.")
    direccion = models.CharField(max_length=255, help_text="Ingrese la dirección completa.")
    enfermedades_preexistentes = models.TextField(blank=True, help_text="Enumere las enfermedades preexistentes.")
    alergias = models.TextField(blank=True, help_text="Enumere las alergias conocidas.")
    medicamentos_actuales = models.TextField(blank=True, help_text="Enumere los medicamentos que está tomando actualmente.")
    intervenciones_previas = models.TextField(blank=True, help_text="Enumere las intervenciones quirúrgicas previas.")
    notas_especialista = models.TextField(blank=True, help_text="Notas del especialista sobre el paciente.")

    def __str__(self):
        return f"Ficha de {self.hora_medica.patient_first_name} {self.hora_medica.patient_last_name}"

    class Meta:
        verbose_name = "Ficha Médica"
        verbose_name_plural = "Fichas Médicas"
        ordering = ['hora_medica']
