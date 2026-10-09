# Ejemplos `6-agent-*`

Todos construyen el mismo agente de Strands con tres tools (`calculator`, `current_time` y la custom `letter_counter`) y le hacen tres preguntas a la vez. Varían en dos ejes: **el modelo** (Bedrock, Ollama o llama.cpp) y **los extras** (observabilidad con Langfuse, cache semántico con Redis, o ambos).

| Archivo | Modelo | Langfuse | Cache Redis |
|---|---|:-:|:-:|
| `6-agent.py` | Por defecto de Strands (Amazon Bedrock) | — | — |
| `6-agent-ollama.py` | Ollama local, `gpt-oss:120b-cloud` | — | — |
| `6-agent-ollama-langfuse.py` | Ollama local, `gpt-oss:120b-cloud` | ✔ | — |
| `6-agent-ollama-redis.py` | Ollama local, `gpt-oss:120b-cloud` | — | ✔ |
| `6-agent-ollama-langfuse-redis.py` | Ollama local, `gpt-oss:120b-cloud` | ✔ | ✔ |
| `6-agent-llamacpp.py` | llama.cpp (`192.168.2.29:8080`, `qwen3.8-27b`) | — | — |
| `6-agent-llamacpp-langfuse.py` | llama.cpp (`192.168.2.29:8080`, `qwen3.8-27b`) | ✔ | — |
| `6-agent-llamacpp-redis.py` | llama.cpp (`192.168.2.29:8080`, `qwen3.8-27b`) | — | ✔ |

Documentación de arquitectura:
- `ARCHITECTURE-6-agent-llamacpp-redis.md`
- `ARCHITECTURE-6-agent-llamacpp-langfuse.md`

## Requisitos por componente

Ejecuta cada ejemplo desde esta carpeta: `python <archivo>`.

| Si el archivo usa… | Necesitas |
|---|---|
| Cualquiera | `pip install strands-agents strands-agents-tools` (o `pip install -r ../requirements.txt`) |
| Bedrock (`6-agent.py`) | Credenciales de AWS y acceso al modelo por defecto en tu región |
| Ollama | Ollama corriendo en `http://localhost:11434` y el modelo disponible (ver abajo) |
| llama.cpp | Servidor accesible en la `base_url` del archivo (ajusta IP/modelo a tu red) |
| Langfuse | `pip install langfuse python-dotenv` y un `.env` (ver abajo) |
| Cache Redis | Redis Stack, `pip install redisvl redis ollama` y `ollama pull nomic-embed-text` (ver abajo) |

### Ollama

1. Instala y arranca Ollama.
2. Los modelos `*-cloud` requieren sesión iniciada: `ollama signin`.
3. Comprueba que existe el modelo: `ollama list` (debe aparecer `gpt-oss:120b-cloud`).

Los parámetros de `OllamaModel` se pasan directo (`max_tokens`, `temperature`). `repeat_penalty` es propio de llama.cpp y no se admite ahí.

### Langfuse

Crea un `.env` en esta carpeta:

```env
LANGFUSE_PUBLIC_KEY=pk-lf-...
LANGFUSE_SECRET_KEY=sk-lf-...
LANGFUSE_HOST=https://cloud.langfuse.com   # o tu instancia
APP_USER_ID=mario          # opcional
APP_VERSION=0.1.0          # opcional
```

Cada llamada a `ask()` genera un trace (`responder-consulta`) con `user_id`, `session_id` (`cli-<uuid>`), tags y metadata. Si las credenciales son inválidas, el script aborta con `Credenciales de Langfuse inválidas`. Al terminar se hace `flush()` para no perder trazas.

### Cache semántico (RedisVL)

Antes de llamar al agente se busca en Redis una pregunta semánticamente parecida. Si existe (distancia ≤ `0.1`), se devuelve la respuesta guardada sin invocar al modelo ni a las tools. Los embeddings los genera Ollama local (`nomic-embed-text`).

```bash
docker compose up -d            # Redis Stack (compose.yml); redis:7-alpine NO sirve, no trae RediSearch
ollama pull nomic-embed-text    # modelo de embeddings
```

Ejecuta el script dos veces (o con una pregunta parafraseada) para ver el HIT:

```
[cache MISS] consultando al agente...   (1ª vez)
[cache HIT] distancia=0.0               (2ª vez)
```

Parámetros ajustables en `SemanticCache(...)`:

- `distance_threshold`: más bajo = más estricto; más alto = más aciertos pero riesgo de respuestas no equivalentes.
- `ttl`: segundos de vida de cada entrada (3600 por defecto).
- Para vaciar el cache: `cache.clear()`.

## Detalles por variante

- **`6-agent-ollama-langfuse-redis.py`**: combina ambos. El cache se consulta *dentro* de la observación raíz de Langfuse, así que los HIT también aparecen como traces (sin spans de modelo ni tools). Usa el tag `semantic-cache` y marca `metadata.cache_hit` (y `cache_distance` en HIT) para medir el hit-rate.
- **`6-agent-ollama-redis.py` y `6-agent-llamacpp-redis.py`**: ambos usan el nombre de índice `agent_llamacpp_cache`, por lo que **comparten cache** aunque usen modelos distintos. Una respuesta guardada por uno la puede servir el otro. Cambia `name=` en uno si quieres aislarlos. El de langfuse-redis usa `agent_ollama_langfuse_cache`.
- **`6-agent.py`**: es el único que imprime métricas (`result.metrics.get_summary()`); en el resto está comentado.

## Problemas frecuentes

- `unknown command 'FT.CREATE'` → Redis sin RediSearch; usa `redis/redis-stack-server`.
- `model "nomic-embed-text" not found` → falta `ollama pull nomic-embed-text`.
- Timeout o connection refused hacia `192.168.2.29:8080` → el servidor llama.cpp no es accesible desde tu red.
- Un HIT devuelve la hora vieja → la respuesta cacheada incluye datos de tools que caducan; espera al TTL o ejecuta `cache.clear()`.

## Notas sobre los scripts de llama.cpp con Langfuse

`6-agent-llamacpp-langfuse.py` conserva nombres heredados de Ollama: la variable `ollama_model`, el tag `"ollama"` y la metadata `ollama_host` (que lee `OLLAMA_HOST`). Describen un servidor que ese script no usa, y pueden confundir al filtrar en Langfuse.
