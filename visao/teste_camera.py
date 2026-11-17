"""Testa só a câmera e a IA (sem Arduino e sem API).

ESPAÇO: tenta ler a placa (e salva as imagens na pasta debug/)
Q: sai
"""
import os

import cv2

from camera import abrir_camera, capturar_frame
from recorte import recortar_placa, separar_caracteres
from reconhecer import ler_caracteres

os.makedirs("debug", exist_ok=True)

camera = abrir_camera()
print("ESPAÇO = ler placa | Q = sair")

while True:
    frame = capturar_frame(camera)
    if frame is None:
        break
    cv2.imshow("webcam", frame)
    tecla = cv2.waitKey(1)

    if tecla == ord("q"):
        break

    if tecla == ord(" "):
        cv2.imwrite("debug/frame.png", frame)

        placa = recortar_placa(frame)
        if placa is None:
            print("Não achei a placa")
            continue
        cv2.imwrite("debug/placa.png", placa)

        caracteres = separar_caracteres(placa)
        for i in range(len(caracteres)):
            cv2.imwrite(f"debug/char_{i}.png", caracteres[i])
        if len(caracteres) != 7:
            print("Achei", len(caracteres), "caracteres em vez de 7 (veja a pasta debug/)")
            continue

        texto, confianca = ler_caracteres(caracteres)
        print("Placa:", texto, "- confiança:", round(confianca * 100), "%")

camera.release()
cv2.destroyAllWindows()
