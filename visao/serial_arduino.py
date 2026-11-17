"""Conversa com o Arduino pelo cabo USB.

Mensagens trocadas:
    PC -> Arduino: ABRIR        (levanta a cancela)
    Arduino -> PC: VAGAS:010    (1 = vaga ocupada, 0 = livre)
"""
import time

import serial

PORTA = "COM7"
VELOCIDADE = 9600


def conectar():
    arduino = serial.Serial(PORTA, VELOCIDADE, timeout=0.1)
    time.sleep(2)
    print("Arduino conectado na porta", PORTA)
    return arduino


def abrir_cancela(arduino):
    arduino.write(b"ABRIR\n")

def ler_vagas(arduino):
    """Devolve o estado mais recente das vagas (ex.: "010") ou None se não chegou nada."""
    estado = None

    while arduino.in_waiting > 0:
        linha = arduino.readline()
        linha = linha.decode(errors="ignore").strip()
        if linha.startswith("VAGAS:"):
            estado = linha.replace("VAGAS:", "")

    return estado
