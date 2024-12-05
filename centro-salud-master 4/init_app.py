import subprocess
import os

def run_command(command):
    """Ejecuta un comando en el terminal"""
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    
    if process.returncode != 0:
        print(f"Error ejecutando el comando: {command}")
        print(stderr.decode())
    else:
        print(f"Comando ejecutado correctamente: {command}")
        print(stdout.decode())

def init_django_app():
    # Instalar las dependencias
    print("Instalando dependencias...")
    run_command("pip install -r requirements.txt")
    
    # Realizar migraciones de la base de datos
    print("Aplicando migraciones...")
    run_command("python manage.py migrate")
    
    # Crear superusuario (si es necesario)
    print("Creando superusuario si no existe...")
    run_command("python manage.py createsuperuser --noinput")
    
    # Ejecutar el servidor de desarrollo
    print("Iniciando el servidor de desarrollo...")
    run_command("python manage.py runserver")

if __name__ == "__main__":
    init_django_app()