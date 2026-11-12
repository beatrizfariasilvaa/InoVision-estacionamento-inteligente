import cv2
import numpy as np

TAMANHO = (28, 28)
MARGEM = 0.12


def _enquadrar(pb):
    """Recorta o caractere justo e centraliza num quadrado com margem fixa.

    Isso faz o caractere do Kaggle e o da webcam ficarem do MESMO tamanho
    e na MESMA posição, não importa como cada imagem veio enquadrada.
    """
    contornos, _ = cv2.findContours(pb, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contornos:
        return pb
    maior = max(cv2.contourArea(c) for c in contornos)
    caixas = [cv2.boundingRect(c) for c in contornos if cv2.contourArea(c) >= 0.1 * maior]
    x0 = min(x for x, y, w, h in caixas)
    y0 = min(y for x, y, w, h in caixas)
    x1 = max(x + w for x, y, w, h in caixas)
    y1 = max(y + h for x, y, w, h in caixas)
    caractere = pb[y0:y1, x0:x1]

    h, w = caractere.shape
    lado = int(max(h, w) / (1 - 2 * MARGEM))
    quadrado = np.zeros((lado, lado), dtype=np.uint8)
    yi, xi = (lado - h) // 2, (lado - w) // 2
    quadrado[yi:yi + h, xi:xi + w] = caractere
    return quadrado


def preparar_caractere(imagem):
    """Recebe a imagem de UM caractere e devolve o vetor de 784 números que a MLP entende.

    Usada no treinar_mlp.py (imagens do Kaggle) e no reconhecer.py (webcam).
    """
    if imagem.ndim == 3:
        imagem = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

    _, pb = cv2.threshold(imagem, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    if pb.mean() > 127:
        pb = 255 - pb

    pb = _enquadrar(pb)

    pb = cv2.resize(pb, TAMANHO, interpolation=cv2.INTER_AREA)
    return (pb.astype(np.float32) / 255.0).flatten()
