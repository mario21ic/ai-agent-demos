from strands import Agent, tool
from strands.models.llamacpp import LlamaCppModel
from strands_tools import calculator, current_time

from pprint import pprint


# Tool personalizada: el docstring y los type hints son lo que el modelo
# lee para decidir cuándo y cómo usar esta herramienta.
@tool
def letter_counter(word: str, letter: str) -> int:
    """
    Cuenta cuántas veces aparece una letra en una palabra.

    Args:
        word (str): La palabra donde buscar
        letter (str): La letra a contar (un solo carácter)

    Returns:
        int: Número de veces que aparece la letra
    """
    if not isinstance(word, str) or not isinstance(letter, str):
        return 0
    if len(letter) != 1:
        raise ValueError("El parámetro 'letter' debe ser un solo carácter")
    return word.lower().count(letter.lower())



local_model = LlamaCppModel(
    base_url="http://192.168.2.29:8080",
    model_id="qwen3.8-27b",
    params={
        "max_tokens": 3000,
        "temperature": 0.7,
        "repeat_penalty": 1.1,
    }
)

agent = Agent(
    system_prompt = "Eres un asistente util que response en español.",
    tools=[calculator, current_time, letter_counter],
    model=local_model,
)
message = """
Tengo 3 preguntas:
1. Que hora es ahora mismo?
2. Calcula 1024/16
3. Cuantas letras R hay en la palabra strawberry?
"""
result = agent(message)

print("\n-- Metrics --")
pprint(result.metrics.get_summary())
