from pathlib import Path

import cv2
import joblib
import numpy as np
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier

from preprocessamento import preparar_caractere

PASTA_DADOS = Path("dados")
EXTENSOES = {".jpg", ".jpeg", ".png", ".bmp"}

# PASSO 1 - Carregar as imagens e os rótulos
# X = as imagens já transformadas em vetores
# y = o rótulo de cada uma (o nome da pasta onde ela está)
X, y = [], []
for arquivo in PASTA_DADOS.rglob("*"):
    if arquivo.suffix.lower() not in EXTENSOES:
        continue
    imagem = cv2.imread(str(arquivo), cv2.IMREAD_GRAYSCALE)
    if imagem is None:
        continue
    X.append(preparar_caractere(imagem))
    y.append(arquivo.parent.name.upper())

X = np.array(X)
y = np.array(y)
print("Formato de X:", X.shape)  
print("Classes encontradas:", sorted(set(y)))
print("Total de classes:", len(set(y)))

# PASSO 2 - Dividir em treino e teste
# stratify=y mantém a mesma proporção de cada letra nos dois conjuntos
X_treino, X_teste, y_treino, y_teste = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)
print("Treino:", X_treino.shape[0], "| Teste:", X_teste.shape[0])


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


# PASSO 4 - Avaliar no teste (imagens que o modelo nunca viu)
y_previsto = modelo.predict(X_teste)
print("\nAcurácia no teste:", round(accuracy_score(y_teste, y_previsto), 4))
print(classification_report(y_teste, y_previsto))


probabilidades = modelo.predict_proba(X_teste[:1])[0]
top3 = np.argsort(probabilidades)[::-1][:3]
print("Rótulo real:", y_teste[0])
for i in top3:
    print(f"  {modelo.classes_[i]}: {probabilidades[i]:.2%}")


# PASSO 5 - Salvar o modelo para o reconhecer.py usar depois
joblib.dump(modelo, "modelo_mlp.pkl")
print("\nModelo salvo em modelo_mlp.pkl")