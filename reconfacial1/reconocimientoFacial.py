import os
import cv2
import time
from django.http import HttpResponse

def reconocer_rostros(request):
    
    dataPath = 'C:/xampp/htdocs/crud-1/biometrikAssProject/data'
    imagePaths = os.listdir(dataPath)
    print('imagePaths=',imagePaths)
    
    # Obtener la lista de directorios en data_path
    people_dirs = [os.path.join(dataPath, d) for d in os.listdir(dataPath) if os.path.isdir(os.path.join(dataPath, d))]

    # Extraer los nombres y apellidos de los directorios
    nombres_apellidos = {}
    for d in people_dirs:
        cedula = os.path.basename(d)
        nombre_dirs = [os.path.join(d, sd) for sd in os.listdir(d) if os.path.isdir(os.path.join(d, sd))]
        for nd in nombre_dirs:
            nombre = os.path.basename(nd)
            apellido_dirs = [os.path.join(nd, sd) for sd in os.listdir(nd) if os.path.isdir(os.path.join(nd, sd))]
            for ad in apellido_dirs:
                apellido = os.path.basename(ad)
                nombres_apellidos[cedula] = (nombre, apellido)

    print(f"nombres_apellidos: {nombres_apellidos}")  # Imprimir nombres_apellidos

    face_recognizer = cv2.face.FisherFaceRecognizer_create()
    face_recognizer.read('modeloFisherFace.xml')

    cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
    cv2.namedWindow('frame', cv2.WINDOW_NORMAL)

    faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')

    counter = 0
    cedula_counts = {}  # Diccionario para contar las apariciones de cada cédula

 

    while counter < 100:
        ret,frame = cap.read()
        if ret == False: break    
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        auxFrame = gray.copy()
        
        time.sleep(0.001)  # Pausar durante  segundos

        faces = faceClassif.detectMultiScale(gray,1.3,5)
        print(f"faces: {faces}")  # Imprimir las caras detectadas

        for (x,y,w,h) in faces:
            rostro = auxFrame[y:y+h,x:x+w]
            rostro = cv2.resize(rostro,(150,150),interpolation= cv2.INTER_CUBIC)
            result = face_recognizer.predict(rostro)
            print(f"result: {result}")  # Imprimir el resultado de la predicción

            if result[1] < 1700:
                # Convertir nombres_apellidos en una lista de cédulas
                cedulas = list(nombres_apellidos.keys())

                # Usar result[0] para indexar la lista de cédulas
                cedula = cedulas[result[0]]
                print(f"cedula: {cedula}")  # Imprimir la cédula
                cedula_counts[cedula] = cedula_counts.get(cedula, 0) + 1  # Incrementar el conteo para esta cédula

                nombre, apellido = nombres_apellidos[cedula]

                print(f"Reconocido: {nombre} {apellido}")  # Imprimir el nombre y apellido reconocidos

                counter += 1  # Incrementar el contador solo si se detecta un rostro

            if counter >= 100:
                break
        
    # Encontrar la cédula que apareció con más frecuencia
    most_common_cedula = max(cedula_counts, key=cedula_counts.get)

    # Buscar el nombre y apellido que corresponden a la cédula más encontrada
    nombre, apellido = nombres_apellidos[most_common_cedula]

    # Obtener el número de veces que se reconoció la cédula más común
    num_recognitions = cedula_counts[most_common_cedula]

    print(f"CEDULA MAS COMUN: {most_common_cedula}")
    print(f"RECONOCIDO: {nombre} {apellido}")
    print(f"PORCENTAJE DE RECONOCIMIENTOS: {num_recognitions} %")
    cap.release()
    cv2.destroyAllWindows()

    return HttpResponse("Face recognition started.")