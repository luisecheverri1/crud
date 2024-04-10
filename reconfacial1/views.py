

from urllib import request
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from reconfacial1.models import Persona
from reconfacial1.forms import PersonaForm
from .capturandoRostros import capturar_rostros3
from .entrenandoRF import entrenando
import os
from urllib.parse import quote


data_path = 'C:/xampp/htdocs/crud/biometrikAssProject/data' 
# Create your views here.


def home(request):
    persona = Persona.objects.first()
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
            cedula = form.cleaned_data['cedula']
            nombre = form.cleaned_data['nombre']
            apellido = form.cleaned_data['apellido']
           
            print("Datos del formulario:", cedula, nombre, apellido)

            #Captura photo_path cuando llamas a capturar_rostros3
            cedula, nombre, apellido, photo_path, person_folder_path, count = capturar_rostros3(cedula, nombre, apellido,count=0)

               # Codifica photo_path para que sea seguro usarlo en una URL
            photo_path = quote(photo_path.encode())
            redirect_url = reverse('reconfacial1:capturar_rostros_exitoso', args=[cedula, nombre, apellido, photo_path,count])
           

            print("Redirecting to capturar_rostros_exitoso")
            return HttpResponseRedirect(redirect_url)
             
        else:
            print("Form is not valid")
            print(form.errors)
    else:
        print("HTTP method is not POST")
        form = PersonaForm()
        print("Rendering capturaRostros.html template")

    print("Leaving capturar_rostros view function")

    return render(request, 'capturaRostros.html', {'form': form})


# En la vista capturar_rostros_exitoso
def capturar_rostros_exitoso(request, cedula='', nombre='', apellido='', photo_path='',count=''):
    print("Entering capturar_rostros_exitoso view function")
    print("Request method:", request.method)
    print(f"cedula: {cedula}")
    print(f"nombre: {nombre}")
    print(f"apellido: {apellido}")
    print(f"photo_path: {photo_path}")


    # Define file_names and person_folder_path here
    file_names = [f'rostro_{i}.jpg' for i in range(299)]  # Lista de nombres de archivo de 0 a 299
    count = len(file_names)  # Calcula el número de archivos
    person_folder_path = os.path.join(data_path,str(cedula), nombre, apellido)


    # Define context here
    
    #photo_path = quote(photo_path)
    context = {'file_names': file_names,
                'person_folder_path': person_folder_path,
                'cedula': cedula,
                'nombre': nombre,
                'apellido': apellido,
                'photo_path': photo_path,
                'count': count,
                }

    if request.method == 'POST':
        form = PersonaForm(request.POST)
        if form.is_valid():
            print("Form is valid")
            cedula = form.cleaned_data['cedula']
            nombre = form.cleaned_data['nombre']
            apellido = form.cleaned_data['apellido']
            photo_path = form.cleaned_data['photo_path']
            print("Datos del formulario:", cedula, nombre, apellido)

            # Obtener la lista de nombres de archivo de las imágenes en la carpeta de la persona
            print("Nombres de archivos:", file_names)

            # Definir la ruta de la carpeta de la persona (person_folder_path)
            print("Ruta de la carpeta de la persona:", person_folder_path)

            context = {
                'file_names': file_names,
                'person_folder_path': person_folder_path,
                'cedula': cedula,
                'nombre': nombre,
                'apellido': apellido,
                'photo_path': photo_path,
            }

            print("Redirecting to entrenandoRF")
            return redirect('reconfacial1:entrenandoRF', cedula=cedula, nombre=nombre, apellido=apellido, photo_path=photo_path,count=count)

    print("Rendering capturar_rostros_exitoso.html template")
    return render(request, 'capturar_rostros_exitoso.html', context)


def entrenandoRF(request,nombre ,apellido, cedula, photo_path, count):
    print("Entering entrenandoRF view function")
    print("Request method:", request.method)
    print("POST data:", request.POST)

    if request.method == 'POST':
  
        print("HTTP method is POST")
        form = PersonaForm(request.POST)
        if form.is_valid():
            print("Form is valid")
            persona = form.save()
            # Call the 'entrenando' function with the form data
            entrenando(request, cedula, nombre, apellido, photo_path, count)

            print("Redirecting to entrenandoRF_exitoso")
            #return HttpResponse(resultado_entrenamiento)  # Render the training result
            return redirect('reconfacial1:entrenandoRF_exitoso', cedula=cedula, nombre=nombre, apellido=apellido, photo_path=photo_path, count=count)
        else:
            print("Form is not valid")
            print("Form errors:", form.errors)
    else:
        print("HTTP method is not POST")
        form = PersonaForm()  # Create a form instance for GET request or form validation errors

    print("Rendering entrenandoRF.html template")
    return render(request,cedula, nombre, apellido, photo_path, count, 'entrenandoRF.html', {'form': form})


def entrenandoRF_exitoso(request,nombre ,apellido, cedula, photo_path, count):
    print("Entering entrenandoRF_exitoso view function")
    print("Request object:", request)
    print("About to return HTTP response with message 'Entrenamiento exitoso'")
    
    if request.method == 'POST':
       pass 
    else:
        # Añade una respuesta para el caso GET
        return HttpResponse('Esta vista solo acepta peticiones POST.')    
        # Debugging statement: Print the current date and time
    import datetime
    print("Current date and time:", datetime.datetime.now())

    # Debugging statement: Print the contents of the request object
    print("Request object contents:")
    for key, value in request.__dict__.copy().items():
        print("\t", key, ":", value)

    # Return the HTTP response{% url 'entrenandoRF' cedula=cedula nombre=nombre apellido=apellido photo_path=photo_path %}
    print("Returning HTTP response with message 'Entrenamiento exitoso'")
    
    # Redirect to the 'reconocer' view
    return render(request, 'reconoceRostros.html',{
        'cedula': cedula,
        'nombre': nombre,
        'apellido': apellido,
        'photo_path': photo_path,
        'count': count,
    })

def reconocer(request,cedula, nombre, apellido, photo_path, count):
    print("Entering reconocer view function")
    if request.method == 'POST':
            print("Rendering reconoceRostros.html template")
            # Renderiza la plantilla reconoceRostros.html
            return render(request,cedula, nombre, apellido, photo_path, count, 'reconoceRostros.html')



