import cv2

# Carga el clasificador frontal de OpenCV para la detección de rostros
face_cascade = cv2.CascadeClassifier('haar_cascades/haarcascade_frontalface_default.xml')

# Inicializa la cámara

def contar_personas(estacion):
    cap = cv2.VideoCapture(estacion['camara'])
    
    contador_personas = 0
    
    ret, frame = cap.read()
    
    # Convierte el fotograma a escala de grises para la detección de rostros
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Detecta rostros en el fotograma
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
    # Incrementa el contador por cada rostro detectado
    contador_personas = len(faces)   
    
    # Libera los recursos
    cap.release()
    cv2.destroyAllWindows()

    return contador_personas
