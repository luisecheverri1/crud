import numpy as np
import cv2
import os
#from django.shortcuts import render
#from reconfacial1.capturandoRostros import capturar_rostros3       
from django.http import HttpResponse
import urllib.parse
# Directorio donde se almacenan las imágenes de entrenamiento

def entrenando(request, cedula, nombre, apellido, photo_path,person_folder_path):
    
    data_path = 'C:/xampp/htdocs/crud-1/biometrikAssProject/data'
    print(f"data_path: {data_path}")  # Imprimir data_path

    if cedula is not None:
        print("Iniciando el proceso de entrenamiento...")

        photo_path = urllib.parse.unquote(photo_path)
        print(f"photo_path después de decodificar: {photo_path}")  # Imprimir photo_path después de decodificar

        photo_dir = os.path.dirname(photo_path)
        print(f"photo_dir: {photo_dir}")  # Imprimir photo_dir

        people_list = os.listdir(data_path)
        print(f"people_list: {people_list}")  # Imprimir people_list

        labels = []
        faces_data = []
        label = 0

        for name_dir in people_list:
            person_path = os.path.join(data_path, name_dir, nombre, apellido)
            print(f"person_path: {person_path}")  # Imprimir person_path

            for count in range(300):
                image_path = os.path.join(person_path, f'rostro_{count}.jpg')
                print(f"image_path: {image_path}")  # Imprimir image_path

                if not os.path.isfile(image_path):
                    print(f"El archivo no existe: {image_path}")
                    continue

                image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
                if image is None:
                    print(f"Error: No se pudo leer la imagen {image_path}")
                    continue

                print(f"Dimensiones de la imagen: {image.shape}")
                print(f"Tipo de datos de la imagen: {image.dtype}")

                faces_data.append(image)
                labels.append(label)

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






        