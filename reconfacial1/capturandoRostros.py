import os
import cv2
from django.shortcuts import redirect, render
from reconfacial1.forms import PersonaForm


data_path = 'C:/Users/PC/Desktop/biometrikAss/biometrikAssProject/data'  # Ruta donde se guardarán las fotos

def capturar_rostros3(data_path, CEDULA, NOMBRE, APELLIDO,  count_limit=5):
    person_folder_path = os.path.join(data_path, CEDULA, NOMBRE, APELLIDO, )
    os.makedirs(person_folder_path, exist_ok=True)  # Asegurar que la carpeta de la persona esté creada
    
    cap = cv2.VideoCapture(0)  # Inicializar la cámara
    if not cap.isOpened():
        print("Error: No se puede abrir la cámara.")
        return

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    count = 0
    while count < count_limit:
        ret, frame = cap.read()
        if not ret:
            print("Error: No se puede leer el fotograma.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        if len(faces) == 0:
            print("No se detectaron rostros en el fotograma.")
            continue

        for (x, y, w, h) in faces:
            face_roi = frame[y:y+h, x:x+w]
            face_roi_resized = cv2.resize(face_roi, (150, 150), interpolation=cv2.INTER_AREA)

            if face_roi_resized is not None:
                # Guardar el rostro en la carpeta de la persona
                photo_path = os.path.join(person_folder_path, f'rostro_{count}.jpg')
                cv2.imwrite(photo_path, face_roi_resized)
                print(f"Rostro capturado y guardado en: {photo_path}")
                count += 1

            if count >= count_limit:
                break

        cv2.imshow('Captura de rostros', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

