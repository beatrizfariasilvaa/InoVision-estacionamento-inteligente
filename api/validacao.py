import re

MAPA_PARA_LETRA = {'0': 'O', '1': 'I', '8': 'B'}
MAPA_PARA_NUMERO = {'O': '0', 'I': '1', 'B': '8'}

def corrigir_e_validar_placa(texto: str):
    placa = re.sub(r'[^A-Za-z0-9]', '', texto.upper())
    if len(placa) != 7:
        return False, placa

    chars = list(placa)

    # Posições 0, 1 e 2 são sempre LETRAS
    for i in [0, 1, 2]:
        if chars[i] in MAPA_PARA_LETRA:
            chars[i] = MAPA_PARA_LETRA[chars[i]]

    # Posições 3, 5 e 6 são sempre NÚMEROS
    for i in [3, 5, 6]:
        if chars[i] in MAPA_PARA_NUMERO:
            chars[i] = MAPA_PARA_NUMERO[chars[i]]

    # Posição 4 pode ser letra (Mercosul) ou número (antiga)
    placa_corrigida = "".join(chars)
    padrao_valido = re.match(r'^[A-Z]{3}[0-9][A-Z0-9][0-9]{2}$', placa_corrigida)

    return bool(padrao_valido), placa_corrigida
