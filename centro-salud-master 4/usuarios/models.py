from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

class Perfil(models.Model):
    USER_TYPE_CHOICES = [
        ('patient', 'Paciente'),
        ('specialist', 'Especialista'),
    ]

    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE) # type: ignore
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='patient')
    rut = models.CharField(max_length=12, unique=True, blank=True, null=True)
    CHOICE_ESPECILIDAD = (
    ('psiquiatra', 'Psiquiatra'),
    ('psicologo', 'Psicólogo'),
    )
    especilidad = models.CharField(max_length=200, choices=CHOICE_ESPECILIDAD,blank=True, null=True)

    def __str__(self):
        return self.user.username
    
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.perfil.save()