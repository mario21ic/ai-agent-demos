from strands import Agent
from strands.models import BedrockModel
from strands.models.model import CacheConfig


model = BedrockModel(
    model_id="global.anthropic.claude-sonnet-4-6",
    region_name="us-east-1",
    cache_config=CacheConfig(
        strategy="auto",
        ttl="5m",
    ),
)

agent = Agent(
    model=model,
    system_prompt=(
        "Eres un asistente AWS especializado en incidentes de producción. "
        * 500
    ),
)

result1 = agent("¿Cómo diagnostico throttling en Bedrock?")
result2 = agent("¿Cómo diagnostico latencia elevada en Bedrock?")

for number, result in enumerate((result1, result2), start=1):
    usage = result.metrics.accumulated_usage

    print(f"Invocación {number}")
    print("Cache write:", usage.get("cacheWriteInputTokens", 0))
    print("Cache read: ", usage.get("cacheReadInputTokens", 0))
