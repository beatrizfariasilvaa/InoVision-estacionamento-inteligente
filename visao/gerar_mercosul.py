"""Gera caracteres sintéticos na fonte da placa Mercosul e salva em dados/<caractere>/.

Antes de rodar:
  1. pip install pillow
  2. Coloque o arquivo da fonte (.ttf ou .otf) dentro da pasta visao.

Rodar:      python gerar_mercosul.py
Depois:     python treinar_mlp.py   (treinar de novo com os dados novos)

Rodar de novo apaga os sintéticos antigos antes de gerar (as imagens do Kaggle ficam intactas).
"""
import random
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

PASTA_DADOS = Path("dados")
POR_CARACTERE = 400             
PREFIXO = "mercosul_"           
CARACTERES = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

random.seed(42)
np.random.seed(42)


def achar_fonte():
    fontes = list(Path(".").glob("*.ttf")) + list(Path(".").glob("*.otf"))
    if not fontes:
        raise FileNotFoundError("Coloque o arquivo .ttf ou .otf da fonte Mercosul na pasta visao.")
    print("Usando a fonte:", fontes[0].name)
    return str(fontes[0])


def desenhar(caractere, fonte_path):
    """Desenha 1 caractere escuro em fundo cinza claro, com variações aleatórias."""
    tamanho = random.randint(90, 130)
    fonte = ImageFont.truetype(fonte_path, tamanho)

    tela = 220
    fundo = random.randint(150, 230)        
    tinta = random.randint(10, 70)           
    img = Image.new("L", (tela, tela), color=fundo)
    ImageDraw.Draw(img).text((tela // 2, tela // 2), caractere, font=fonte, fill=tinta, anchor="mm")
    img = np.array(img)


    angulo = random.uniform(-6, 6)
    inclinacao = random.uniform(-0.25, 0.1)
    M = cv2.getRotationMatrix2D((tela / 2, tela / 2), angulo, 1.0)
    M[0, 1] += inclinacao
    M[0, 2] -= inclinacao * tela / 2
    img = cv2.warpAffine(img, M, (tela, tela), borderValue=fundo)

    kernel = np.ones((3, 3), np.uint8)
    sorteio = random.random()
    if sorteio < 0.3:
        img = cv2.erode(img, kernel)          
    elif sorteio < 0.5:
        img = cv2.dilate(img, kernel)         

    ys, xs = np.where(img < (fundo + tinta) / 2)
    m = random.randint(-3, 15)
    y0, y1 = max(0, ys.min() - m), min(tela, ys.max() + m)
    x0, x1 = max(0, xs.min() - m), min(tela, xs.max() + m)
    img = img[y0:y1, x0:x1]

    # Desfoque e ruído, como numa foto
    if random.random() < 0.6:
        img = cv2.GaussianBlur(img, (random.choice([3, 5]),) * 2, 0)
    ruido = np.random.normal(0, random.uniform(2, 12), img.shape)
    img = np.clip(img + ruido, 0, 255).astype(np.uint8)

    altura = random.randint(60, 110)
    largura = max(8, int(img.shape[1] * altura / img.shape[0]))
    return cv2.resize(img, (largura, altura), interpolation=cv2.INTER_AREA)


def main():
    fonte_path = achar_fonte()
    exemplos = []
    for caractere in CARACTERES:
        pasta = PASTA_DADOS / caractere
        pasta.mkdir(parents=True, exist_ok=True)
        for antigo in pasta.glob(PREFIXO + "*"):
            antigo.unlink()
        for i in range(POR_CARACTERE):
            img = desenhar(caractere, fonte_path)
            cv2.imwrite(str(pasta / f"{PREFIXO}{i:04d}.png"), img)
            if i == 0:
                exemplos.append(cv2.resize(img, (60, 80)))
        print(f"{caractere}: {POR_CARACTERE} imagens")

if __name__ == "__main__":
    main()