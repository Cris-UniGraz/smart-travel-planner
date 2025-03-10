import re
from typing import List

def extract_bracketed_text(text: str) -> List[str]:
    """
    Extrae todo el texto que se encuentra entre corchetes.
    
    Args:
        text (str): El texto de entrada.
        
    Returns:
        List[str]: Lista de textos encontrados entre corchetes.
    """
    return re.findall(r'\[(.*?)\]', text)

def highlight_bracketed_text(text: str, highlight_format: str = '<span class="highlight">{}</span>') -> str:
    """
    Reemplaza el texto entre corchetes con un formato HTML para destacarlo.
    
    Args:
        text (str): El texto de entrada.
        highlight_format (str): El formato HTML a aplicar.
        
    Returns:
        str: El texto con el formato aplicado.
    """
    return re.sub(
        r'\[(.*?)\]',
        lambda m: highlight_format.format(m.group(1)),
        text
    )