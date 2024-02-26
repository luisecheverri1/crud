import os
import cv2
import numpy as np
from reconfacial1.capturandoRostros import capturar_rostros3

def entrenando(photo_path, cedula, nombre, apellido):
    dataPath = "C:/Users/PC/Desktop/biometrikAss/biometrikAssProject/data" # Cambia a la ruta donde hayas almacenado Data
    peopleList = os.listdir(dataPath)
    print('Lista de personas: ', peopleList)

    # Verificar que haya al menos dos personas antes de continuar
    if len(peopleList) < 2:
        print("Error: Se necesitan al menos dos personas para entrenar el modelo.")
        return

    labels = []
    facesData = []
    label = 0

    for nameDir in peopleList:
        personPath = dataPath + '/' + nameDir
        print('Leyendo las imágenes')

        for fileName in os.listdir(photo_path):
            print('Rostros: ', photo_path)
            labels.append(label)
            facesData.append(cv2.imread(personPath+'/'+fileName, 0))
            # image = cv2.imread(personPath+'/'+fileName,0)
            # cv2.imshow('image',image)
            # cv2.waitKey(10)
        label = label + 1

    # Verificar que haya al menos una muestra de cada persona
    if len(labels) < 2:
        print("Error: Se necesitan al menos dos personas con muestras de entrenamiento.")
        return

    # Métodos para entrenar el reconocedor
    face_recognizer = cv2.face.FisherFaceRecognizer_create()

    # Entrenando el reconocedor de rostros
    print("Entrenando...")
    face_recognizer.train(facesData, np.array(labels))

    # Almacenando el modelo obtenido
    face_recognizer.write('modeloFisherFace.xml')
    print("Modelo almacenado...")
