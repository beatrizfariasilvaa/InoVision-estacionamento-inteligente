"""Abre a webcam e tira fotos (frames) dela."""
import cv2

#0 -> webcam do notebook
#1 -> webcam USB.
CAMERA = 1


def abrir_camera():
    camera = cv2.VideoCapture(CAMERA, cv2.CAP_DSHOW)
    if not camera.isOpened():
        print("Não foi possivel abrir a câmera", CAMERA)
    return camera


def capturar_frame(camera):
    """Tira uma foto da webcam. Devolve a foto, ou None se deu erro."""
    deu_certo, foto = camera.read()
    if deu_certo:
        return foto
    return None
