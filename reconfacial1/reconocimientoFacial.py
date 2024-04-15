from django.http import HttpResponse
import cv2
import os
import threading

def reconocer_rostros(request):
    def run():
        dataPath = 'C:/xampp/htdocs/crud-1/biometrikAssProject/data'
        imagePaths = os.listdir(dataPath)
        print('imagePaths=',imagePaths)

        # Obtener la lista de directorios en data_path
        people_dirs = [os.path.join(dataPath, d) for d in os.listdir(dataPath) if os.path.isdir(os.path.join(dataPath, d))]

        # Extraer los nombres de las personas de los nombres de los directorios
        nombres_apellidos = [os.path.basename(d) for d in people_dirs]
        print(f"nombres_apellidos: {nombres_apellidos}")  # Imprimir nombres_apellidos
        face_recognizer = cv2.face.FisherFaceRecognizer_create()
        face_recognizer.read('modeloFisherFace.xml')

        cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
        cv2.namedWindow('frame', cv2.WINDOW_NORMAL)

        faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')

        while True:
            ret,frame = cap.read()
            if ret == False: break    
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            auxFrame = gray.copy()

            faces = faceClassif.detectMultiScale(gray,1.3,5)

            for (x,y,w,h) in faces:
                rostro = auxFrame[y:y+h,x:x+w]
                rostro = cv2.resize(rostro,(150,150),interpolation= cv2.INTER_CUBIC)
                result = face_recognizer.predict(rostro)

                cv2.putText(frame,'{}'.format(result),(x,y-5),1,1.3,(255,255,0),1,cv2.LINE_AA)
                
                if result[1] < 1700:
                    cedula = result[0]
                    nombre, apellido = nombres_apellidos[cedula]
                    cv2.putText(frame,'Cedula: {}'.format(cedula),(x,y-45),2,1.1,(0,255,0),1,cv2.LINE_AA)
                    cv2.putText(frame,'{} {}'.format(nombre, apellido),(x,y-25),2,1.1,(0,255,0),1,cv2.LINE_AA)
                    cv2.rectangle(frame, (x,y),(x+w,y+h),(0,255,0),2)
                else:
                    cv2.putText(frame,'Desconocido',(x,y-20),2,0.8,(0,0,255),1,cv2.LINE_AA)
                    cv2.rectangle(frame, (x,y),(x+w,y+h),(0,0,255),2)

            cv2.imshow('frame',frame)
            k = cv2.waitKey(1)
            if k == 27:
                break

        cap.release()
        cv2.destroyAllWindows()

    threading.Thread(target=run).start()

    return HttpResponse("Face recognition started.")