

import os
import shutil
import time
import cv2

data_path = "C:/xampp/htdocs/crud-1/biometrikAssProject/data"

def capturar_rostros3(cedula, nombre, apellido,count_limit=300):
   
    person_folder_path = os.path.join(data_path, cedula)

    if os.path.exists(person_folder_path):
        print(f"La carpeta para la cédula {cedula} ya existe. Sobrescribiendo los datos...")
        shutil.rmtree(person_folder_path)
    person_folder_path = os.path.join(data_path, cedula, nombre, apellido)
    os.makedirs(person_folder_path)

    cap = cv2.VideoCapture(0)# Prueba con índice 0  
    if not cap.isOpened():
        cap = cv2.VideoCapture(1)  # Si no funciona, prueba con índice 1
        
    if not cap.isOpened():
        print("Error: No se puede abrir la cámara.Esperando...")
        time.sleep(2)
        return capturar_rostros3( cedula, nombre, apellido,count_limit)   
    else:
        print("¡Cámara abierta correctamente!")

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    count = 0
    
    cv2.namedWindow('Captura de rostros', cv2.WINDOW_NORMAL)  # Crear una ventana con tamaño ajustable
    cv2.setWindowProperty('Captura de rostros', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)  # Maximizar la ventana

    
    
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
            # Dibujar un rectángulo verde alrededor del rostro detectado
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

            face_roi = frame[y:y+h, x:x+w]
            face_roi_resized = cv2.resize(face_roi, (150, 150), interpolation=cv2.INTER_AREA)

            if face_roi_resized is not None:
                photo_path = os.path.join(person_folder_path, f'rostro_{count}.jpg')
                cv2.imwrite(photo_path, face_roi_resized)
                print(f"Rostro capturado y guardado en: {photo_path}")
                count += 1

            if count >= count_limit:
                break

        cv2.imshow('Captura de rostros', frame)
        cv2.resizeWindow('Captura de rostros', 800, 600)  # Ajusta el tamaño de la ventana
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    
    # Asegúrate de que photo_path se define antes de intentar devolverlo
    photo_path = "algún valor"
    return (cedula,nombre,apellido,photo_path,person_folder_path,count)

# Ejemplo de cómo llamar y utilizar la función capturar_rostros3
if __name__ == "__main__":
    cedula = "123456789"
    nombre = "Juan"
    apellido = "Perez"
    resultado_captura = capturar_rostros3(cedula, nombre, apellido)
    print("Resultado de la captura:", resultado_captura)
