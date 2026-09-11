# AWS Agentic AI Patterns with Strands

Esta carpeta contiene implementaciones de los **patrones de IA Agentica** descritos en la documentación oficial de AWS usando el framework Strands.

**Referencia Oficial:**
https://docs.aws.amazon.com/es_es/prescriptive-guidance/latest/agentic-ai-patterns/agent-patterns.html

---

## 🏗️ Principios Fundamentales de AWS

Todos los patrones se construyen sobre tres principios fundamentales:

### 1. **Asincrónico** (Asynchronous)
- Los agentes operan en entornos desacoplados
- Procesamiento basado en eventos
- No bloquean en operaciones largas
- Escalables a múltiples solicitudes

### 2. **Autonomía** (Autonomy)
- Agentes actúan sin intervención humana
- Toman decisiones independientes
- Tienen capacidad de razonamiento
- No requieren aprobación en cada paso

### 3. **Agencia** (Agency)
- Agentes actúan con propósito
- En nombre de usuarios o sistemas
- Para lograr objetivos específicos
- Con intención clara

---

## 📋 Patrones Implementados

### 1. **Basic Reasoning Agent** - `01-basic-reasoning-agent.py`

**Descripción:**
Agente que realiza razonamiento profundo sobre problemas complejos sin acceso a herramientas externas.

**Características:**
- ✓ Razonamiento paso a paso
- ✓ Descomposición de problemas
- ✓ Evaluación de opciones
- ✓ Justificación de decisiones

**Ejemplo de Salida:**
```
Problem: Elegir arquitectura de microservicios

1. Understanding: [Analiza problema]
2. Options: [Genera 3 enfoques]
3. Evaluation: [Evalúa cada uno]
4. Decision: [Recomendación final]
```

**Casos de Uso:**
- Análisis de problemas abstractos
- Toma de decisiones estratégica
- Evaluación de opciones
- Brainstorming estructurado

**Ejecución:**
```bash
python 01-basic-reasoning-agent.py
```

---

### 2. **Tool-based Agent for Functions** - `02-tool-based-agent-functions.py`

**Descripción:**
Agente que llama funciones/herramientas para completar tareas prácticas y obtener datos en tiempo real.

**Características:**
- ✓ Determina qué herramientas usar
- ✓ Encadena múltiples llamadas
- ✓ Procesa resultados
- ✓ Toma decisiones basadas en datos

**Herramientas Disponibles:**
```python
- current_time()        # Obtiene hora actual
- http_request(url)     # Hace solicitudes HTTP
```

**Casos de Uso:**
- Obtención de datos en tiempo real
- Integración con APIs externas
- Ejecución de acciones
- Automatización de procesos

**Ejecución:**
```bash
python 02-tool-based-agent-functions.py
```

---

### 3. **Workflow Orchestration Agent** - `03-workflow-orchestration-agent.py`

**Descripción:**
Agente que orquesta flujos de trabajo complejos coordinando múltiples pasos, dependencias y decisiones.

**Características:**
- ✓ Coordina múltiples pasos
- ✓ Maneja dependencias
- ✓ Recuperación ante errores
- ✓ Toma decisiones sobre bifurcaciones

**Ejemplo de Flujo:**
```
Step 1: Data Ingestion
  ↓ (success)
Step 2: Data Validation
  ↓ (success)
Step 3: Data Processing
  ↓ (success)
Step 4: Quality Check
  ↓ (success)
Step 5: Notification
```

**Casos de Uso:**
- Pipelines de datos ETL
- Procesos de aprobación
- Automatización de empleados
- Orquestación de microservicios

**Ejecución:**
```bash
python 03-workflow-orchestration-agent.py
```

---

### 4. **Memory-augmented Agent** - `04-memory-augmented-agent.py`

**Descripción:**
Agente que mantiene y utiliza memoria persistente de conversaciones previas, aprendizajes y contexto histórico.

**Características:**
- ✓ Recuerda interacciones previas
- ✓ Mejora con experiencia
- ✓ Personalización automática
- ✓ Sesiones persistentes

**Tipos de Memoria:**
- Preferencias aprendidas
- Hechos importantes
- Errores a evitar
- Contexto histórico

**Casos de Uso:**
- Asistentes personales
- Chatbots de servicio al cliente
- Tutores educativos
- Análisis histórico

