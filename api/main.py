from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import Base, engine, SessionLocal
from models import RegistroVeiculo
from validacao import corrigir_e_validar_placa
import regras

Base.metadata.create_all(bind=engine)

app = FastAPI(title="InoVision - Estacionamento Inteligente")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class LeituraInput(BaseModel):
    placa: str

class VagasInput(BaseModel):
    estado: str # Ex.: "010"

@app.post("/leituras")
def receber_leitura(dados: LeituraInput, db: Session = Depends(get_db)):
    valida, placa_corrigida = corrigir_e_validar_placa(dados.placa)
    if not valida:
        return {
            "acao": "recusar",
            "tipo": "desconhecido",
            "placa": placa_corrigida,
            "motivo": "Placa em formato inválido."
        }
    return regras.processar_leitura(db, placa_corrigida)

@app.put("/vagas")
def atualizar_vagas(dados: VagasInput):
    if len(dados.estado) != 3 or any(c not in "01" for c in dados.estado):
        raise HTTPException(status_code=400, detail="Use 3 dígitos 0 ou 1 (ex: '010')")
    regras.atualizar_estado_vagas(dados.estado)
    return regras.obter_estado_vagas()

@app.get("/vagas")
def listar_vagas():
    return regras.obter_estado_vagas()

@app.get("/veiculos")
def listar_veiculos(db: Session = Depends(get_db)):
    ativos = db.query(RegistroVeiculo).filter(RegistroVeiculo.saida == None).all()
    historico = db.query(RegistroVeiculo).order_by(RegistroVeiculo.id.desc()).limit(20).all()
    return {"estacionados_agora": ativos, "historico": historico}

@app.delete("/veiculos")
def zerar_banco(db: Session = Depends(get_db)):
    removidos = db.query(RegistroVeiculo).delete()
    db.commit()
    regras.atualizar_estado_vagas("000")
    return {
        "mensagem": "Banco de dados e vagas zerados com sucesso!",
        "registros_apagados": removidos,
        "estado_vagas": "000"
    }
