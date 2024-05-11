
# Standard library imports
from concurrent.futures import ThreadPoolExecutor
import json
from multiprocessing import context
import threading
from urllib import request
from urllib.parse import quote
import os

# Third party imports
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.views import LoginView
from django.views import View
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError


# Local application imports
from .capturandoRostros import capturar_rostros3
from .entrenando import entrenando
from .reconocimientoFacial import reconocer_rostros
from .models import Persona, ReconocimientoFacial
from .forms import PersonaForm

import time

# Constants
DATA_PATH = 'C:/xampp/htdocs/crud/biometrikAssProject/data'

def home(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        cedula = request.POST.get('cedula')
        if action == 'actualizar_persona':
            return redirect('reconfacial1:actualizar_persona', cedula=cedula)
        elif action == 'eliminar_persona':
            return redirect('reconfacial1:eliminar_persona', cedula=cedula)
    return render(request, 'home.html')

def capturar_rostros(request):
    """Handle the form for capturing faces."""
    if request.method == 'POST':
        form = PersonaForm(request.POST, request.FILES)
        if form.is_valid():
            cedula = form.cleaned_data['cedula']
            if Persona.objects.filter(cedula=cedula).exists():
                form.add_error('cedula', 'La persona con la CEDULA introducida, YA EXISTE en la base de datos.')
            else:
                persona = form.save(commit=False)

                # Call the 'capturar_rostros3' function
                cedula, nombre, apellido, photo_path, person_folder_path, count = capturar_rostros3(
                    persona.cedula, persona.nombre, persona.apellido, persona.photo_path, persona.person_folder_path, persona.count)

                # Save the photo path in the database
                persona.photo_path = photo_path
                persona.save()

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
            entrenando(request, cedula, nombre, apellido, photo_path, person_folder_path, count)
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
            #persona = form.save()

            # Call the 'entrenando' function with the form data
            print("Calling entrenando function")
            entrenando(request, cedula, nombre, apellido, photo_path, person_folder_path, count)

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
    return render(request, 'entrenandoRF.html', {
        'cedula': cedula,
        'nombre': nombre,
        'apellido': apellido,
        'photo_path': photo_path,
        'person_folder_path': person_folder_path,
        'count': count,
    })


def entrenandoRF_exitoso(request, cedula, nombre, apellido, photo_path, person_folder_path, count):
    """Handle the form after training the facial recognition model."""
    print("HTTP method is POST")
    print("nombre:", nombre)
    print("apellido:", apellido)
    print("cedula:", cedula)
    print("photo_path:", photo_path)
    print("count:", count)
    return render(request, 'entrenamiento_exitoso.html', {'cedula': cedula, 'nombre': nombre, 'apellido': apellido,
                                                          'photo_path': photo_path, 'person_folder_path': person_folder_path, 'count': count})




from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(max_workers=1)

def reconocerhtml(request):
    return render(request, 'reconoceRostros.html')

def reconociendo(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'reconocer_rostros':
            future = executor.submit(reconocer_rostros, request)
            response = future.result()  # Asume que la función `reconocer_rostros` devuelve una respuesta JSON

            # Convertir la respuesta JSON en un diccionario
            data = json.loads(response.content)
            
            nombre = data['nombre']
            apellido = data['apellido']

            if nombre and apellido:
                return redirect('reconfacial1:bienvenido', nombre=nombre, apellido=apellido)

        else:
            nombre, apellido = None, None  # Si no se está realizando el reconocimiento facial, establece `nombre` y `apellido` en None

        return render(request, 'reconociendo.html', {'nombre': nombre, 'apellido': apellido})


def bienvenido(request, nombre, apellido):
    persona = Persona.objects.filter(nombre=nombre, apellido=apellido).first()
    return render(request, 'bienvenido.html', {'nombre': nombre, 'apellido': apellido})


def persona_list(request):
    personas = Persona.objects.all()
    return render(request, 'persona_list.html', {'personas': personas})



# Read
def leer_persona(request, cedula):
    try:
        persona = Persona.objects.get(cedula=cedula)
    except ObjectDoesNotExist:
        messages.error(request, 'La persona con la CEDULA introducida, NO EXISTE en la base de datos.')
        return redirect('reconfacial1:persona_list')
    return render(request, 'persona_detail.html', {'persona': persona})

# Update
def actualizar_persona(request, cedula):
    try:
        persona = Persona.objects.get(cedula=cedula)
    except ObjectDoesNotExist:
        messages.error(request, 'La persona con la CEDULA introducida, NO EXISTE en la base de datos.')
        return redirect('reconfacial1:persona_list')
    if request.method == "POST":
        form = PersonaForm(request.POST, instance=persona)
        if form.is_valid():
            # Guarda los datos del formulario en la instancia de Persona y sobrescribe los valores existentes
            persona = form.save(commit=False)
            # Puedes hacer cualquier modificación adicional aquí antes de guardar la instancia de Persona
            persona.save()
            return redirect('reconfacial1:leer_persona', cedula=persona.cedula)
    else:
        form = PersonaForm(instance=persona)
    return render(request, 'persona_edit.html', {'form': form})


# Delete
def eliminar_persona(request, cedula):
    persona = get_object_or_404(Persona, cedula=cedula)
    if request.method == 'POST':
        # Construye la ruta al archivo
        file_path = os.path.join('C:', 'xampp', 'data', 'crud1', f'{persona.cedula}.jpg')  # Asegúrate de que esta ruta sea correcta

        # Verifica que el archivo exista antes de intentar eliminarlo
        if os.path.isfile(file_path):
            os.remove(file_path)
        else:
            print(f"Error: {file_path} file not found")

        persona.delete()
        return redirect('reconfacial1:persona_list')
    return render(request, 'persona_confirm_delete.html', {'persona': persona})

class MyLoginView(LoginView):
    template_name = 'home.html'


class ProfileView(View):
    def get(self, request):
        # Aquí va tu lógica para la vista
        return render(request, 'home.html')   

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('reconfacial1:administrador')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    return render(request, 'login_view.html')

@login_required
def admin_view(request):
    return render(request, 'admin.html')