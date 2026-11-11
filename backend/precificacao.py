# presificacao.py
from typing import Dict, Any

def parse_preco(txt: str) -> float:
    """
    Converte 'R$ 12,34' ou '12,34' ou '12.34' -> float
    """
    if txt is None:
        return 0.0
    s = str(txt).strip().lower().replace('r$', '').replace(' ', '')
    s = s.replace('.', '').replace(',', '.')
    try:
        return float(s)
    except ValueError:
        raise ValueError(f"Preço inválido: {txt!r}")

def format_preco(valor: float) -> str:
    return f"R$ {valor:0.2f}".replace('.', ',')

# Estado default (pode ser carregado/alterado)
DEFAULT_ITENS: Dict[int, Dict[str, Any]] = {
    2: {"nome": "Teclado", "preco": 99.90},
    3: {"nome": "Copo",    "preco": 12.50},
    4: {"nome": "Livro",   "preco": 59.00},
    5: {"nome": "Mouse",   "preco": 49.99},
    6: {"nome": "Cabo",    "preco": 19.90},
    7: {"nome": "Luz",     "preco": 9.99},
}
