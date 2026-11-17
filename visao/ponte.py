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
TEMPO_PARA_SUMIR = 15

camera = abrir_camera()
arduino = conectar()
ultima_placa = None
ultima_vez_vista = 0
print("Rodando. Q na janela da webcam para sair.")

while True:
    frame = capturar_frame(camera)
    if frame is None:
        break
    cv2.imshow("webcam", frame)
    if cv2.waitKey(1) == ord("q"):
        break

    try:
        estado = ler_vagas(arduino)
        if estado is not None:
            requests.put(URL_API + "/vagas", json={"estado": estado})
            print("Vagas:", estado)

        placa, confianca = reconhecer_placa(frame)

        if placa is not None and confianca >= CONFIANCA_MINIMA:
            agora = time.time()
            carro_ainda_na_frente = placa == ultima_placa and agora - ultima_vez_vista < TEMPO_PARA_SUMIR
            ultima_vez_vista = agora

            if not carro_ainda_na_frente:
                ultima_placa = placa

                resposta = requests.post(URL_API + "/leituras", json={"placa": placa}).json()
                print(f"Placa {resposta['placa']}: {resposta['acao']} ({resposta['tipo']}) - {resposta['motivo']}")

                if resposta["acao"] == "abrir":
                    abrir_cancela(arduino)

    except requests.RequestException:
        print("Sem conexão com a API.")
        time.sleep(1)

camera.release()
arduino.close()
cv2.destroyAllWindows()
