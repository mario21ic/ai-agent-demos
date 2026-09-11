# Agent-to-Agent (A2A) Communication with Strands

Este directorio contiene ejemplos de comunicación entre agentes usando el framework Strands.

## Ejemplos

### 1. **01-simple-a2a.py** - Comunicación Básica
Ejemplo más simple: un **Investigador** pregunta y un **Experto** responde.

```bash
python 01-simple-a2a.py
```

**Concepto clave:**
- 2 agentes con roles específicos
- Ciclo simple de pregunta-respuesta
- Perfecto para empezar

---

### 2. **02-a2a-with-tools.py** - Con Herramientas Externas
Agentes que usan tools (http_request, current_time) en su comunicación.

```bash
python 02-a2a-with-tools.py
```

**Concepto clave:**
- **Research Phase**: Investigador recopila datos con tools
- **Analysis Phase**: Analista procesa la información
- **Validation Phase**: Investigador valida resultados

**Flujo workflow:**
```
Researcher (con tools) → Analysis → Validation
```

---

### 3. **03-a2a-with-sessions.py** - Sesiones Persistentes
Comunicación A2A que se guarda y puede retomarse.

```bash
python 03-a2a-with-sessions.py
```

**Concepto clave:**
- Conversaciones persistentes en disco
- Historial guardado automáticamente
- Resumidor de conversaciones largas
- Retomable en otra sesión

**Caso de uso:**
- Lecciones interactivas
- Mentoring a largo plazo
- Sesiones que toman múltiples días

---

### 4. **04-multi-agent-orchestration.py** - Múltiples Agentes
4 agentes especializados en un equipo completo.

```bash
python 04-multi-agent-orchestration.py
```

**Agentes:**
1. **PM** (Product Manager): Define requerimientos
2. **Tech Lead**: Evalúa factibilidad
3. **Engineer**: Estima implementación
4. **QA Lead**: Planifica testing

**Flujo:**
```
PM → Tech Lead → Engineer → QA → PM (decision final)
```

---

## Conceptos de A2A

### ¿Qué es Agent-to-Agent Communication?
- Dos o más agentes intercambian mensajes
- Cada agente tiene un rol/especialización específico
- Los agentes pueden tener acceso a diferentes tools
- El contexto se pasa entre agentes

### Casos de Uso

| Ejemplo | Caso de Uso |
|---------|-----------|
| 01-simple | Preguntas y respuestas simples |
| 02-with-tools | Investigación y análisis de datos |
| 03-with-sessions | Tutorías y mentoring |
| 04-multi-agent | Reuniones de equipo, flujos de trabajo |

---

## Ejecución

### Prerrequisitos
```bash
pip install strands strands-tools
```

### Ejecutar todos los ejemplos
```bash
# Desde el directorio a2a/
for file in 0*.py; do
    echo "Running $file..."
    python "$file"
    echo "---"
done
```

### Ejecutar uno específico
```bash
python 01-simple-a2a.py
```

---

## Estructura de un Agente A2A

```python
from strands import Agent

agent = Agent(
    system_prompt="Descripción del rol del agente",
    tools=[optional_tools],
    conversation_manager=optional_manager,
    session_manager=optional_session
)

# Comunicación
response = agent("Mensaje de otro agente")
```

---

## Tips para A2A

1. **Roles claros**: Define bien el sistema prompt de cada agente
2. **Context passing**: Pasa contexto completo entre agentes
3. **Tool distribution**: Considera qué tools necesita cada agente
4. **Session management**: Usa sesiones para conversaciones largas
5. **Message format**: Estructura bien los mensajes entre agentes

---

## Próximos Pasos

- Experimenta combinando agentes
- Crea flujos de trabajo personalizados
- Agrega más agentes especializados
- Implementa validación entre agentes
