import platform

import cv2


INDICE_CAMERA = None

BACKEND = cv2.CAP_DSHOW if platform.system() == "Windows" else cv2.CAP_ANY


def listar_cameras(maximo=5):
    disponiveis = []
    for i in range(maximo):
        cam = cv2.VideoCapture(i, BACKEND)
        if cam.isOpened() and cam.read()[0]:
            disponiveis.append(i)
        cam.release()
    return disponiveis


def abrir_camera(indice=INDICE_CAMERA):
    if indice is None:
        disponiveis = listar_cameras()
        print("Câmeras encontradas:", disponiveis)
        if not disponiveis:
            raise RuntimeError("Nenhuma câmera encontrada. A webcam está plugada?")
        indice = disponiveis[-1]  
    camera = cv2.VideoCapture(indice, BACKEND)
    if not camera.isOpened():
        raise RuntimeError(f"Não consegui abrir a câmera {indice}")
    print("Usando a câmera", indice)
    return camera


def capturar_frame(camera):
    ok, frame = camera.read()
    return frame if ok else None