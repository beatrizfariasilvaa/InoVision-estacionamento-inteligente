import joblib
import numpy as np

from preprocessamento import preparar_caractere
from recorte import NUM_CARACTERES, recortar_placa, separar_caracteres

modelo = joblib.load("modelo_mlp.pkl")


def ler_caracteres(caracteres):
    """Recebe a lista de imagens de caracteres e devolve (string, confiança mínima)."""
    vetores = np.array([preparar_caractere(c) for c in caracteres])
    probabilidades = modelo.predict_proba(vetores)          
    indices = probabilidades.argmax(axis=1)                
    letras = modelo.classes_[indices]
    confianca = probabilidades.max(axis=1).min()      
    return "".join(letras), float(confianca)


def reconhecer_placa(frame):
    """Do frame da webcam até a string. Devolve (placa, confiança) ou (None, 0.0)."""
    placa = recortar_placa(frame)
    if placa is None:
        return None, 0.0

    caracteres = separar_caracteres(placa)
    if len(caracteres) != NUM_CARACTERES:
        return None, 0.0

    return ler_caracteres(caracteres)