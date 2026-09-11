# Agent Patterns with Strands

Este directorio contiene ejemplos de diferentes **patrones de agentes** implementados con el framework Strands. Los patrones describen formas comunes de estructurar y coordinar múltiples agentes para resolver problemas.

---

## 📚 Patrones Incluidos

### 1. **Sequential Pattern** - `01-sequential-pattern.py`

Los agentes se ejecutan **uno después del otro en secuencia**. La salida de un agente es entrada del siguiente.

**Estructura:**
```
Investigador → Analista → Escritor → Editor
```

**Características:**
- ✓ Simple de entender y debuggear
- ✓ Orden determinístico
- ✓ Cada etapa añade valor
- ✗ Lento (serie, no paralelo)
- ✗ Un fallo detiene todo

**Casos de Uso:**
- Procesamiento de documentos
- Análisis en fases
- Pipelines de transformación
- Workflows lineales

**Ejecución:**
```bash
python 01-sequential-pattern.py
```

---

### 2. **Parallel Pattern** - `02-parallel-pattern.py`

Múltiples agentes **ejecutan tareas simultáneamente en paralelo**. Ideal cuando las tareas son independientes.

**Estructura:**
```
         ┌─→ Technical Analyst
Topic ──┤─→ Business Analyst
         ├─→ Security Analyst
         └─→ UX Analyst
```

**Características:**
- ✓ Más rápido (paralelo)
- ✓ Análisis desde múltiples ángulos
- ✓ Máxima utilización de recursos
- ✗ Más complejo de implementar
- ✗ Difícil de debuggear

**Casos de Uso:**
- Análisis multi-perspectiva
- Recolección de datos paralela
- Validación desde múltiples ángulos
- Evaluaciones simultáneas

**Ejecución:**
```bash
python 02-parallel-pattern.py
```

**Beneficio:** Ver aceleración en tiempo de ejecución (ej: 4x más rápido)

---

### 3. **Hierarchical Pattern** - `03-hierarchical-pattern.py`

Un agente **supervisor** coordina y delega tareas a agentes **subordinados**. Estructura organizacional clara.

**Estructura:**
```
                    Supervisor
                        │
        ┌───────────────┼───────────────┐
        │               │               │
    Frontend        Backend          DevOps
   Specialist      Specialist       Specialist
```

**Características:**
- ✓ Estructura clara y escalable
- ✓ Fácil delegación
- ✓ Decisiones centralizadas
- ✗ Cuello de botella en supervisor
- ✗ Menos flexible

**Casos de Uso:**
- Proyectos grandes
- Estructuras organizacionales
- Toma de decisiones centralizada
- Escalabilidad controlada

**Ejecución:**
```bash
python 03-hierarchical-pattern.py
```

---

### 4. **Debate Pattern** - `04-debate-pattern.py`

Múltiples agentes con **perspectivas diferentes debaten** para llegar a consenso o clarificar posiciones.

**Estructura:**
```
Proponent vs Skeptic vs Pragmatist
         ↓
    Moderator
         ↓
   Consensus/Vote
```

**Características:**
- ✓ Múltiples perspectivas
- ✓ Decisiones bien fundamentadas
- ✓ Identifica riesgos y oportunidades
- ✗ Consume tiempo
- ✗ Puede llevar a parálisis

**Casos de Uso:**
- Decisiones importantes
- Análisis de riesgos
- Validación de ideas
- Brainstorming estructurado
- Resolución de conflictos

**Ejecución:**
```bash
python 04-debate-pattern.py
```

---

### 5. **Reactive Pattern** - `05-reactive-pattern.py`

Los agentes **reaccionan a eventos específicos** disparados por el sistema. Arquitectura basada en eventos.

**Estructura:**
```
Event Queue
    │
    ├─→ Event 1 ─→ [Load Monitor, Customer Support]
    ├─→ Event 2 ─→ [Security Monitor]
    ├─→ Event 3 ─→ [Analytics Monitor]
    └─→ Event N ─→ [Relevant Agents]
```

