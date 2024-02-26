


import os
from django.http import HttpResponse
from django.shortcuts import render, redirect
from reconfacial1.borrar_datos_xml import borrar_datos_xml
from reconfacial1.capturandoRostros import  capturar_rostros3
from reconfacial1.forms import PersonaForm
from reconfacial1.entrenandoRF import entrenando

data_path = 'C:/Users/PC/Desktop/facialPython/data' 
# Create your views here.

def home(request):
    return render(request, 'home.html')

def capturar_rostros(request):
    data_path = 'C:/Users/PC/Desktop/biometrikAss/biometrikAssProject/data'  # Ruta donde se guardarán las fotos
    if request.method == 'POST':
        form = PersonaForm(request.POST)
        if form.is_valid():
            # Obtener los datos del formulario
            nombre = form.cleaned_data['NOMBRE']
            apellido = form.cleaned_data['APELLIDO']
            cedula = form.cleaned_data['CEDULA']
            # Llamar a capturar_rostros3 con los datos del formulario
            photo_path, cedula, nombre, apellido = capturar_rostros3(data_path, cedula,  nombre, apellido) 
            # Llamar al entrenamiento después de la captura
           
            entrenando(photo_path, cedula, nombre, apellido)
            # Redirigir a una página de éxito
            return redirect('reconfacial1:capturar_rostros_exitoso')
    else:
        form = PersonaForm()
    return render(request, 'capturaRostros.html', {'form': form})


def capturar_rostros_exitoso(request):
    return render(request, 'capturar_rostros_exitoso.html')
  
#def entrenandoRF(photo_path, cedula, nombre, apellido):
 #    entrenando(photo_path, cedula, nombre, apellido)
 #  return redirect('reconfacial1:entrenamiento_exitoso')


def reconocer(request):
    return render(request,'reconoceRostros.html')
pass

def llamar_borrar_datos_xml(request):
    # Llamar a la función para borrar los datos del archivo XML
    archivo_xml='modeloFisherFace.xml'
    borrar_datos_xml(archivo_xml)

    return HttpResponse('Datos del archivo XML eliminados correctamente.')