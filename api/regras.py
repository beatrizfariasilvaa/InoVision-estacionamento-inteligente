from datetime import datetime
from sqlalchemy.orm import Session
from models import RegistroVeiculo

# Estado em memória das 3 vagas (atualizado pelo PUT /vagas)
estado_vagas = "000"

def atualizar_estado_vagas(novo_estado: str):
    global estado_vagas
    estado_vagas = novo_estado

def obter_estado_vagas():
    ocupadas = estado_vagas.count("1")
    return {
        "estado": estado_vagas,
        "vagas_ocupadas": ocupadas,
        "vagas_livres": 3 - ocupadas
    }

def processar_leitura(db: Session, placa: str):
    horario_atual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    # Verifica se o carro já está dentro do estacionamento (sem horário de saída)
    registro_ativo = db.query(RegistroVeiculo).filter(
        RegistroVeiculo.placa == placa,
        RegistroVeiculo.saida == None
    ).first()

    # Caso 1: Carro já está no banco -> é uma SAÍDA
    if registro_ativo:
        registro_ativo.saida = horario_atual
        db.commit()
        return {
            "acao": "abrir",
            "tipo": "saida",
            "placa": placa,
            "motivo": "Saída registrada com sucesso."
        }

    # Caso 2: Carro não está no banco -> é uma ENTRADA
    ocupadas_sensores = estado_vagas.count("1")
    carros_no_banco = db.query(RegistroVeiculo).filter(RegistroVeiculo.saida == None).count()
    total_ocupadas = max(ocupadas_sensores, carros_no_banco)

    if total_ocupadas >= 3:
        return {
            "acao": "recusar",
            "tipo": "entrada",
            "placa": placa,
            "motivo": "Estacionamento lotado (3/3 vagas ocupadas)."
        }

    novo_carro = RegistroVeiculo(placa=placa, entrada=horario_atual)
    db.add(novo_carro)
    db.commit()
    return {
        "acao": "abrir",
        "tipo": "entrada",
        "placa": placa,
        "motivo": "Entrada autorizada. Vaga disponível."
    }