**Ejecución:**
```bash
python 04-memory-augmented-agent.py
```

---

### 5. **Observer and Monitoring Agent** - `05-observer-monitoring-agent.py`

**Descripción:**
Agente que monitorea sistemas, detecta anomalías y actúa sobre eventos de observación.

**Características:**
- ✓ Monitoreo 24/7
- ✓ Detección automática de anomalías
- ✓ Respuesta rápida a eventos
- ✓ Escalable a múltiples sistemas

**Métricas Monitoreadas:**
- CPU Usage
- Memory Usage
- Disk Space
- API Latency
- Error Rate
- Throughput

**Casos de Uso:**
- Monitoreo de infraestructura
- Detección de fraude
- Alertas de performance
- Compliance monitoring

**Ejecución:**
```bash
python 05-observer-monitoring-agent.py
```

---

### 6. **Multi-agent Collaboration** - `06-multi-agent-collaboration.py`

**Descripción:**
Múltiples agentes colaboran, negocian y alcanzan consenso para resolver problemas complejos.

**Características:**
- ✓ Perspectivas diversas
- ✓ Evaluación cruzada de propuestas
- ✓ Resolución de conflictos
- ✓ Consenso integrado

**Agentes Involucrados:**
- Backend Engineer
- Frontend Engineer
- DevOps Engineer
- Security Specialist
- Facilitator

**Casos de Uso:**
- Toma de decisiones organizacional
- Diseño de arquitectura
- Revisión de seguridad
- Análisis de impacto
- Resolución de conflictos

**Ejecución:**
```bash
python 06-multi-agent-collaboration.py
```

---

## 📊 Matriz Comparativa de Patrones

| Patrón | Complejidad | Velocidad | Escalabilidad | Mejor Para |
|--------|-------------|-----------|---------------|-----------|
| **Basic Reasoning** | Baja | Lento | Media | Análisis abstracto |
| **Tool-based** | Media | Medio | Alta | APIs y datos reales |
| **Workflow** | Alta | Variable | Muy Alta | Procesos complejos |
| **Memory-augmented** | Media | Medio | Alta | Personalización |
| **Observer/Monitoring** | Alta | Rápido | Muy Alta | Monitoreo 24/7 |
| **Multi-agent Collab** | Muy Alta | Lento | Media | Decisiones complejas |

---

## 🚀 Ejecución de Patrones

### Ejecutar Individual
```bash
# Basic Reasoning
python 01-basic-reasoning-agent.py

# Tool-based
python 02-tool-based-agent-functions.py

# Workflow Orchestration
python 03-workflow-orchestration-agent.py

# Memory-augmented
python 04-memory-augmented-agent.py

# Observer/Monitoring
python 05-observer-monitoring-agent.py

# Multi-agent Collaboration
python 06-multi-agent-collaboration.py
```

### Ejecutar Todos
```bash
for file in 0*.py; do
    echo "Running $file..."
    python "$file"
    echo "---"
done
```

---

## 🏆 Matriz de Decisión: Qué Patrón Usar

```
¿Necesitas razonamiento sin herramientas?
├─ SÍ → BASIC REASONING AGENT
└─ NO → ¿Necesitas acceso a datos/APIs?
       ├─ SÍ → TOOL-BASED AGENT
       └─ NO → ¿Necesitas orquestar múltiples pasos?
              ├─ SÍ → WORKFLOW ORCHESTRATION
              └─ NO → ¿Necesitas memoria persistente?
                     ├─ SÍ → MEMORY-AUGMENTED
                     └─ NO → ¿Necesitas monitoreo continuo?
                            ├─ SÍ → OBSERVER/MONITORING
                            └─ NO → ¿Múltiples perspectivas?
                                   ├─ SÍ → MULTI-AGENT COLLAB
                                   └─ CUSTOM SOLUTION
```

---

## 🔗 Integración con AWS Services

Cada patrón corresponde a servicios específicos de AWS:

| Patrón | AWS Services |
|--------|--------------|
| **Basic Reasoning** | Bedrock, SageMaker |
| **Tool-based** | Lambda, API Gateway, Bedrock |
| **Workflow** | Step Functions, Bedrock |
| **Memory-augmented** | DynamoDB, Bedrock |
| **Observer/Monitoring** | CloudWatch, EventBridge, Bedrock |
| **Multi-agent Collab** | SQS, SNS, Bedrock |

