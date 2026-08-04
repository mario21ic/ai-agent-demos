from __future__ import annotations

import os
from typing import Any

from botocore.exceptions import BotoCoreError, ClientError
from strands import Agent
from strands.models import BedrockModel
from strands.types.content import SystemContentBlock


AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

# Usa un modelo que tenga Prompt Caching habilitado en tu región/cuenta.
MODEL_ID = os.getenv(
    "BEDROCK_MODEL_ID",
    "global.anthropic.claude-sonnet-4-6",
    # "us.anthropic.claude-sonnet-4-6",
    # "global.amazon.nova-2-lite-v1:0",
    # "us.amazon.nova-2-lite-v1:0",
)


# En un proyecto real, esto podría contener:
# - políticas empresariales;
# - documentación técnica;
# - instrucciones extensas;
# - catálogos de productos;
# - runbooks;
# - ejemplos few-shot.
#
# Para que la demostración supere el mínimo cacheable del modelo,
# ampliamos artificialmente el contenido estático.
BASE_INSTRUCTIONS = """
Eres un asistente SRE especializado en AWS y Kubernetes.

Reglas operativas:

1. Primero recopila evidencia y después propone cambios.
2. Nunca inventes nombres de recursos, métricas ni resultados.
3. Diferencia claramente observaciones, hipótesis y conclusiones.
4. Para incidentes de Kubernetes revisa pods, eventos, logs,
   deployments, probes, recursos y cambios recientes.
5. Para incidentes de AWS revisa métricas, logs, cuotas,
   throttling, permisos IAM y dependencias.
6. No recomiendes acciones destructivas sin advertir sus riesgos.
7. Prioriza acciones reversibles y con bajo blast radius.
8. Incluye una validación posterior a cada remediación.
9. Responde en español.
10. Presenta la respuesta con diagnóstico, evidencia,
    recomendación y validación.
""".strip()

# Solo para la demostración. En producción debería ser contenido
# estático real, no texto duplicado.
LONG_STATIC_PROMPT = "\n\n".join(
    f"Sección operativa {number}:\n{BASE_INSTRUCTIONS}"
    for number in range(1, 14)
)


def get_cache_usage(result: Any) -> dict[str, int]:
    """Extrae las métricas de prompt caching de una respuesta Strands."""
    usage = getattr(
        getattr(result, "metrics", None),
        "accumulated_usage",
        {},
    ) or {}

    return {
        "input_tokens": usage.get("inputTokens", 0),
        "output_tokens": usage.get("outputTokens", 0),
        "cache_write_tokens": usage.get("cacheWriteInputTokens", 0),
        "cache_read_tokens": usage.get("cacheReadInputTokens", 0),
    }


def print_cache_usage(label: str, result: Any) -> None:
    usage = get_cache_usage(result)

    print(f"\n--- {label} ---")
    print(f"Input tokens:       {usage['input_tokens']}")
    print(f"Output tokens:      {usage['output_tokens']}")
    print(f"Cache write tokens: {usage['cache_write_tokens']}")
    print(f"Cache read tokens:  {usage['cache_read_tokens']}")


def create_agent() -> Agent:
    model = BedrockModel(
        model_id=MODEL_ID,
        region_name=AWS_REGION,
        max_tokens=600,
        temperature=0.1,
    )

    # Todo lo anterior al cachePoint forma el prefijo cacheable.
    system_prompt = [
        SystemContentBlock(text=LONG_STATIC_PROMPT),
        SystemContentBlock(
            cachePoint={
                "type": "default"
            }
        ),
    ]

    return Agent(
        model=model,
        system_prompt=system_prompt,
    )


def main() -> None:
    agent = create_agent()

    try:
        print("Primera invocación: escribe el prompt estático en caché.")

        first_result = agent(
            """
            Un deployment de EKS presenta CrashLoopBackOff.
            Dame un procedimiento inicial de diagnóstico.
            """
        )

        print(first_result)
        print_cache_usage("PRIMERA INVOCACIÓN", first_result)

        print("\nSegunda invocación: debería reutilizar el prompt cacheado.")

        second_result = agent(
            """
            Ahora explica cómo investigar un error
            ImagePullBackOff en el mismo clúster.
            """
        )

        print(second_result)
        print_cache_usage("SEGUNDA INVOCACIÓN", second_result)

    except ClientError as exc:
        error = exc.response.get("Error", {})
        print(
            "Error de AWS Bedrock: "
            f"{error.get('Code', 'Unknown')} - "
            f"{error.get('Message', str(exc))}"
        )
        raise

    except BotoCoreError as exc:
        print(f"Error de conexión o configuración AWS: {exc}")
        raise


if __name__ == "__main__":
    main()
