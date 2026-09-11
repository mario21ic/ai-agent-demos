import os
import uuid

from strands import Agent, tool
from strands.models.llamacpp import LlamaCppModel
from strands_tools import calculator, current_time

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



ollama_model = LlamaCppModel(
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
    model=ollama_model,
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
            tags=["strands", "ollama"],
            metadata={
                "model_id": ollama_model.get_config()["model_id"],
                "ollama_host": os.getenv("OLLAMA_HOST", "http://localhost:11434"),
            },
            version=os.getenv("APP_VERSION", "0.1.0"),
        ):
            result = agent(pregunta)

        respuesta = str(result)
        root.update(output=respuesta)
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
            1. Que hora es ahora mismo?
            2. Calcula 1024/16
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
