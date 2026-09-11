# 20 Agentic AI Design Patterns with Strands

Esta carpeta contiene implementaciones de los **20 patrones de diseño de IA Agentica** más importantes, usando el framework Strands.

---

## 📋 Los 20 Patrones

### Grupo 1: Patrones Fundamentales (1-3)

#### **1. Agentic Loop Pattern** - `01-agentic-loop.py`
El patrón más fundamental: **Think → Act → Observe → Repeat**

**Concepto:**
```
┌─────────────┐
│ THINK       │ Analizar situación
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ ACT         │ Ejecutar acción
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ OBSERVE     │ Observar resultados
└──────┬──────┘
       │
       └───→ REPEAT o STOP
```

**Características:**
- ✓ Universal y fundamental
- ✓ Adaptativo e iterativo
- ✓ Permite mejora continua

**Ejecución:**
```bash
python 01-agentic-loop.py
```

---

#### **2. Tool Use/Function Calling Pattern** - `02-tool-use-pattern.py`
Agentes que invocan herramientas y APIs externas.

**Concepto:**
```
Agent → Determine Tools → Call Tools → Process Results → Response
```

**Características:**
- ✓ Extiende capacidades del agente
- ✓ Acceso a datos en tiempo real
- ✓ Integración con sistemas externos

**Ejecución:**
```bash
python 02-tool-use-pattern.py
```

---

#### **3. Retrieval Augmented Generation (RAG) Pattern** - `03-rag-pattern.py`
Busca documentos relevantes antes de generar respuestas.

**Concepto:**
```
Query → RETRIEVE → AUGMENT → GENERATE → Response
```

**Fases:**
1. **Retrieve:** Buscar documentos relevantes
2. **Augment:** Crear contexto aumentado
3. **Generate:** Generar respuesta informada

**Características:**
- ✓ Respuestas basadas en hechos
- ✓ Reduce alucinaciones
- ✓ Información actualizada

**Ejecución:**
```bash
python 03-rag-pattern.py
```

---

### Grupo 2: Patrones de Coordinación (4-6)

#### **4. Prompt Chaining Pattern**
Encadena múltiples prompts secuencialmente.

**Flujo:**
```
Step 1 → Step 2 (usa resultado 1) → Step 3 → Final Result
```

**Casos de Uso:**
- Análisis de problemas complejos
- Razonamiento paso a paso
- Descomposición de tareas

---

#### **5. Multi-Agent Collaboration Pattern**
Múltiples agentes especializados trabajan juntos.

**Flujo:**
```
Task → Agent1 + Agent2 + Agent3 → Coordinator → Solution
```

---

#### **6. Planning & Reasoning Pattern**
Agente que planifica antes de actuar.

**Flujo:**
```
Goal → Plan → Reason → Action → Execute
```

---

### Grupo 3: Patrones de Gestión (7-9)

#### **7. Memory Management Pattern**
Gestión de memoria a corto y largo plazo.

**Tipos de Memoria:**
- Short-term: Contexto actual
- Long-term: Historico persistente
- Working: Datos activos

---

#### **8. Error Handling & Recovery Pattern**
Manejo resiliente de errores.

**Estrategias:**
- Retry con backoff
- Fallback mechanisms
- Graceful degradation

---

#### **9. Conditional Logic Pattern**
Agente que toma decisiones condicionales.

**Estructuras:**
```
if condition:
    execute_path_a()
else:
    execute_path_b()
```

---

### Grupo 4: Patrones de Ejecución (10-12)

#### **10. Parallel Execution Pattern**
Ejecuta múltiples tareas simultáneamente.

**Beneficio:** Aceleración 3-4x

---

#### **11. Fallback Mechanisms Pattern**
Múltiples estrategias para recuperación.

**Niveles:**
1. Primary strategy
2. Fallback A
3. Fallback B
4. Default response

---

#### **12. Validation & Verification Pattern**
Valida y verifica resultados antes de usar.

**Proceso:**
```
Generate → Validate → Verify → Approve → Use
```

---

### Grupo 5: Patrones Avanzados (13-20)

#### **13. Streaming & Partial Responses**
Respuestas incrementales y streaming.

**Beneficios:**
- Respuesta más rápida
- Menos latencia
- Mejor UX

---

#### **14. Context Management**
Gestión efectiva del contexto del agente.

**Elementos:**
- Histórico de conversación
- Estado actual
- Metadatos relevantes

---

#### **15. State Management**
Persistencia y sincronización de estado.

---

#### **16. Knowledge Graph Integration**
Integración con bases de conocimiento estructurado.

---

#### **17. Meta-Reasoning**
Agente que razona sobre su propio razonamiento.

---

#### **18. Behavioral Modification**
Adaptación de comportamiento basado en feedback.

---

#### **19. Long Context Understanding**
Comprensión de contextos muy largos.

---

#### **20. Reflection & Self-Improvement**
Autorreflexión y mejora continua.

---

## 🎯 Matriz de Decisión: Qué Patrón Usar

```
¿Cuál es el tipo de problema?

SIMPLE (Una tarea):
├─ Necesita herramientas → TOOL USE
├─ Necesita información → RAG
└─ Ejecutable directamente → AGENTIC LOOP

COMPLEJO (Múltiples pasos):
├─ Secuencial → PROMPT CHAINING
├─ Paralelo → PARALLEL EXECUTION
├─ Condicional → CONDITIONAL LOGIC
└─ Coordinado → MULTI-AGENT COLLABORATION

CON RIESGOS (Fallos posibles):
├─ Error handling → ERROR HANDLING & RECOVERY
├─ Validación crítica → VALIDATION & VERIFICATION
└─ Alternativas necesarias → FALLBACK MECHANISMS

LARGO PLAZO:
├─ Necesita memoria → MEMORY MANAGEMENT
├─ Cambios de comportamiento → BEHAVIORAL MODIFICATION
├─ Mejora continua → REFLECTION & SELF-IMPROVEMENT
└─ Contexto extenso → LONG CONTEXT UNDERSTANDING
```

