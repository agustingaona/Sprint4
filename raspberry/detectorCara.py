import cv2

face_cascade = cv2.CascadeClassifier('haar_cascades/haarcascade_frontalface_default.xml')


def contar_personas(estacion):
    cap = cv2.VideoCapture(estacion['camara'])
    
    contador_personas = 0
    
    ret, frame = cap.read()
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
    contador_personas = len(faces)   
    
    cap.release()
    cv2.destroyAllWindows()

    return contador_personas
