import cv2
from preprocessamento import preparar_caractere

img = cv2.imread("dados/0/aug8041_0.jpg")
vetor = preparar_caractere(img)
print(vetor.shape)
cv2.imwrite("teste.png", (vetor.reshape(28, 28) * 255).astype("uint8"))