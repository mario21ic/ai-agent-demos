import os
import uuid

from strands import Agent, tool
from strands.models.ollama import OllamaModel
from strands_tools import calculator, current_time

from redisvl.extensions.cache.llm import SemanticCache
from redisvl.utils.vectorize import OllamaTextVectorizer

from pprint import pprint
from dotenv import load_dotenv

from langfuse import get_client, propagate_attributes  # noqa: E402


load_dotenv()

langfuse = get_client()
if not langfuse.auth_check():
    raise RuntimeError("Credenciales de Langfuse inválidas. Revisa tu .env")


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
    temperature=0.7,
)

# Cache semántico en Redis: si llega una pregunta parecida a una anterior
# (distancia coseno <= distance_threshold) se devuelve la respuesta guardada
# sin llamar al modelo ni ejecutar las tools.
# Requiere Redis con RediSearch (redis-stack, ver compose.yml) y Ollama local
# con el modelo de embeddings: `ollama pull nomic-embed-text`.
cache = SemanticCache(
    name="agent_ollama_langfuse_cache",
    redis_url="redis://localhost:6379",
    distance_threshold=0.1,
    ttl=3600,  # segundos
    vectorizer=OllamaTextVectorizer(model="nomic-embed-text", host="http://localhost:11434"),
)


agent = Agent(
    system_prompt = "Eres un asistente util que response en español.",
    tools=[calculator, current_time, letter_counter],
    model=local_model,
)


def ask(pregunta: str, *, user_id: str, session_id: str) -> str:
    """Una llamada = un trace. La conversación completa = una session."""
    with langfuse.start_as_current_observation(
        as_type="agent",
        name="responder-consulta",
        input=pregunta,
    ) as root:
        with propagate_attributes(
            user_id=user_id,
            session_id=session_id,
            tags=["strands", "ollama", "semantic-cache"],
            metadata={
                "model_id": local_model.get_config()["model_id"],
                "ollama_host": os.getenv("OLLAMA_HOST", "http://localhost:11434"),
            },
            version=os.getenv("APP_VERSION", "0.1.0"),
        ):
            hits = cache.check(prompt=pregunta)
            if hits:
                print(f"[cache HIT] distancia={hits[0]['vector_distance']}")
                respuesta = hits[0]["response"]
                root.update(
                    output=respuesta,
                    metadata={"cache_hit": True, "cache_distance": hits[0]["vector_distance"]},
                )
                return respuesta

            print("[cache MISS] consultando al agente...")
            respuesta = str(agent(pregunta))
            cache.store(prompt=pregunta, response=respuesta)

        root.update(output=respuesta, metadata={"cache_hit": False})
        return respuesta



if __name__ == "__main__":
    session_id = f"cli-{uuid.uuid4()}"
    try:
        ask(
            # "Dime acerca de Strands agents.",
            #"Dime acerca del protocolo anget to agents desarrollado por Google.",
            #"Dime acerca del protocolo MCP por Anthropic.",
            """
            Tengo 3 preguntas:
            1. Que hora es ahora mismo en Lima?
            2. Calcula 1024/32
            3. Cuantas letras R hay en la palabra strawberry?
            """,
            user_id=os.getenv("APP_USER_ID", "mario"),
            session_id=session_id,
        )
        """
        result = agent(message)

        print("\n-- Metrics --")
        pprint(result.metrics.get_summary())
        """
    finally:
        langfuse.flush()