---

## 💡 Mejores Prácticas

### 1. **Elegir el Patrón Correcto**
- Entender el problema antes de elegir
- Considerar restricciones (tiempo, presupuesto, escalabilidad)
- Estar dispuesto a combinar patrones

### 2. **Implementar Robustez**
- Error handling en cada paso
- Timeouts apropiados
- Fallback strategies
- Logging completo

### 3. **Optimizar Performance**
- Paralelizar cuando sea posible
- Cachear resultados
- Batch processing
- Asincronía

### 4. **Monitorear y Observar**
- Metrics de rendimiento
- Alertas en tiempo real
- Auditoría de decisiones
- Feedback de usuarios

### 5. **Seguridad**
- Validación de inputs
- Control de acceso
- Encriptación de datos
- Compliance

---

## 📈 Evolución de Patrones

Es común **combinar patrones** en aplicaciones reales:

```
Ejemplo: Sistema de Recomendaciones
├─ WORKFLOW ORCHESTRATION (orquestar flujo)
│   ├─ TOOL-BASED AGENT (obtener datos de usuario)
│   ├─ BASIC REASONING AGENT (analizar preferencias)
│   └─ OBSERVER AGENT (monitorear relevancia)
│
└─ MULTI-AGENT COLLAB (resolver conflictos de recomendación)
    ├─ Content Specialist
    ├─ Performance Specialist
    └─ Privacy Specialist
```

---

## 🧪 Testing Patrones

Cada patrón necesita testing específico:

### Basic Reasoning
```python
# Verificar que el razonamiento es lógico
assert "therefore" in reasoning_output  # Contiene conclusión
assert len(options) >= 3  # Genera múltiples opciones
```

### Tool-based
```python
# Verificar que las herramientas se llamaron
assert tool_calls >= 1
assert results_processed == True
```

### Workflow
```python
# Verificar orden de ejecución
assert execution_order == expected_order
assert all_dependencies_met == True
```

### Memory-augmented
```python
# Verificar persistencia
assert memory_retrieved == True
assert improvement_over_time == True
```

### Observer/Monitoring
```python
# Verificar detección de anomalías
assert anomalies_detected >= threshold
assert response_time < SLA
```

### Multi-agent Collaboration
```python
# Verificar consenso
assert consensus_reached == True
assert all_perspectives_considered == True
```

---

## 📚 Referencia de Conceptos

### Asincronía en Patrones AWS
- **Basic Reasoning**: Sincrónico (piensa antes de actuar)
- **Tool-based**: Asincrónico (espera resultados de APIs)
- **Workflow**: Asincrónico (pasos pueden esperar)
- **Memory-augmented**: Sincrónico con persistencia asincrónica
- **Observer**: Totalmente asincrónico
- **Multi-agent**: Asincrónico con sincronización

### Autonomía en Patrones
- **Grado bajo**: Basic Reasoning (solo analiza)
- **Grado medio**: Tool-based, Memory-augmented (toma decisiones simples)
- **Grado alto**: Workflow, Observer (toma muchas decisiones)
- **Grado muy alto**: Multi-agent (negocia con otros)

---

## 🔗 Referencias Externas

- [AWS Agentic AI Patterns (Documentación Oficial)](https://docs.aws.amazon.com/es_es/prescriptive-guidance/latest/agentic-ai-patterns/agent-patterns.html)
- [AWS Bedrock](https://aws.amazon.com/es/bedrock/)
- [Amazon Step Functions](https://aws.amazon.com/es/step-functions/)
- [Strands Documentation](https://github.com/strands-ai/strands)

---

## 📝 Notas

- Estos ejemplos son educacionales y demuestran conceptos
- En producción, añadir error handling más robusto
- Considerar costos de API calls y almacenamiento
- Implementar autenticación y autorización adecuadas
- Monitorear y loguear todas las decisiones del agente

---

## 🎯 Próximos Pasos

1. **Entender** cada patrón ejecutando ejemplos
2. **Experimentar** modificando prompts y parámetros
3. **Combinar** patrones para tu caso de uso
4. **Integrar** con servicios de AWS
5. **Deployar** en producción con seguridad y monitoreo
