# Generated by Django 5.1.2 on 2024-12-05 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='perfil',
            name='especilidad',
            field=models.CharField(blank=True, choices=[('psiquiatra', 'Psiquiatra'), ('psicologo', 'Psicólogo')], max_length=200, null=True),
        ),
    ]