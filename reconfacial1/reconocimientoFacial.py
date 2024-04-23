import os
import cv2
import time
from django.http import HttpResponse

def reconocer_rostros(request):
    
    dataPath = 'C:/xampp/htdocs/crud-1/biometrikAssProject/data'
    imagePaths = os.listdir(dataPath)
    print('imagePaths=',imagePaths)
    
    people_dirs = [os.path.join(dataPath, d) for d in os.listdir(dataPath) if os.path.isdir(os.path.join(dataPath, d))]

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

    print(f"nombres_apellidos: {nombres_apellidos}")

    face_recognizer = cv2.face.LBPHFaceRecognizer_create()
    face_recognizer.read('modeloLBPHFace.xml')

    cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
    cv2.namedWindow('frame', cv2.WINDOW_NORMAL)

    faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')

    counter = 0
    cedula_counts = {}

    while counter < 100:
        ret,frame = cap.read()
        
        if ret == False: break    
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        auxFrame = gray.copy()
        
        time.sleep(0.001)
        
        faces = faceClassif.detectMultiScale(gray,1.3,5)

        for (x,y,w,h) in faces:
            rostro = auxFrame[y:y+h,x:x+w]
            rostro = cv2.resize(rostro,(150,150),interpolation= cv2.INTER_CUBIC)
            result = face_recognizer.predict(rostro)

            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.imshow('frame', frame)
            cv2.waitKey(1)  # Agregar esta línea  


            if result[1] < 1700:
                cedulas = list(nombres_apellidos.keys())
                cedula = cedulas[result[0]]
                print(f"cedula: {cedula}")
                cedula_counts[cedula] = cedula_counts.get(cedula, 0) + 1

                nombre, apellido = nombres_apellidos[cedula]

                print(f"Reconocido: {nombre} {apellido}")

                counter += 1

            if counter >= 100:
                break
   

    most_common_cedula = max(cedula_counts, key=cedula_counts.get)
    nombre, apellido = nombres_apellidos[most_common_cedula]
    num_recognitions = cedula_counts[most_common_cedula]

    print(f"CEDULA MAS COMUN: {most_common_cedula}")
    print(f"RECONOCIDO: {nombre} {apellido}")
    print(f"PORCENTAJE DE RECONOCIMIENTOS: {num_recognitions} %")
    cap.release()
    cv2.destroyAllWindows()

    return HttpResponse("Face recognition started.")