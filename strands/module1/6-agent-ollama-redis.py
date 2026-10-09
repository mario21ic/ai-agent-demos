from strands import Agent, tool

from strands.models.ollama import OllamaModel
from strands_tools import calculator, current_time

from redisvl.extensions.cache.llm import SemanticCache
from redisvl.utils.vectorize import OllamaTextVectorizer

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



local_model = OllamaModel(
    host="http://localhost:11434",
    model_id="gpt-oss:120b-cloud",
    max_tokens=3000,
    temperature=0.7
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

# Cache semántico en Redis: si llega una pregunta parecida a una anterior
# (distancia coseno <= distance_threshold) se devuelve la respuesta guardada
# sin llamar al modelo ni ejecutar las tools.
# Requiere Redis con RediSearch (redis-stack, ver compose.yml) y Ollama local
# con el modelo de embeddings: `ollama pull nomic-embed-text`.
cache = SemanticCache(
    name="agent_llamacpp_cache",
    redis_url="redis://localhost:6379",
    distance_threshold=0.1,
    ttl=3600,  # segundos
    vectorizer=OllamaTextVectorizer(model="nomic-embed-text", host="http://localhost:11434"),
)


def ask(prompt: str) -> str:
    hits = cache.check(prompt=prompt)
    if hits:
        print(f"[cache HIT] distancia={hits[0]['vector_distance']}")
        return hits[0]["response"]
    print("[cache MISS] consultando al agente...")
    response = str(agent(prompt))
    cache.store(prompt=prompt, response=response)
    return response


# Ejecútalo dos veces (o con una pregunta parafraseada) para ver el HIT.
# Para limpiar el cache: cache.clear()
answer = ask(message)
print("\n-- Respuesta --")
print(answer)

#print("\n-- Metrics --")
#pprint(result.metrics.get_summary())
