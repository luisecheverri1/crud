

# Standard library imports
from urllib import request
from urllib.parse import quote
import os

# Third party imports
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

# Local application imports
from .capturandoRostros import capturar_rostros3
from .entrenando import entrenando
from .reconocimientoFacial import reconocer_rostros
from reconfacial1.models import Persona
from reconfacial1.forms import PersonaForm

# Constants
DATA_PATH = 'C:/xampp/htdocs/crud/biometrikAssProject/data'


def home(request):
    """Render the home page."""
    print("Entering the home view function")
    response = render(request, 'home.html')
    print("Leaving the home view function")
    return response


def capturar_rostros(request):
    """Handle the form for capturing faces."""
    if request.method == 'POST':
        form = PersonaForm(request.POST)
        if form.is_valid():
            cedula = form.cleaned_data['cedula']
            nombre = form.cleaned_data['nombre']
            apellido = form.cleaned_data['apellido']
            count = 0  # Initialize count
            photo_path = ""  # Initialize photo_path
            person_folder_path = ""  # Initialize person_folder_path
            cedula, nombre, apellido, photo_path, person_folder_path, count = capturar_rostros3(
                cedula, nombre, apellido, photo_path, person_folder_path, count)

            # Print the variables before the redirection
            print(f"cedula: {cedula}")
            print(f"nombre: {nombre}")
            print(f"apellido: {apellido}")
            print(f"photo_path: {photo_path}")
            print(f"person_folder_path: {person_folder_path}")
            print(f"count: {count}")

            return redirect('reconfacial1:capturar_rostros_exitoso', cedula=cedula, nombre=nombre, apellido=apellido,
                            photo_path=photo_path, person_folder_path=person_folder_path, count=count )
    else:
        form = PersonaForm()
    return render(request, 'capturaRostros.html', {'form': form})


def capturar_rostros_exitoso(request, cedula, nombre, apellido, photo_path, person_folder_path, count):
    """Handle the form after capturing faces."""
    print(f"Request method: {request.method}")
    print(f"Parameters: cedula={cedula}, nombre={nombre}, apellido={apellido}, photo_path={photo_path}, "
          f"person_folder_path={person_folder_path}, count={count}")

    if request.method == 'POST':
        form = PersonaForm(request.POST)
        print(f"Form is valid: {form.is_valid()}")
        if form.is_valid():
            print("Calling entrenando()")
            entrenando()
            print("Redirecting to entrenandoRF")
            return HttpResponseRedirect(reverse('entrenandoRF', args=(nombre, apellido, cedula, photo_path,
                                                                     person_folder_path, count)))
    else:
        form = PersonaForm()
        print("Created new PersonaForm")

    print("Rendering capturar_rostros_exitoso.html")
    return render(request, 'capturar_rostros_exitoso.html', {'form': form, 'cedula': cedula, 'nombre': nombre,
                                                              'apellido': apellido, 'photo_path': photo_path,
                                                              'person_folder_path': person_folder_path, 'count': count})


def entrenandoRF(request, cedula, nombre, apellido, photo_path, person_folder_path, count):
    """Train the facial recognition model."""
    print("Entering entrenandoRF view function")
    print("Request method:", request.method)
    print("POST data:", request.POST)
    print(f"cedula: {cedula}")
    print(f"nombre: {nombre}")
    print(f"apellido: {apellido}")
    print(f"photo_path: {photo_path}")
    if request.method == 'POST':
        print("HTTP method is POST")
        form = PersonaForm(request.POST)
        if form.is_valid():
            print("Form is valid")
            persona = form.save()

            # Call the 'entrenando' function with the form data
            print("Calling entrenando function")
            entrenando(request, cedula, nombre, apellido, photo_path,person_folder_path, count)

            print("Redirecting to entrenandoRF_exitoso")
            return redirect('reconfacial1:entrenandoRF_exitoso', cedula=cedula, nombre=nombre, apellido=apellido,
                            photo_path=photo_path, person_folder_path=person_folder_path, count=count)
        
        else:
            print("Form is not valid")
            print("Form errors:", form.errors)
    else:
        print("HTTP method is not POST")
        form = PersonaForm()  # Create a form instance for GET request or form validation errors

    print("Rendering entrenandoRF.html template")
    return render(request, 'entrenandoRF.html', {'form': form})


def entrenandoRF_exitoso( request, cedula, nombre, apellido, photo_path,person_folder_path, count):
    """Handle the form after training the facial recognition model."""
    
    print("HTTP method is POST")
    print("nombre:", nombre)
    print("apellido:", apellido)
    print("cedula:", cedula)
    print("photo_path:", photo_path)
    print("count:", count)
    return redirect('reconfacial1:reconocer')



#def reconocer(request, cedula, nombre, apellido, photo_path,person_folder_path, count):
    """Recognize faces."""
    reconocer_rostros(request)  # Llama a la función de reconocimiento facial
      
    return render(request, 'reconoceRostros.html', {'cedula': cedula, 'nombre': nombre, 'apellido': apellido,
    'photo_path': photo_path, 'person_folder_path': person_folder_path, 'count': count})


def reconocer(request):
    """Recognize faces."""
    reconocer_rostros(request)  # Llama a la función de reconocimiento facial
    return render(request, 'reconoceRostros.html')