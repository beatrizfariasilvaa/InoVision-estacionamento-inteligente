from sqlalchemy import Column, Integer, String
from datetime import datetime
from database import Base

def agora_formatado():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

class RegistroVeiculo(Base):
    __tablename__ = "veiculos"

    id = Column(Integer, primary_key=True, index=True)
    placa = Column(String(7), index=True, nullable=False)
    entrada = Column(String(20), default=agora_formatado, nullable=False)
    saida = Column(String(20), nullable=True) # Fica vazio enquanto o carro está estacionado
