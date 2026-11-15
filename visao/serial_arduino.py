"""Conversa com o Arduino pelo cabo USB.

PC -> Arduino: ABRIR
Arduino -> PC: VAGAS:010
"""
import time

import serial
from serial.tools import list_ports

PORTA = None
VELOCIDADE = 9600


def conectar(porta=PORTA):
    if porta is None:
        portas = [p.device for p in list_ports.comports()]
        print("Portas encontradas:", portas)
        if not portas:
            raise RuntimeError("Nenhum Arduino encontrado.")
        porta = portas[0]
    arduino = serial.Serial(porta, VELOCIDADE, timeout=0.1)
    time.sleep(2)
    print("Arduino conectado na porta", porta)
    return arduino


def abrir_cancela(arduino):
    arduino.write(b"ABRIR\n")


def ler_vagas(arduino):
    """Devolve o estado mais recente das vagas (ex.: "010") ou None se não chegou nada."""
    estado = None
    while arduino.in_waiting:
        linha = arduino.readline().decode(errors="ignore").strip()
        if linha.startswith("VAGAS:"):
            estado = linha.replace("VAGAS:", "")
    return estado
