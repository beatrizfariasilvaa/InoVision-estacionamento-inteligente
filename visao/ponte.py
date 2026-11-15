"""Programa principal: câmera -> IA -> API -> Arduino.

Antes de rodar, deixe a API ligada (dentro de api/: uvicorn main:app).
Rodar (dentro de visao/): python ponte.py
Q na janela da webcam: sai
"""
import time

import cv2
import requests

from camera import abrir_camera, capturar_frame
from reconhecer import reconhecer_placa
from serial_arduino import abrir_cancela, conectar, ler_vagas

URL_API = "http://localhost:8000"
CONFIANCA_MINIMA = 0.6
ESPERA = 10

camera = abrir_camera()
arduino = conectar()
ultima_leitura = 0.0
print("Rodando. Q na janela da webcam para sair.")

while True:
    frame = capturar_frame(camera)
    if frame is None:
        break
    cv2.imshow("webcam", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

    try:
        estado = ler_vagas(arduino)
        if estado is not None:
            requests.put(f"{URL_API}/vagas", json={"estado": estado})
            print("Vagas:", estado)

        if time.time() - ultima_leitura < ESPERA:
            continue
        placa, confianca = reconhecer_placa(frame)
        if placa is None or confianca < CONFIANCA_MINIMA:
            continue

        ultima_leitura = time.time()
        resposta = requests.post(f"{URL_API}/leituras", json={"placa": placa}).json()
        print(f"Placa {resposta['placa']}: {resposta['acao']} ({resposta['tipo']}) - {resposta['motivo']}")

        if resposta["acao"] == "abrir":
            abrir_cancela(arduino)

    except requests.RequestException:
        print("Sem conexão com a API.")
        time.sleep(1)

camera.release()
arduino.close()
cv2.destroyAllWindows()
