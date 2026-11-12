import cv2
import numpy as np

TAMANHO = (28, 28)


def preparar_caractere(imagem):
    """Recebe a imagem de UM caractere e devolve o vetor de números que a MLP entende.

    Usada em dois lugares:
      - treinar_mlp.py  -> nas imagens do Kaggle
      - reconhecer.py   -> nos recortes da webcam
    Por isso fica num arquivo separado: os dois TÊM que preparar a imagem igual.
    """
    if imagem.ndim == 3:
        imagem = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

    imagem = cv2.resize(imagem, TAMANHO, interpolation=cv2.INTER_AREA)

    _, imagem = cv2.threshold(imagem, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    if imagem.mean() > 127:
        imagem = 255 - imagem

    imagem = imagem.astype(np.float32) / 255.0
    return imagem.flatten()