"""Acha a placa na foto e separa as letras dela."""
import cv2
import numpy as np


def recortar_placa(frame):
    """Procura um retângulo com formato de placa e devolve só esse pedaço da foto (ou None)."""
    cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cinza = cv2.bilateralFilter(cinza, 11, 17, 17)   
    bordas = cv2.Canny(cinza, 30, 200)

    contornos, hierarquia = cv2.findContours(bordas, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    contornos = sorted(contornos, key=cv2.contourArea, reverse=True)
    for contorno in contornos[:15]:
        perimetro = cv2.arcLength(contorno, True)
        cantos = cv2.approxPolyDP(contorno, 0.02 * perimetro, True)
        if len(cantos) != 4:
            continue

        x, y, largura, altura = cv2.boundingRect(cantos)
        if altura == 0 or largura * altura < 1500:   
            continue

        if 2 <= largura / altura <= 6:
            return frame[y:y + altura, x:x + largura]

    return None


def separar_caracteres(placa):
    """Devolve a lista de imagens das letras, da esquerda para a direita."""
    cinza = cv2.cvtColor(placa, cv2.COLOR_BGR2GRAY)

    limite, pb = cv2.threshold(cinza, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    altura_placa, largura_placa = pb.shape
    borda_y = max(2, int(0.06 * altura_placa))
    borda_x = max(2, int(0.03 * largura_placa))
    pb[:borda_y, :] = 0    
    pb[-borda_y:, :] = 0
    pb[:, :borda_x] = 0
    pb[:, -borda_x:] = 0

    contornos, hierarquia = cv2.findContours(pb, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    letras = []
    for contorno in contornos:
        x, y, largura, altura = cv2.boundingRect(contorno)
        if 0.35 * altura_placa <= altura <= 0.95 * altura_placa and largura < altura:
            letras.append((x, y, largura, altura))

    letras = sorted(letras, key=lambda letra: letra[3], reverse=True)[:7]
    letras = sorted(letras, key=lambda letra: letra[0])

    imagens = []
    for x, y, largura, altura in letras:
        recorte = pb[y:y + altura, x:x + largura]
        imagens.append(colocar_em_quadrado(recorte))
    return imagens


def colocar_em_quadrado(letra):
    """Cola a letra no meio de um quadrado preto, para ela não ficar esticada depois."""
    altura, largura = letra.shape
    lado = max(altura, largura) + 8
    quadrado = np.zeros((lado, lado), dtype=np.uint8)

    y = (lado - altura) // 2
    x = (lado - largura) // 2
    quadrado[y:y + altura, x:x + largura] = letra
    return quadrado
