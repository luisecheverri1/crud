import numpy as np
import cv2
import os
#from django.shortcuts import render
#from reconfacial1.capturandoRostros import capturar_rostros3       
from django.http import HttpResponse
import urllib.parse
# Directorio donde se almacenan las imágenes de entrenamiento

def entrenando(request, cedula, nombre, apellido, photo_path,person_folder_path, count):
    data_path = 'C:/xampp/htdocs/crud-1/biometrikAssProject/data'
    # Your view logic here
    if cedula is not None:
        print("Iniciando el proceso de entrenamiento...")

         # Decodificar photo_path y obtener la ruta al directorio que contiene todas las fotos capturadas
        photo_path = urllib.parse.unquote(photo_path)
        photo_dir = os.path.dirname(photo_path)

        # Listar las personas en el directorio de datos
        people_list = os.listdir(data_path)
        print("Lista de personas:", people_list)
        
        
        # Crear listas para almacenar etiquetas y datos de rostros
        labels = []
        faces_data = []
        label = 0
        
        # Iterar sobre cada persona en el directorio de datos
        for name_dir in people_list:
            person_path = os.path.join(data_path, name_dir)
            print('Leyendo las imágenes de:', person_path)
            
           # Iterar sobre cada subcarpeta de la persona
            for subfolder in os.listdir(person_path):
                subfolder_path = os.path.join(person_path, subfolder)
                
                # Iterar sobre cada archivo de imagen en la subcarpeta
                for file_name in os.listdir(subfolder_path):
                    # Construir la ruta del archivo de la imagen
                    image_path = os.path.join(subfolder_path, file_name)

                    # Verificar que el archivo existe antes de intentar leerlo
                    if not os.path.isfile(image_path):
                        print(f"El archivo no existe: {image_path}")
                        continue

                    # Leer la imagen en escala de grises
                    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

                    # Verificar si la imagen se leyó correctamente
                    if image is None:
                        print(f"Error: No se pudo leer la imagen {image_path}")
                        continue

                    # Imprimir las dimensiones y el tipo de datos de la imagen
                    print(f"Dimensiones de la imagen: {image.shape}")
                    print(f"Tipo de datos de la imagen: {image.dtype}")

                    # Agregar la imagen a la lista de datos de rostros y la etiqueta correspondiente a la lista de etiquetas
                    faces_data.append(image)
                    labels.append(label)
            
            # Incrementar la etiqueta para la siguiente persona
            label += 1
        
        # Verificar que haya al menos una muestra de cada persona
        if len(labels) < 2:
            print("Error: Se necesitan al menos dos personas con muestras de entrenamiento.")
            
        
        # Inicializar el reconocedor de rostros
        face_recognizer = cv2.face.FisherFaceRecognizer_create()
        
        # Entrenar el reconocedor de rostros con los datos recopilados
        print("Entrenando el reconocedor de rostros...")
        face_recognizer.train(faces_data, np.array(labels))
        print("Entrenamiento completado.")
        
        # Crear la ruta del archivo XML para guardar el modelo entrenado
        model_path = os.path.join('C:/xampp/htdocs/crud-1/', 'modeloFisherFace.xml')
        
        # Escribir el modelo entrenado en el archivo XML
        face_recognizer.write(model_path)
        print(f"Modelo entrenado almacenado en {model_path}")

        return HttpResponse("Training process completed successfully")  # Example response
    else:
        # Handle GET requests or other cases if needed
        return HttpResponse("Method not allowed", status=405)  # Example response for other cases






        