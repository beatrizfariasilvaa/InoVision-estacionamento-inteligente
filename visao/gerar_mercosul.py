"""Gera caracteres sintéticos na fonte da placa Mercosul e salva em dados/<caractere>/.

O objetivo é dar ao modelo mais exemplos parecidos com a placa de verdade.
Cada imagem sai um pouco diferente (tamanho, cor, inclinação, borrão, ruído),
para o modelo aprender a reconhecer o caractere mesmo com a câmera ruim.
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
TELA = 220

random.seed(42)
np.random.seed(42)


def achar_fonte():
    fontes = list(Path(".").glob("*.ttf"))
    if len(fontes) == 0:
        raise FileNotFoundError("Coloque o arquivo .ttf da fonte Mercosul na pasta visao.")
    print("Usando a fonte:", fontes[0].name)
    return str(fontes[0])


def escrever_letra(caractere, caminho_fonte):
    """Passo 1: escreve a letra escura no meio de um quadrado cinza claro."""
    tamanho = random.randint(90, 130)
    fonte = ImageFont.truetype(caminho_fonte, tamanho)

    cor_fundo = random.randint(150, 230)  
    cor_tinta = random.randint(10, 70)

    img = Image.new("L", (TELA, TELA), color=cor_fundo)
    meio = (TELA // 2, TELA // 2)
    ImageDraw.Draw(img).text(meio, caractere, font=fonte, fill=cor_tinta, anchor="mm")
    return np.array(img), cor_fundo, cor_tinta


def girar_e_inclinar(img, cor_fundo):
    """Passo 2: gira um pouco a letra e deixa ela meio itálica."""
    angulo = random.uniform(-6, 6)
    inclinacao = random.uniform(-0.25, 0.1)

    centro = (TELA / 2, TELA / 2)
    matriz = cv2.getRotationMatrix2D(centro, angulo, 1.0)
    matriz[0, 1] += inclinacao
    matriz[0, 2] -= inclinacao * TELA / 2

    return cv2.warpAffine(img, matriz, (TELA, TELA), borderValue=cor_fundo)


def engrossar_ou_afinar(img):
    """Passo 3: às vezes deixa o traço mais fino ou mais grosso."""
    kernel = np.ones((3, 3), np.uint8)
    sorteio = random.random()
    if sorteio < 0.3:
        img = cv2.erode(img, kernel)    
    elif sorteio < 0.5:
        img = cv2.dilate(img, kernel)   
    return img           


def recortar_em_volta(img, cor_fundo, cor_tinta):
    """Passo 4: recorta em volta da letra, com uma folga sorteada."""
    limite = (cor_fundo + cor_tinta) / 2
    linhas, colunas = np.where(img < limite)

    folga = random.randint(-3, 15)  
    topo = max(0, linhas.min() - folga)
    baixo = min(TELA, linhas.max() + folga)
    esquerda = max(0, colunas.min() - folga)
    direita = min(TELA, colunas.max() + folga)
    return img[topo:baixo, esquerda:direita]


def borrar_e_sujar(img):
    """Passo 5: às vezes borra a imagem, e sempre adiciona ruído (granulado)."""
    if random.random() < 0.6:
        tamanho_borrao = random.choice([3, 5])
        img = cv2.GaussianBlur(img, (tamanho_borrao, tamanho_borrao), 0)

    forca_ruido = random.uniform(2, 12)
    ruido = np.random.normal(0, forca_ruido, img.shape)
    img = img + ruido
    img = np.clip(img, 0, 255)
    return img.astype(np.uint8)


def redimensionar(img):
    """Passo 6: muda a altura final, mantendo a proporção da letra."""
    altura = random.randint(60, 110)
    altura_atual, largura_atual = img.shape
    largura = max(8, int(largura_atual * altura / altura_atual))
    return cv2.resize(img, (largura, altura), interpolation=cv2.INTER_AREA)


def desenhar(caractere, caminho_fonte):
    """Desenha 1 caractere escuro em fundo cinza claro, com variações aleatórias."""
    img, cor_fundo, cor_tinta = escrever_letra(caractere, caminho_fonte)
    img = girar_e_inclinar(img, cor_fundo)
    img = engrossar_ou_afinar(img)
    img = recortar_em_volta(img, cor_fundo, cor_tinta)
    img = borrar_e_sujar(img)
    img = redimensionar(img)
    return img


def main():
    caminho_fonte = achar_fonte()
    for caractere in CARACTERES:
        pasta = PASTA_DADOS / caractere
        pasta.mkdir(parents=True, exist_ok=True)

        for arquivo_antigo in pasta.glob(PREFIXO + "*"):
            arquivo_antigo.unlink()

        for i in range(POR_CARACTERE):
            img = desenhar(caractere, caminho_fonte)
            nome = f"{PREFIXO}{i:04d}.png"
            cv2.imwrite(str(pasta / nome), img)

        print(f"{caractere}: {POR_CARACTERE} imagens")


if __name__ == "__main__":
    main()
