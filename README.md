# InoVision-estacionamento-inteligente

## Como rodar

### Pré-requisitos
- Python 3.10 ou mais novo (desenvolvido com 3.14)
- Uma webcam (pode ser a do notebook ou uma USB)
- Git

### 1. Clonar o repositório
```bash
git clone https://github.com/beatrizfariasilvaa/InoVision-estacionamento-inteligente.git
cd InoVision-estacionamento-inteligente
```

### 2. Criar e ativar o ambiente virtual
```bash
python -m venv venv

venv\Scripts\Activate.ps1
```
### 3. Instalar as dependências
```bash
pip install opencv-python numpy scikit-learn joblib pillow
```
### 4. Testar o reconhecimento de placas
```bash
cd visao
python teste_camera.py
```

Como testar:
- Aponte a webcam para a placa e aperte ESPAÇO para ler.
- Aperte Q para sair.
- Os recortes de cada tentativa (frame, placa e caracteres) são salvos em visao/debug/, o que ajuda a entender por que uma leitura falhou.