**Características:**
- ✓ Respuesta rápida a eventos
- ✓ Escalable (agregar agentes = manejar nuevos eventos)
- ✓ Desacoplamiento entre componentes
- ✗ Complejo de debuggear
- ✗ Orden de procesamiento importa

**Casos de Uso:**
- Monitoreo de sistemas
- Alertas en tiempo real
- Respuesta a incidentes
- Sistemas reactivos
- Procesamiento de streams

**Ejecución:**
```bash
python 05-reactive-pattern.py
```

---

### 6. **Specialist Pattern** - `06-specialist-pattern.py`

Cada agente es **especialista en un dominio específico**. Los especialistas colaboran para resolver problemas complejos.

**Estructura:**
```
Problem
   ↓
┌──────────────────────────────┐
│  Specialist Consultancy      │
├──────────────────────────────┤
│ • Architect                  │
│ • Database Expert            │
│ • Security Expert            │
│ • Performance Expert         │
└──────────────────────────────┘
   ↓
Integrated Recommendation
```

**Características:**
- ✓ Profundidad de expertise
- ✓ Soluciones completas
- ✓ Recomendaciones balanceadas
- ✗ Requiere coordinación
- ✗ Puede ser lento

**Casos de Uso:**
- Consultoría
- Equipos de expertos
- Problemas complejos multi-dominio
- Auditorías
- Diseño de sistemas

**Ejecución:**
```bash
python 06-specialist-pattern.py
```

---

## 7. **Judge/Evaluator Pattern** - `07-judge-pattern.py`

Un agente "juez" evalúa y valida el trabajo de otros agentes, garantizando calidad y consistencia.

**Estructura:**
```
Agent 1 ─┐
Agent 2 ─┼→ Submission → Judge → Judgment (✓/✗)
Agent 3 ─┘
```

**Características:**
- ✓ Garantiza calidad consistente
- ✓ Feedback constructivo
- ✓ Establece estándares
- ✗ Agrega latencia
- ✗ Requiere criterios claros

**Casos de Uso:**
- Validación de calidad
- Revisión de código
- Auditoría y compliance
- Control de contenido

**Ejecución:**
```bash
python 07-judge-pattern.py
```

---

## 8. **Routing Pattern** - `08-routing-pattern.py`

Un agente "router" clasifica y dirige solicitudes al especialista correcto, optimizando eficiencia.

**Estructura:**
```
Request → Router → Classify → Route → Specialist Agent → Response
```

**Características:**
- ✓ Optimiza eficiencia
- ✓ Dirige al experto correcto
- ✓ Escalable
- ✗ Clasificación imperfecta
- ✗ Overhead de clasificación

**Casos de Uso:**
- Customer support routing
- Task delegation
- Load balancing
- Service distribution

**Ejecución:**
```bash
python 08-routing-pattern.py
```

---

## 9. **Self-Critique Pattern** - `09-self-critique-pattern.py`

Un agente genera contenido, se auto-critica iterativamente y mejora hasta alcanzar calidad aceptable.

**Estructura:**
```
Generate → Critique → Quality OK? (Yes → Done, No → Revise) ↻
```

**Características:**
- ✓ Mejora iterativa de calidad
- ✓ Auto-corrección automática
- ✓ Transparencia en proceso
- ✗ Lentitud (múltiples iteraciones)
- ✗ Costo computacional

**Casos de Uso:**
- Mejora de escritura
- Generación de código
- Análisis profundo
- Creative content generation

**Ejecución:**
```bash
python 09-self-critique-pattern.py
```

---

## 10. **Ensemble Pattern** - `10-ensemble-pattern.py`

Múltiples agentes con perspectivas diferentes responden la misma pregunta, luego se sintetizan/votan.

**Estructura:**
```
Question → [Conservative, Optimistic, Analytical, Pragmatic]
             ↓ (todas responden)
          Synthesis → Final Answer
```

**Características:**
- ✓ Reduce bias individual
- ✓ Decisiones más robustas
- ✓ Múltiples perspectivas
- ✗ Costo computacional (4 agentes)
- ✗ Lentitud

