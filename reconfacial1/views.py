

from urllib import request
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
    print("Entering the home view function")
    
    # Render the home.html template
    response = render(request, 'home.html')
    
    print("Leaving the home view function")
    
    return response

def capturar_rostros(request):
    print("Entering capturar_rostros view function")

    if request.method == 'POST':
        print("HTTP method is POST")
        form = PersonaForm(request.POST)
        if form.is_valid():
            print("Form is valid")
            cedula = form.cleaned_data['CEDULA']
            nombre = form.cleaned_data['NOMBRE']
            apellido = form.cleaned_data['APELLIDO']
            
            print("Datos del formulario:", cedula, nombre, apellido)

            capturar_rostros3(cedula, nombre, apellido) 
            
            print("Redirecting to capturar_rostros_exitoso")
            return redirect('reconfacial1:capturar_rostros_exitoso', cedula=cedula, nombre=nombre, apellido=apellido)
        else:
            print("Form is not valid")
    else:
        print("HTTP method is not POST")
        form = PersonaForm()
        print("Rendering capturaRostros.html template")

    print("Leaving capturar_rostros view function")

    return render(request, 'capturaRostros.html', {'form': form})


# En la vista capturar_rostros_exitoso
def capturar_rostros_exitoso(request, cedula, nombre, apellido):
    print("Entering capturar_rostros_exitoso view function")
    print("Request method:", request.method)
    print("Cédula:", cedula)
    print("Nombre:", nombre)
    print("Apellido:", apellido)

    if request.method == 'POST':
        form = PersonaForm(request.POST)
        if form.is_valid():
            print("Form is valid")
            cedula = form.cleaned_data['CEDULA']
            nombre = form.cleaned_data['NOMBRE']
            apellido = form.cleaned_data['APELLIDO']
            print("Datos del formulario:", cedula, nombre, apellido)

            # Obtener la lista de nombres de archivo de las imágenes en la carpeta de la persona
            file_names = [f'rostro_{i}.jpg' for i in range(299)]  # Lista de nombres de archivo de 0 a 299
            print("Nombres de archivos:", file_names)

            # Definir la ruta de la carpeta de la persona (person_folder_path)
            person_folder_path = os.path.join(data_path, cedula, nombre, apellido)
            print("Ruta de la carpeta de la persona:", person_folder_path)

            context = {
                'file_names': file_names,
                'person_folder_path': person_folder_path,
            }

            print("Redirecting to entrenandoRF")
            return redirect('reconfacial1:entrenandoRF', cedula=cedula, nombre=nombre, apellido=apellido)

    print("Rendering capturar_rostros_exitoso.html template")
    return render(request, 'capturar_rostros_exitoso.html', context)


def entrenandoRF(request,cedula, nombre, apellido):
    print("Entering entrenandoRF view function")
    print("Request method:", request.method)

    if request.method == 'POST':
  
        print("HTTP method is POST")
        form = PersonaForm(request.POST)
        if form.is_valid():
            print("Form is valid")
            persona = form.save()
            # Call the 'entrenando' function with the form data
            resultado_entrenamiento = entrenando(request, cedula, nombre, apellido, photo_path)

            print("Redirecting to entrenandoRF_exitoso")
            return HttpResponse(resultado_entrenamiento)  # Render the training result
        else:
            print("Form is not valid")
            print("Form errors:", form.errors)
    else:
        print("HTTP method is not POST")
        form = PersonaForm()  # Create a form instance for GET request or form validation errors

    print("Rendering entrenandoRF.html template")
    return render(request, 'entrenandoRF.html', {'form': form})


def entrenandoRF_exitoso(request):
    print("Entering entrenandoRF_exitoso view function")
    print("Request object:", request)
    print("About to return HTTP response with message 'Entrenamiento exitoso'")
    
    # Debugging statement: Print the current date and time
    import datetime
    print("Current date and time:", datetime.datetime.now())

    # Debugging statement: Print the contents of the request object
    print("Request object contents:")
    for key, value in request.__dict__.items():
        print("\t", key, ":", value)

    # Return the HTTP response
    print("Returning HTTP response with message 'Entrenamiento exitoso'")
    
    return entrenando(request)


def reconocer(request):
    print("Entering reconocer view function")

    print("Rendering reconoceRostros.html template")
    # Renderiza la plantilla reconoceRostros.html
    return render(request, 'reconoceRostros.html')
def capturar_rostros_exitoso(request, cedula, nombre, apellido):
    if request.method == 'POST':
        form = PersonaForm(request.POST)
        if form.is_valid():
            # Obtener los datos del formulario
            cedula = form.cleaned_data['CEDULA']
            nombre = form.cleaned_data['NOMBRE']
            apellido = form.cleaned_data['APELLIDO']
            print("Procesando solicitud de captura de rostros exitosa...")

            # Obtener la lista de nombres de archivo de las imágenes en la carpeta de la persona
            file_names = [f'rostro_{i}.jpg' for i in range(299)]  # Lista de nombres de archivo de 0 a 299
            print("Nombres de archivos:", file_names)

            # Definir la ruta de la carpeta de la persona (person_folder_path)
            person_folder_path = os.path.join(data_path, cedula, nombre, apellido)
            print("Ruta de la carpeta de la persona:", person_folder_path)

            # Pasar las variables al contexto del template
            context = {
                'file_names': file_names,
                'person_folder_path': person_folder_path,
            }

            return render(request, 'capturar_rostros_exitoso.html', context)

    # Si llegamos aquí, significa que el formulario no es válido o estamos en una solicitud GET
    # En cualquiera de los casos, renderizamos la plantilla capturar_rostros_exitoso.html
    return render(request, 'capturar_rostros_exitoso.html')
