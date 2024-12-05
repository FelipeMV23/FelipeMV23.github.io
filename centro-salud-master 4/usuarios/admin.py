from django import forms
from django.contrib import admin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from usuarios.models import Perfil
from toma_de_hora.models import HoraMedica
 

class PerfilAdmin(admin.ModelAdmin):
    list_display = ('user', 'rut')
    search_fields = ('user__username', 'user__email', 'rut')

    # Permitir la edición del campo user_type en el panel de admin
    fields = ('user', 'user_type', 'rut')  # Asegura que el campo 'user_type' esté disponible para edición
    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            # No permitir que usuarios que no sean superusuarios cambien el user_type
            obj.user_type = Perfil.objects.get(pk=obj.pk).user_type
        super().save_model(request, obj, form, change)
admin.site.register(Perfil, PerfilAdmin)

class HoraMedicaAdmin(admin.ModelAdmin):
    list_display = ('get_patient_name', 'date', 'time', 'get_specialist_name')
    
    def get_patient_name(self, obj):
        return f"{obj.patient.user.first_name} {obj.patient.user.last_name}"
    get_patient_name.admin_order_field = 'patient'  # permite ordenar por este campo
    get_patient_name.short_description = 'Paciente'  # nombre de la columna
    
    def get_specialist_name(self, obj):
        return f"{obj.specialist_first_name} {obj.specialist_last_name}"
    get_specialist_name.admin_order_field = 'specialist_first_name'  # permite ordenar por este campo
    get_specialist_name.short_description = 'Especialista'  # nombre de la columna

admin.site.register(HoraMedica, HoraMedicaAdmin)