**Casos de Uso:**
- Decisiones críticas
- Predicciones importantes
- Análisis de riesgos
- Validación de recomendaciones

**Ejecución:**
```bash
python 10-ensemble-pattern.py
```

---

## 🎯 Tabla Comparativa de Patrones (Completa)

| Patrón | Velocidad | Complejidad | Escala | Mejor Para |
|--------|-----------|-------------|--------|-----------|
| **Sequential** | Lento | Baja | Pequeño | Pipelines simples |
| **Parallel** | Rápido | Media | Medio | Análisis multi-perspectiva |
| **Hierarchical** | Medio | Media | Grande | Organizaciones grandes |
| **Debate** | Lento | Media | Pequeño | Decisiones críticas |
| **Reactive** | Muy Rápido | Alta | Muy Grande | Sistemas en tiempo real |
| **Specialist** | Lento | Alta | Medio | Problemas complejos |
| **Judge** | Medio | Media | Medio | Validación de calidad |
| **Routing** | Rápido | Baja | Muy Grande | Distribución eficiente |
| **Self-Critique** | Lento | Baja | Pequeño | Mejora iterativa |
| **Ensemble** | Muy Lento | Muy Alta | Pequeño | Decisiones críticas |

---

## 🚀 Ejecutar Todos los Patrones

### Opción 1: Ejecutar uno por uno
```bash
# Patrones básicos (1-6)
python 01-sequential-pattern.py
python 02-parallel-pattern.py
python 03-hierarchical-pattern.py
python 04-debate-pattern.py
python 05-reactive-pattern.py
python 06-specialist-pattern.py

# Patrones adicionales (7-10)
python 07-judge-pattern.py
python 08-routing-pattern.py
python 09-self-critique-pattern.py
python 10-ensemble-pattern.py
```

### Opción 2: Script para ejecutar todos
```bash
for file in 0*.py; do
    echo "Ejecutando $file..."
    python "$file"
    echo "---"
done
```

---

## 📊 Matriz de Decisión: Qué Patrón Usar

```
¿Necesitas evaluar/validar trabajo?
├─ SÍ → JUDGE PATTERN
└─ NO → ¿Necesitas enrutar a especialistas?
       ├─ SÍ → ROUTING PATTERN
       └─ NO → ¿Necesitas mejorar iterativamente?
              ├─ SÍ → SELF-CRITIQUE PATTERN
              └─ NO → ¿Las tareas son independientes?
                     ├─ SÍ → ¿Necesitas análisis rápido?
                     │       ├─ SÍ → PARALLEL PATTERN
                     │       └─ NO → Continuación...
                     └─ NO → ¿Hay un orden específico?
                            ├─ SÍ → SEQUENTIAL PATTERN
                            └─ NO → ¿Necesitas estructura?
                                   ├─ SÍ → HIERARCHICAL PATTERN
                                   └─ NO → ¿Basado en eventos?
                                          ├─ SÍ → REACTIVE PATTERN
                                          └─ NO → ¿Necesitas múltiples perspectivas?
                                                 ├─ SÍ → ¿Decisión crítica?
                                                 │       ├─ SÍ → ENSEMBLE PATTERN
                                                 │       └─ NO → DEBATE PATTERN
                                                 └─ NO → SPECIALIST PATTERN
```

---

## 🔄 Comparación: Secuencial vs Paralelo

### Sequential Pattern (01-sequential-pattern.py)
```
Time: ████████████████████████████ (30 sec)
         Researcher (7s) + Analyst (8s) + Writer (8s) + Editor (7s)
```

### Parallel Pattern (02-parallel-pattern.py)
```
Time: ████████ (8 sec)
       4 análisis simultáneamente
```

**Aceleración: ~3.75x más rápido** ⚡

---

## 📖 Conceptos Clave

### 1. **Orchestration**
La coordinación central de múltiples agentes. Ejemplos:
- Supervisor en Hierarchical
- Moderator en Debate
- Coordinator en Specialist