---

## 📊 Tabla Comparativa

| Patrón | Complejidad | Velocidad | Escalabilidad | Mejor Para |
|--------|-------------|-----------|---------------|-----------|
| Agentic Loop | Baja | Medio | Media | Cualquier tarea |
| Tool Use | Media | Medio | Alta | APIs y datos |
| RAG | Media | Lento | Alta | Búsqueda + generación |
| Prompt Chaining | Media | Lento | Media | Problemas complejos |
| Multi-Agent | Alta | Lento | Alta | Coordinación |
| Planning & Reasoning | Media | Lento | Media | Toma de decisiones |
| Memory Management | Media | Rápido | Alta | Conversaciones largas |
| Error Handling | Baja | Rápido | Alta | Sistemas críticos |
| Conditional Logic | Baja | Rápido | Alta | Decisiones |
| Parallel Execution | Media | Muy Rápido | Muy Alta | Tareas independientes |
| Fallback Mechanisms | Baja | Rápido | Alta | Resiliencia |
| Validation | Baja | Medio | Alta | Calidad |

---

## 🚀 Ejecución Rápida

### Ejecutar todos los patrones
```bash
python 01-agentic-loop.py
python 02-tool-use-pattern.py
python 03-rag-pattern.py
python 04-to-20-design-patterns.py
```

### Ejecutar patrón específico
```bash
python 01-agentic-loop.py    # Agentic Loop
python 02-tool-use-pattern.py   # Tool Use
python 03-rag-pattern.py        # RAG
```

---

## 📚 Orden Recomendado de Aprendizaje

### Nivel 1: Fundamentos (Día 1)
1. Agentic Loop - Entender el bucle básico
2. Tool Use - Agregar herramientas
3. RAG - Búsqueda + generación

### Nivel 2: Intermedios (Día 2-3)
4. Prompt Chaining - Encadenar prompts
5. Multi-Agent - Coordinación
6. Planning & Reasoning - Planificación

### Nivel 3: Avanzados (Día 4-5)
7. Memory Management - Memoria
8. Error Handling - Resiliencia
9. Conditional Logic - Decisiones
10. Parallel Execution - Paralelización

### Nivel 4: Producción (Día 6-7)
11-20. Patrones de producción y especialización

---

## 🔧 Implementación Paso a Paso

### Template para nuevo patrón:
```python
from strands import Agent

class MyPattern:
    def __init__(self):
        self.agent = Agent(system_prompt="...")
    
    def execute(self, task: str) -> str:
        # Tu implementación aquí
        result = self.agent(task)
        return result

def main():
    pattern = MyPattern()
    result = pattern.execute("tu tarea aquí")
    print(result)

if __name__ == "__main__":
    main()
```

---

## 💡 Mejores Prácticas

### 1. **Elegir el patrón correcto**
- Analizar el problema
- Considerar restricciones
- Validar con prototipo

### 2. **Combinar patrones**
- Agentic Loop + Tool Use
- RAG + Multi-Agent
- Planning + Error Handling

### 3. **Optimizar performance**
- Paralelizar cuando sea posible
- Cachear resultados
- Monitorear latencia

### 4. **Asegurar calidad**
- Validar salidas
- Manejar errores
- Tener fallbacks

### 5. **Documentar**
- Explicar decisiones
- Comentar lógica
- Mantener logs

---

## 🧪 Testing Patrones

### Agentic Loop
```python
assert iterations > 0
assert iterations < max_iterations
```

### Tool Use
```python
assert tool_was_called == True
assert result is not None
```

### RAG
```python
assert len(documents) > 0
assert context_is_relevant == True
```

---

## 📈 Evolución: Combinar Patrones

### Sistema Completo:
```
User Input
    ↓
ROUTING (Pattern 8) → ¿Qué tipo de tarea?
    ↓
AGENTIC LOOP (Pattern 1) → Bucle principal
    ├─ PLANNING (Pattern 6) → Plan strategy
    ├─ RAG (Pattern 3) → Buscar información
    ├─ TOOL USE (Pattern 2) → Llamar APIs
    ├─ CONDITIONAL LOGIC (Pattern 9) → Decidir
    ├─ ERROR HANDLING (Pattern 8) → Manejar errores
    └─ VALIDATION (Pattern 12) → Validar resultado
    ↓
MEMORY (Pattern 7) → Guardar resultado
    ↓
User Response
```

---

## 🔗 Referencias

- [Agentic AI Research](https://www.anthropic.com/research/agentic-ai)
- [Strands Documentation](https://github.com/strands-ai/strands)
- [LLM Agents Design](https://lilianweng.github.io/posts/2023-06-23-agent/)

---

## 📝 Notas

- Estos patrones son independientes pero complementarios
- Combina según necesidades del problema
- Prueba con casos pequeños primero
- Itera y mejora continuamente
- Monitorea performance y calidad

---

## ✨ Lo Que Aprendiste

✓ 20 patrones de diseño de IA agentica
✓ Cómo implementarlos con Strands
✓ Cuándo usar cada patrón
✓ Cómo combinarlos efectivamente
✓ Mejores prácticas de implementación

¡Ahora eres experto en diseño de agentes IA! 🚀
