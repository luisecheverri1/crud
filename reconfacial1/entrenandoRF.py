import cv2
import os
import numpy as np

# Directorio donde se almacenan las imágenes de entrenamiento
data_path = 'C:/xampp/htdocs/crud-1/biometrikAssProject/data'

def entrenando(cedula, nombre, apellido):
    print("Iniciando el proceso de entrenamiento...")

    # Listar las personas en el directorio de datos
    people_list = os.listdir(data_path)
    print("Lista de personas:", people_list)
    
    # Verificar que haya al menos dos personas antes de continuar
    if len(people_list) < 2:
        print("Error: Se necesitan al menos dos personas para entrenar el modelo.")
        return
    
    # Crear listas para almacenar etiquetas y datos de rostros
    labels = []
    faces_data = []
    label = 0
    
    # Iterar sobre cada persona en el directorio de datos
    for name_dir in people_list:
        person_path = os.path.join(data_path, name_dir)
        print('Leyendo las imágenes de:', person_path)
        
        # Iterar sobre cada archivo de imagen en la carpeta de la persona
        for file_name in os.listdir(person_path):
            # Leer la imagen en escala de grises
            image_path = os.path.join(person_path, file_name)
            image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            
            # Agregar la imagen a la lista de datos de rostros y la etiqueta correspondiente a la lista de etiquetas
            faces_data.append(image)
            labels.append(label)
        
        # Incrementar la etiqueta para la siguiente persona
        label += 1
    
    # Verificar que haya al menos una muestra de cada persona
    if len(labels) < 2:
        print("Error: Se necesitan al menos dos personas con muestras de entrenamiento.")
        return
    
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

    return None  # Agrega esta línea para devolver None al final de la función
