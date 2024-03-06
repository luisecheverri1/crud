
from django.http import HttpResponse
from django.shortcuts import render, redirect
from reconfacial1.borrar_datos_xml import borrar_datos_xml
from reconfacial1.capturandoRostros import  capturar_rostros3
from reconfacial1.forms import PersonaForm
from reconfacial1.entrenandoRF import entrenando
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
           
            # Llamar a capturar_rostros3 con los datos del formulario
            cedula, nombre, apellido = capturar_rostros3(cedula,nombre,apellido) 
            
            # Redirigir a una página de éxito
            return redirect('reconfacial1:capturar_rostros_exitoso',cedula=cedula,nombre=nombre,apellido=apellido)
    else:
        form = PersonaForm()
    return render(request, 'capturaRostros.html', {'form': form})


# En la vista capturar_rostros_exitoso
def capturar_rostros_exitoso(request, cedula, nombre, apellido):
    # Resto del código...

    # Obtener la lista de nombres de archivo de las imágenes en la carpeta de la persona
    file_names = [f'rostro_{i}.jpg' for i in range(5)]  # Lista de nombres de archivo de 0 a 4

    # Definir la ruta de la carpeta de la persona (person_folder_path)
    person_folder_path = os.path.join(data_path, cedula, nombre, apellido)

    # Pasar las variables al contexto del template
    context = {
        'file_names': file_names,
        'person_folder_path': person_folder_path,
    }

    # Renderizar la plantilla con el contexto
    return render(request, 'capturar_rostros_exitoso.html', context)

     
def entrenandoRF(request):
    if request.method == 'POST':
        # Suponiendo que obtienes los datos de CEDULA, NOMBRE y APELLIDO de algún formulario
        cedula = request.POST.get('CEDULA')
        nombre = request.POST.get('NOMBRE')
        apellido = request.POST.get('APELLIDO')

        # Llama a la función 'entrenando' con los datos obtenidos
        cedula, nombre, apellido = entrenando(cedula,nombre,apellido) 

        # Si deseas redirigir a otra página después de que se complete el entrenamiento,
        # puedes hacerlo aquí, por ejemplo:
        return render(request, 'entrenamiento_exitoso.html')

    elif request.method == 'GET':
        # Si se recibe una solicitud GET, simplemente renderiza la plantilla entrenandoRF.html
        return render(request, 'entrenandoRF.html')

    else:
        # Si se recibe una solicitud con un método diferente a GET o POST, devuelve un mensaje de error
        return HttpResponse("Error: Método de solicitud no válido.")



def reconocer(request):
    return render(request,'reconoceRostros.html')
pass

def llamar_borrar_datos_xml(request):
    # Llamar a la función para borrar los datos del archivo XML
    archivo_xml='modeloFisherFace.xml'
    borrar_datos_xml(archivo_xml)

    return HttpResponse('Datos del archivo XML eliminados correctamente.')