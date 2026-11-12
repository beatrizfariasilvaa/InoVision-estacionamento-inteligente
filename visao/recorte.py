import cv2
import numpy as np

PROPORCAO_MIN = 2.0
PROPORCAO_MAX = 6.0
NUM_CARACTERES = 7


def recortar_placa(frame):
    """Recebe o frame inteiro da webcam e devolve só o retângulo da placa (ou None).

    Procura contornos com 4 cantos e formato de placa, e fica com o maior.
    """
    cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cinza = cv2.bilateralFilter(cinza, 11, 17, 17) 
    bordas = cv2.Canny(cinza, 30, 200)

    contornos, _ = cv2.findContours(bordas, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contornos = sorted(contornos, key=cv2.contourArea, reverse=True)[:15]

    for contorno in contornos:
        perimetro = cv2.arcLength(contorno, True)
        aproximado = cv2.approxPolyDP(contorno, 0.02 * perimetro, True)
        if len(aproximado) != 4:
            continue
        x, y, w, h = cv2.boundingRect(aproximado)
        if h == 0 or w * h < 1500:
            continue
        if PROPORCAO_MIN <= w / h <= PROPORCAO_MAX:
            return frame[y:y + h, x:x + w]
    return None


def _quadrado_com_margem(caractere, margem=4):
    """Coloca o caractere no centro de um quadrado preto, para não distorcer no 28x28."""
    h, w = caractere.shape
    lado = max(h, w) + 2 * margem
    quadrado = np.zeros((lado, lado), dtype=np.uint8)
    y0 = (lado - h) // 2
    x0 = (lado - w) // 2
    quadrado[y0:y0 + h, x0:x0 + w] = caractere
    return quadrado


def separar_caracteres(placa):
    """Recebe a imagem da placa e devolve a lista de caracteres, da esquerda para a direita.

    Cada caractere sai como letra branca em fundo preto, no mesmo padrão do treino.
    """
    if placa.ndim == 3:
        placa = cv2.cvtColor(placa, cv2.COLOR_BGR2GRAY)

    _, pb = cv2.threshold(placa, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    h_p, w_p = pb.shape
    my, mx = max(2, int(0.06 * h_p)), max(2, int(0.03 * w_p))
    pb[:my, :] = 0
    pb[-my:, :] = 0
    pb[:, :mx] = 0
    pb[:, -mx:] = 0

    altura_placa = pb.shape[0]
    contornos, _ = cv2.findContours(pb, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    caixas = []
    for contorno in contornos:
        x, y, w, h = cv2.boundingRect(contorno)
        if 0.35 * altura_placa <= h <= 0.95 * altura_placa and w < h:
            caixas.append((x, y, w, h))

    caixas = sorted(caixas, key=lambda c: c[3], reverse=True)[:NUM_CARACTERES]
    caixas = sorted(caixas, key=lambda c: c[0])

    return [_quadrado_com_margem(pb[y:y + h, x:x + w]) for x, y, w, h in caixas]