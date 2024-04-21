import os
import urllib

import cv2
from django.http import HttpResponse
import numpy as np


def entrenando(request, cedula, nombre, apellido, photo_path, person_folder_path,count):
    print("Iniciando la función de entrenando...")
    
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

        print(f"people_dirs: {people_dirs}")  # Imprimir people_dirs
        
        for person_dir in people_dirs:
            # Obtener la lista de subdirectorios en person_dir
            subdirs = [os.path.join(person_dir, sd) for sd in os.listdir(person_dir) if os.path.isdir(os.path.join(person_dir, sd))]

            # Recorrer cada subdirectorio
            for subdir in subdirs:
                # Obtener la lista de sub-subdirectorios en subdir
                subsubdirs = [os.path.join(subdir, ssd) for ssd in os.listdir(subdir) if os.path.isdir(os.path.join(subdir, ssd))]

                # Recorrer cada sub-subdirectorio
                for subsubdir in subsubdirs:
                    # Obtener las partes de la ruta del directorio
                    path_parts = os.path.normpath(subsubdir).split(os.sep)
                    print(f"path_parts: {path_parts}")  # Imprimir path_parts

                    # Asegurarse de que la ruta del directorio tiene al menos cinco partes
                    if len(path_parts) < 5:
                        print(f"La ruta del directorio {subsubdir} no tiene suficientes partes. Saltando este directorio.")
                        continue

                    # Desempaquetar las partes de la ruta del directorio
                    _, _, cedula, nombre, apellido = path_parts[-5:]

                    print(f"subsubdir: {subsubdir}")  # Imprimir subsubdir

                    for count in range(30):
                        photo_path = os.path.join(subsubdir, f'rostro_{count}.jpg')
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
        print("Saliendo de la función de entrenando...hacia entrenandoRF")
        return HttpResponse("Training process completed successfully")  # Example response    
    else:  
        print("Rendering entrenandoRF.html template")
        return (request,cedula, nombre, apellido, photo_path,person_folder_path, count)