"""Teste ao vivo: webcam -> recorte -> MLP -> string.

ESPAÇO: tenta ler a placa do frame atual (e salva os recortes em debug/)
Q: sai
"""
from pathlib import Path

import cv2

from camera import abrir_camera, capturar_frame
from recorte import recortar_placa, separar_caracteres
from reconhecer import ler_caracteres

PASTA_DEBUG = Path("debug")
PASTA_DEBUG.mkdir(exist_ok=True)

camera = abrir_camera()
print("ESPAÇO = ler placa | Q = sair")

while True:
    frame = capturar_frame(camera)
    if frame is None:
        break
    cv2.imshow("webcam", frame)
    tecla = cv2.waitKey(1) & 0xFF

    if tecla == ord("q"):
        break

    if tecla == ord(" "):
        cv2.imwrite(str(PASTA_DEBUG / "frame.png"), frame)
        placa = recortar_placa(frame)
        if placa is None:
            print("Placa não encontrada no frame")
            continue
        cv2.imwrite(str(PASTA_DEBUG / "placa.png"), placa)

        caracteres = separar_caracteres(placa)
        for i, c in enumerate(caracteres):
            cv2.imwrite(str(PASTA_DEBUG / f"char_{i}.png"), c)
        if len(caracteres) != 7:
            print(f"Achei {len(caracteres)} caracteres em vez de 7 (veja debug/)")
            continue

        texto, confianca = ler_caracteres(caracteres)
        print(f"Placa: {texto}  (confiança mínima: {confianca:.0%})")

camera.release()
cv2.destroyAllWindows()