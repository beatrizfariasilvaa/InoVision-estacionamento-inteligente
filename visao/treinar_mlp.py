"""Treina a rede neural (MLP) que reconhece letras e números.

Rodar uma vez (dentro de visao/): python treinar_mlp.py
No final ela é salva em modelo_mlp.pkl, que o reconhecer.py usa.
"""
from pathlib import Path

import cv2
import joblib
import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier

from preprocessamento import preparar_caractere

# PASSO 1 - Carregar as imagens
# X = as imagens (já transformadas em números)
# y = a resposta certa de cada imagem (o nome da pasta onde ela está: A, B, 7...)
X = []
y = []
for arquivo in Path("dados").rglob("*"):
    if arquivo.suffix not in [".jpg", ".png"]:
        continue
    imagem = cv2.imread(str(arquivo), cv2.IMREAD_GRAYSCALE)
    X.append(preparar_caractere(imagem))
    y.append(arquivo.parent.name.upper())

X = np.array(X)
y = np.array(y)
print("Total de imagens:", len(X))

# PASSO 2 - Separar 80% para treinar e 20% para testar
X_treino, X_teste, y_treino, y_teste = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# PASSO 3 - Criar e treinar a MLP
modelo = MLPClassifier(
    hidden_layer_sizes=(256, 128),
    activation="relu",
    max_iter=300,                    
    early_stopping=True,             
    random_state=42,
    verbose=True,                    
)
modelo.fit(X_treino, y_treino)

# PASSO 4 - Testar com imagens que o modelo nunca viu
y_previsto = modelo.predict(X_teste)
print("Acurácia no teste:", accuracy_score(y_teste, y_previsto))

# PASSO 5 - Salvar o modelo
joblib.dump(modelo, "modelo_mlp.pkl")
print("Modelo salvo em modelo_mlp.pkl")
