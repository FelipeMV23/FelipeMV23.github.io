# ficha_medica/forms.py
from django import forms
from .models import FichaMedica

class FichaMedicaForm(forms.ModelForm):
    class Meta:
        model = FichaMedica
        fields = [
            'telefono_contacto',
            'correo_electronico',
            'direccion',
            'enfermedades_preexistentes',
            'alergias',
            'medicamentos_actuales',
            'intervenciones_previas',
            'notas_especialista',
        ]
        widgets = {
            'telefono_contacto': forms.TextInput(attrs={'pattern': '[0-9]*', 'maxlength': '15'}),
            'correo_electronico': forms.EmailInput(attrs={'required': False}),
            'direccion': forms.TextInput(attrs={'maxlength': '255'}),
            'enfermedades_preexistentes': forms.Textarea(attrs={'rows': 3}),
            'alergias': forms.Textarea(attrs={'rows': 3}),
            'medicamentos_actuales': forms.Textarea(attrs={'rows': 3}),
            'intervenciones_previas': forms.Textarea(attrs={'rows': 3}),
            'notas_especialista': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_telefono_contacto(self):
        telefono_contacto = self.cleaned_data.get('telefono_contacto')
        if not telefono_contacto.isdigit():
            raise forms.ValidationError("El número de teléfono solo puede contener dígitos.")
        return telefono_contacto

    def clean_correo_electronico(self):
        correo_electronico = self.cleaned_data.get('correo_electronico')
        if correo_electronico and not forms.EmailField().clean(correo_electronico):
            raise forms.ValidationError("Por favor, introduce un correo electrónico válido.")
        return correo_electronico

    def clean_direccion(self):
        direccion = self.cleaned_data.get('direccion')
        if not direccion:
            raise forms.ValidationError("La dirección es obligatoria.")
        return direccion
