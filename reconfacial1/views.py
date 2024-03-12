

from django.shortcuts import render, redirect
from django.http import HttpResponse
from reconfacial1.models import Persona
from reconfacial1.forms import PersonaForm
from reconfacial1.capturandoRostros import capturar_rostros3
from .entrenandoRF import entrenando

import os
data_path = 'C:/xampp/htdocs/crud/biometrikAssProject/data' 
# Create your views here.

def home(request):
    return render(request, 'home.html')

def capturar_rostros(request):
    if request.method == 'POST':
        form = PersonaForm(request.POST)
        if form.is_valid():
            # Obtener los datos del formulario
            cedula = form.cleaned_data['CEDULA']
            nombre = form.cleaned_data['NOMBRE']
            apellido = form.cleaned_data['APELLIDO']
            
            # Impresión de depuración
            print("Datos del formulario:", cedula, nombre, apellido)

            # Llamar a capturar_rostros3 con los datos del formulario
            capturar_rostros3(cedula, nombre, apellido) 
            
            # Redirigir a una página de éxito
            return redirect('reconfacial1:capturar_rostros_exitoso', cedula=cedula, nombre=nombre, apellido=apellido)
    else:
        form = PersonaForm()
    return render(request, 'capturaRostros.html', {'form': form})


# En la vista capturar_rostros_exitoso
def capturar_rostros_exitoso(request, cedula, nombre, apellido):
    print("Procesando solicitud de captura de rostros exitosa...")

    # Obtener la lista de nombres de archivo de las imágenes en la carpeta de la persona
    file_names = [f'rostro_{i}.jpg' for i in range(299)]  # Lista de nombres de archivo de 0 a 4
    print("Nombres de archivos:", file_names)

    # Definir la ruta de la carpeta de la persona (person_folder_path)
    person_folder_path = os.path.join(data_path, cedula, nombre, apellido)
    print("Ruta de la carpeta de la persona:", person_folder_path)

    # Pasar las variables al contexto del template
    context = {
        'file_names': file_names,
        'person_folder_path': person_folder_path,
    }

    # Renderizar la plantilla con el contexto
    return render(request, 'capturar_rostros_exitoso.html', context)


def entrenandoRF(request):
    if request.method == 'POST':
        form = PersonaForm(request.POST)
        if form.is_valid():
            # Suponiendo que obtienes los datos de CEDULA, NOMBRE y APELLIDO del formulario válido
            cedula = form.cleaned_data['CEDULA']
            nombre = form.cleaned_data['NOMBRE']
            apellido = form.cleaned_data['APELLIDO']

            # Impresión de depuración
            print("Datos del formulario:", cedula, nombre, apellido)

            # Llama a la función 'entrenando' con los datos obtenidos
            entrenando(cedula, nombre, apellido)

            # Redirige a la página de éxito después de completar el entrenamiento
            return render(request, 'entrenamiento_exitoso.html')

    # Si llegamos aquí, significa que el formulario no es válido o estamos en una solicitud GET
    # En cualquiera de los casos, renderizamos la plantilla entrenandoRF.html con el formulario
    form = PersonaForm()  # Crea una instancia del formulario para la solicitud GET o para mostrar errores de validación POST
    return render(request, 'entrenandoRF.html', {'form': form})


def reconocer(request):
    return render(request,'reconoceRostros.html')
