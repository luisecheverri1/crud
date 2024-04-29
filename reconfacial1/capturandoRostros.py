import os
import shutil
import time
import cv2

from reconfacial1.models import Foto, Persona
from django.db import IntegrityError

data_path = "C:/xampp/htdocs/crud-1/biometrikAssProject/data"

def capturar_rostros3(cedula, nombre, apellido, photo_path, person_folder_path, count, count_limit=5):
    """
    Captures multiple faces using the camera and saves them as images.

    Args:
        cedula (str): The ID number of the person.
        nombre (str): The first name of the person.
        apellido (str): The last name of the person.
        photo_path (str): The path where the captured face images will be saved.
        person_folder_path (str): The path of the folder where the person's images will be stored.
        count (int): The current count of captured faces.
        count_limit (int, optional): The maximum number of faces to capture. Defaults to 5.

    Returns:
        tuple: A tuple containing the cedula, nombre, apellido, photo_path, person_folder_path, and count.

    Raises:
        None

    """

    # Get or create the Persona instance
    persona, created = Persona.objects.get_or_create(cedula=cedula, nombre=nombre, apellido=apellido)
    
    person_folder_path = os.path.join(data_path, cedula, nombre, apellido)
    os.makedirs(person_folder_path)

    cap = cv2.VideoCapture(0)  # Prueba con índice 0  
    if not cap.isOpened():
        cap = cv2.VideoCapture(1)  # Si no funciona, prueba con índice 1
        
    if not cap.isOpened():
        print("Error: No se puede abrir la cámara.Esperando...")
        time.sleep(2)
        return capturar_rostros3(cedula, nombre, apellido,count)   
    else:
        print("¡Cámara abierta correctamente!")

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    #Crear ventana con tamano ajustable
    cv2.namedWindow('Captura de rostros', cv2.WINDOW_NORMAL)  

    ret, frame = cap.read()  # Capturar el frame actual de la cámara
    if ret:  # Si se capturó el frame correctamente...
        #Mostrar el frame
        cv2.imshow('Captura de rostros', frame)
 
    while count < count_limit:
        ret, frame = cap.read()
        if not ret:
            print("Error: No se puede leer el fotograma.")
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        # Establecer el tamaño de la ventana
        cv2.resizeWindow('Captura de rostros', 800, 600) 

        # Mover la ventana a una ubicación específica
        cv2.moveWindow('Captura de rostros', 100, 100)  # Mueve la ventana a la posición (x, y) = (100, 100)

        if len(faces) == 0:
            print("No se detectaron rostros en el fotograma.")
            continue

        for (x, y, w, h) in faces:
            # Dibujar un rectángulo verde alrededor del rostro detectado
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

            face_roi = frame[y:y+h, x:x+w]
            face_roi_resized = cv2.resize(face_roi, (150, 150), interpolation=cv2.INTER_AREA)

            if face_roi_resized is not None:
                photo_path = os.path.join(person_folder_path, f'rostro_{count}.jpg')
                cv2.imwrite(photo_path, face_roi_resized)
                print(f"Rostro capturado y guardado en: {photo_path}")


                # Save the photo_path in the database
                foto = Foto(persona=persona, photo_path=photo_path)
                foto.save()

                count += 1
                print(f"Contador de rostros incrementado a: {count}")  # Imprimir el valor de count después de cada incremento
            if count >= count_limit:
                break

        
        #cv2.resizeWindow('Captura de rostros', 800, 600)  # Ajusta el tamaño de la ventana
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    # Save the Persona in the database
    #persona = Persona(cedula=cedula, nombre=nombre, apellido=apellido, photo_path=photo_path)
    #persona.save() 
    
    # Asegúrate de que photo_path se define antes de intentar devolverlo
    #photo_path = "algún valor"
    return (cedula,nombre,apellido,photo_path,person_folder_path,count)