### 2. **Communication**
Cómo se comunican los agentes:
- Sequential: Salida → Entrada
- Parallel: Resultados combinados
- Reactive: Event → Action
- Specialist: Cross-consultation

### 3. **Scalability**
Cómo crece el patrón:
- Sequential: Lineal (más tareas = más tiempo)
- Parallel: Sublineal (más agentes = poco overhead)
- Hierarchical: Exponencial (más niveles)
- Reactive: Lineal (más eventos)

### 4. **Resilience**
Cómo maneja fallos:
- Sequential: Falla total si uno falla
- Parallel: Solo falla ese análisis
- Hierarchical: Falla en esa rama
- Reactive: Los otros eventos se procesan
- Debate: Continúa sin el que falló

---

## 🏆 Mejores Prácticas

### Elegir el Patrón Correcto
1. **Entender el problema**: ¿Qué necesitas resolver?
2. **Mapear dependencias**: ¿Qué debe suceder antes que qué?
3. **Considerar velocidad**: ¿Necesitas respuesta rápida?
4. **Pensar en escala**: ¿Cuántos agentes?
5. **Evaluar complejidad**: ¿Puedes mantenerlo?

### Implementar Patrones
1. **Claro y simple**: Comienza simple, agrega complejidad si es necesario
2. **Logging**: Registra todo para debugging
3. **Timeouts**: Prevén agentes que se cuelguen
4. **Error handling**: Gestiona fallos gracefully
5. **Monitoring**: Supervisa performance y calidad

---

## 🧪 Testing Patrones

Cada patrón tiene características únicas que necesitan testing:

```python
# Sequential: Verificar que el orden es correcto
assert output_1.used_in(output_2)  # Output de paso 1 usado en paso 2

# Parallel: Verificar que todos los análisis se ejecutan
assert len(analyses) == num_agents

# Hierarchical: Verificar delegación correcta
assert task.assigned_to == correct_specialist

# Debate: Verificar que hay consenso o claridad
assert len(votes) == num_participants

# Reactive: Verificar que eventos se procesan
assert len(event_log) == num_events

# Specialist: Verificar síntesis de perspectivas
assert recommendation_includes(all_specialist_inputs)
```

---

## 📈 Evolución de Patrones

Es común **combinar patrones**:

```
Ejemplo: Sistema de e-commerce
├─ HIERARCHICAL (Supervisor)
│   ├─ Frontend Team (Hierarchical)
│   ├─ Backend Team (Hierarchical)
│   └─ DevOps Team (Hierarchical)
│       └─ Monitoreo (Reactive)
│
└─ SPECIALIST (Para decisiones arquitectónicas)
    ├─ Architect
    ├─ Database Expert
    └─ Security Expert
        └─ Debate (Sobre trade-offs)
```

---

## 📚 Referencias

- [Strands Framework Documentation](https://github.com/strands-ai/strands)
- [Agent Design Patterns](https://www.anthropic.com/research)
- [Multi-Agent Systems](https://en.wikipedia.org/wiki/Multi-agent_system)
- [Reactive Programming](https://en.wikipedia.org/wiki/Reactive_programming)

---

## 🎓 Orden Recomendado de Aprendizaje

1. **Comenzar con lo simple**: `01-sequential-pattern.py`
2. **Entender paralelismo**: `02-parallel-pattern.py`
3. **Añadir estructura**: `03-hierarchical-pattern.py`
4. **Introducir debate**: `04-debate-pattern.py`
5. **Sistemas reactivos**: `05-reactive-pattern.py`
6. **Especialización**: `06-specialist-pattern.py`

Cada patrón construye sobre conceptos anteriores.

---

## 💡 Próximos Pasos

1. **Experimenta**: Modifica ejemplos para tu caso de uso
2. **Combina**: Mezcla patrones para tu problema específico
3. **Optimiza**: Mide performance y mejora
4. **Extiende**: Agrega nuevos tipos de agentes
5. **Produce**: Implementa en tu aplicación real
