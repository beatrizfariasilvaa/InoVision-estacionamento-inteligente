"""Transforma a imagem de UMA letra nos 784 números que a rede neural entende."""
import cv2
import numpy as np


def preparar_caractere(imagem):
    """Usada no treino (treinar_mlp.py) e na webcam (reconhecer.py)."""
    if imagem.ndim == 3:
        imagem = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

    limite, pb = cv2.threshold(imagem, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    if pb.mean() > 127:
        pb = 255 - pb

    pb = centralizar(pb)
    pb = cv2.resize(pb, (28, 28), interpolation=cv2.INTER_AREA)

    pb = pb.astype(np.float32) / 255.0
    return pb.flatten()


def centralizar(pb):
    """Recorta a letra bem justa e coloca no meio de um quadrado com margem.

    Assim as letras do treino e as da webcam ficam do mesmo tamanho e na mesma posição.
    """
    contornos, hierarquia = cv2.findContours(pb, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(contornos) == 0:
        return pb

    maior_area = max(cv2.contourArea(c) for c in contornos)
    pedacos = []
    for contorno in contornos:
        if cv2.contourArea(contorno) >= 0.1 * maior_area:
            pedacos.append(contorno)

    x, y, largura, altura = cv2.boundingRect(np.vstack(pedacos))
    letra = pb[y:y + altura, x:x + largura]

    lado = int(max(altura, largura) / 0.76)
    quadrado = np.zeros((lado, lado), dtype=np.uint8)
    y = (lado - altura) // 2
    x = (lado - largura) // 2
    quadrado[y:y + altura, x:x + largura] = letra
    return quadrado
