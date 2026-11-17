"""Lê o texto da placa: foto -> placa -> caracteres -> texto."""
import joblib

from preprocessamento import preparar_caractere
from recorte import recortar_placa, separar_caracteres

modelo = joblib.load("modelo_mlp.pkl")


def ler_caracteres(caracteres):
    """Recebe as imagens dos 7 caracteres e devolve (texto, confiança)."""
    texto = ""
    confianca = 1.0

    for imagem in caracteres:
        vetor = preparar_caractere(imagem)

        chances = modelo.predict_proba([vetor])[0]

        melhor = chances.argmax()            
        texto += modelo.classes_[melhor]

        confianca = min(confianca, chances[melhor])

    return texto, float(confianca)


def reconhecer_placa(frame):
    """Devolve (placa, confiança), ou (None, 0.0) se não achou a placa."""
    placa = recortar_placa(frame)
    if placa is None:
        return None, 0.0

    caracteres = separar_caracteres(placa)
    if len(caracteres) != 7:
        return None, 0.0

    return ler_caracteres(caracteres)
