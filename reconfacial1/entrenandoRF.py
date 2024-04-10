import numpy as np
import cv2
import os
from django.http import HttpResponse
import urllib.parse

def entrenando(request, cedula, nombre, apellido, photo_path, person_folder_path):
    data_path = 'C:/xampp/htdocs/crud-1/biometrikAssProject/data'
    print(f"data_path: {data_path}")  # Imprimir data_path

    if cedula is not None:
        print("Iniciando el proceso de entrenamiento...")
        
        print(f"photo_path antes de decodificar: {photo_path}")  # Imprimir photo_path antes de decodificar

        photo_path = urllib.parse.unquote(photo_path)
        print(f"photo_path después de decodificar: {photo_path}")  # Imprimir photo_path después de decodificar

        photo_dir = os.path.dirname(photo_path)
        print(f"photo_dir: {photo_dir}")  # Imprimir photo_dir

        people_list = os.listdir(data_path)
        print(f"people_list: {people_list}")  # Imprimir people_list

        labels = []
        faces_data = []
        label = 0
        print(f"labels: {labels}") 
        print(f"faces_data: {faces_data}") 
        print(f"label: {label}") 

        # Obtener la lista de directorios en data_path
        people_dirs = [os.path.join(data_path, d) for d in os.listdir(data_path) if os.path.isdir(os.path.join(data_path, d))]
        print(f"people_dirs: {people_dirs}")  # Imprimir people_dirs

        # Ordenar los directorios por fecha de modificación
        people_dirs.sort(key=lambda x: os.path.getmtime(x), reverse=True)

        # Inicializar la lista de los dos últimos directorios de personas
        last_two_people_dirs = []

      # Recorrer los directorios en orden de modificación
        for person_dir in people_dirs:
            # Verificar si el directorio contiene al menos una imagen de rostro
            if any(os.path.isfile(os.path.join(person_dir, nombre, apellido, f'rostro_{i}.jpg')) for i in range(30)):
                # Añadir el directorio a la lista
                last_two_people_dirs.append(person_dir)

                # Si ya se han añadido dos directorios, salir del bucle
                if len(last_two_people_dirs) == 2:
                    break

        # Verificar que se encontraron dos directorios
        if len(last_two_people_dirs) != 2:
            print("Error: No se encontraron dos directorios con imágenes de rostros.")
            return

        # Agregar nombre y apellido a cada directorio de cédula
        last_two_people_dirs = [os.path.join(dir, nombre, apellido) for dir in last_two_people_dirs]

        print(f"last_two_people_dirs: {last_two_people_dirs}")  # Imprimir last_two_people_dirs
        
        for person_dir in last_two_people_dirs:
            # Obtener las partes de la ruta del directorio
            path_parts = os.path.normpath(person_dir).split(os.sep)
            print(f"path_parts: {path_parts}")  # Imprimir path_parts

            # Asegurarse de que la ruta del directorio tiene al menos cuatro partes
            if len(path_parts) < 4:
                print(f"La ruta del directorio {person_dir} no tiene suficientes partes. Saltando este directorio.")
                continue

            # Desempaquetar las partes de la ruta del directorio
            _, cedula, nombre, apellido = path_parts[-4:]

            print(f"person_dir: {person_dir}")  # Imprimir person_dir

            for count in range(30):
                photo_path = os.path.join(person_dir, f'rostro_{count}.jpg')
                print(f"photo_path: {photo_path}")  # Imprimir image_path

                if not os.path.isfile(photo_path):
                    print(f"El archivo no existe: {photo_path}")
                    continue

                image = cv2.imread(photo_path, cv2.IMREAD_GRAYSCALE)
                if image is None:
                    print(f"Error: No se pudo leer la imagen {photo_path}")
                    continue

                print(f"Dimensiones de la imagen: {image.shape}")
                print(f"Tipo de datos de la imagen: {image.dtype}")

                faces_data.append(image)
                labels.append(label)

            label += 1

        # Verificar que haya al menos una muestra de cada persona
        if len(labels) < 2 or len(faces_data) < 2:
            print("Error: Se necesitan al menos dos personas con muestras de entrenamiento.")
            return HttpResponse("Insufficient training data", status=400)  # Example response for insufficient data

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