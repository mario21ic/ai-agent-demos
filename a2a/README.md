# Google A2A Protocol con Strands

Este directorio contiene ejemplos de implementación del **protocolo Agent-to-Agent (A2A) de Google** usando el framework Strands.

## Sobre el Protocolo A2A

El **protocolo A2A (Agent-to-Agent)** es una especificación abierta desarrollada por Google que permite que agentes de IA se comuniquen entre sí de forma estandarizada, independientemente del modelo o framework utilizado.

**Fuentes:**
- [Medium: Google A2A Protocol Explained](https://medium.com/@shamim_ru/google-agent-to-agent-a2a-protocol-explained-with-real-working-examples-99e362b61ba8)
- [Atlan: Google A2A Protocol](https://atlan.com/know/google-a2a-protocol/)
- [GitHub: A2A Project](https://github.com/a2aproject/A2A)

---

## Conceptos Clave del Protocolo A2A

### 1. **AgentCard**
Documento JSON que sirve desde `/.well-known/agent.json` y describe:
- Identidad del agente (nombre, descripción, versión)
- Acciones disponibles (id, parámetros, tipos de datos)
- Método de autenticación
- URL del agente

### 2. **Solicitud A2A**
Mensaje estándar JSON-RPC que contiene:
```json
{
  "id": "uuid-único",
  "action": "nombre-de-acción",
  "input": {
    "parámetro1": "valor1"
  },
  "authorization": "Bearer token-jwt",
  "timestamp": "ISO-8601"
}
```

### 3. **Respuesta A2A**
Respuesta estructurada:
```json
{
  "id": "uuid-mismo-que-request",
  "action": "nombre-de-acción",
  "status": "success|error",
  "output": {
    "resultado": "datos"
  },
  "timestamp": "ISO-8601"
}
```

### 4. **Autenticación**
- **OAuth 2.0** con bearer tokens
- **JWT (JSON Web Tokens)** para tokens cortos
- Scopes para control granular de permisos

### 5. **Descubrimiento**
Los agentes se descubren accediendo a `/.well-known/agent.json`

---

## Orden de Ejecución y Dependencias

### Árbol de Dependencias

```
01-agent-card.py (Independiente)
    ↓
    └─→ Enseña conceptos básicos

02-a2a-server.py (Independiente)
    ↓
    └─→ Levanta servidor en puerto 5000

03-a2a-client.py (Depende de 02-a2a-server.py)
    ├─→ Requiere que 02 esté ejecutándose
    └─→ Se comunica con servidor en localhost:5000

04-a2a-complete-example.py (Independiente)
    ↓
    └─→ Demostración completa (no requiere servidor)
```

### Orden Recomendado de Aprendizaje

| Paso | Archivo | Duración | Propósito | Dependencias |
|------|---------|----------|-----------|--------------|
| **1** | `01-agent-card.py` | 2 min | Entender estructura de AgentCard | Ninguna |
| **2** | `04-a2a-complete-example.py` | 3 min | Ver ejemplo completo con Strands | Ninguna |
| **3** | `02-a2a-server.py` | ∞ (servidor) | Implementar servidor A2A | Flask |
| **4** | `03-a2a-client.py` | 2 min | Cliente que descubre y llama servidor | Requests + 02 ejecutándose |

### Flujos de Ejecución

#### 🎓 **Flujo 1: Aprendizaje Teórico (Sin dependencias)**
```bash
# Terminal única - sin dependencias externas
python 01-agent-card.py      # 2 min
python 04-a2a-complete-example.py  # 3 min
# Total: ~5 minutos
```

#### 🔄 **Flujo 2: Servidor + Cliente (Requiere 2 terminales)**
```
Terminal 1:                    Terminal 2:
pip install flask             pip install requests
python 02-a2a-server.py      (espera a que se inicie el servidor)
Servidor escuchando...        python 03-a2a-client.py
```

#### 🚀 **Flujo 3: Demostración Completa (Recomendado)**
```bash
# Ejecutar en orden para aprender progresivamente
python 01-agent-card.py              # Conceptos básicos
python 04-a2a-complete-example.py    # Implementación completa
# Luego, en 2 terminales:
python 02-a2a-server.py              # Terminal 1
python 03-a2a-client.py              # Terminal 2
```

### Matriz de Dependencias

| Archivo | Strands | Flask | Requests | PyJWT | Server ejecutando | Descripción |
|---------|---------|-------|----------|-------|------------------|------------|
| **01** | ✓ | ✗ | ✗ | ✗ | No | Educacional - Conceptos |
| **02** | ✓ | ✓ | ✗ | ✗ | Sí (se levanta) | Servidor que expone A2A |
| **03** | ✓ | ✗ | ✓ | ✗ | Sí (02 debe estar activo) | Cliente que descubre y llama |
| **04** | ✓ | ✗ | ✗ | ✓ | No | Demo completa de orquestación |

### Instalación de Dependencias

```bash
# Dependencias base (todos los ejemplos)
pip install strands strands-tools

# Ejemplo 02 (Servidor A2A)
pip install flask

# Ejemplo 03 (Cliente A2A)
pip install requests

# Ejemplo 04 (Autenticación JWT)
pip install pyjwt

# Instalar todo
pip install strands strands-tools flask requests pyjwt
```

### Validar Instalación

```bash
# Verificar que todo está instalado
python -c "import strands; print('✓ Strands')"
python -c "import flask; print('✓ Flask')"
python -c "import requests; print('✓ Requests')"
python -c "import jwt; print('✓ PyJWT')"
```

---

## Ejemplos

### 1. **01-agent-card.py** - Crear AgentCards

Demuestra cómo crear AgentCards para diferentes tipos de agentes.

```bash
python 01-agent-card.py
```

**Salida:**
- AgentCard de Weather Agent
- AgentCard de Search Agent
- Explicación de componentes

**Conceptos:**
- Estructura de AgentCard
- Definición de acciones y parámetros
- Configuración de autenticación

---

### 2. **02-a2a-server.py** - Servidor A2A

Implementa un servidor que expone un agente usando el protocolo A2A.

```bash
pip install flask  # Instalación requerida
python 02-a2a-server.py
```

**Endpoints:**
```
GET  /.well-known/agent.json       → Descubrimiento (AgentCard)
GET  /v1/status                    → Estado del agente
POST /v1/actions/get_weather       → Ejecutar acción
```

**Ejemplo de uso:**
```bash
# Descubrir agente
curl http://localhost:5000/.well-known/agent.json

# Llamar una acción
curl -X POST http://localhost:5000/v1/actions/get_weather \
  -H "Content-Type: application/json" \
  -d '{
    "action": "get_weather",
    "input": {"city": "Paris"}
  }'
```

**Conceptos:**
- Estructura de servidor A2A
- Endpoints estándar
- Integración con Strands

---

### 3. **03-a2a-client.py** - Cliente A2A

Cliente que descubre y se comunica con múltiples agentes A2A.

```bash
pip install requests  # Instalación requerida
python 03-a2a-client.py
```

**Funcionalidades:**
- Descubrimiento automático de agentes
- Llamada de acciones remotas
- Coordinación entre agentes
- Logging de solicitudes

**Conceptos:**
- Cliente A2A
- Descubrimiento de capacidades
- Orquestación multi-agente

---

### 4. **04-a2a-complete-example.py** - Ejemplo Completo

Demostración completa con autenticación JWT y orquestación de viajes.

```bash
pip install pyjwt  # Instalación requerida
python 04-a2a-complete-example.py
```

**Componentes:**
1. **Autenticador A2A**: Gestión de tokens JWT
2. **Modelos A2A**: Clases estándar de Request/Response
3. **Agentes Especializados**: Weather y Activities Agents
4. **Orquestador**: Travel Planner que coordina múltiples agentes

**Ejemplo de flujo:**
```
Travel Planner
  ↓
  ├─→ Weather Agent (get_weather)
  │   └─→ "Clima cálido y soleado"
  │
  └─→ Activities Agent (get_activities)
      └─→ "Museos, gastronomía, paseos"
```

**Conceptos:**
- Autenticación JWT
- Modelos A2A estándar
- Múltiples agentes especializados
- Orquestación completa

---

## Arquitectura de los Ejemplos

```
01-agent-card.py
├── AgentCard definition
├── Weather Agent Card
└── Search Agent Card

02-a2a-server.py
├── Flask app
├── Strands Agent
├── AgentCard endpoint (/.well-known/agent.json)
└── Action endpoints (/v1/actions/*)

03-a2a-client.py
├── A2A Client
├── Agent Discovery
├── Action Invocation
└── Orchestration

04-a2a-complete-example.py
├── A2A Authenticator (JWT)
├── A2A Request/Response models
├── Multiple A2A Agents
└── Travel Planner Orchestrator
```

---

## Flujo Típico A2A

```
1. DESCUBRIMIENTO
   ┌─────────────────────────────────────┐
   │ Client                              │
   │  │                                  │
   │  └─→ GET /.well-known/agent.json    │
   │       Agent Card response           │
   └─────────────────────────────────────┘

2. AUTENTICACIÓN
   ┌─────────────────────────────────────┐
   │ Client obtiene Bearer Token         │
   │ (OAuth2/JWT)                        │
   └─────────────────────────────────────┘

3. INVOCACIÓN DE ACCIÓN
   ┌─────────────────────────────────────┐
   │ Client                              │
   │  │                                  │
   │  └─→ POST /v1/actions/{action}      │
   │       ├─ id: uuid                   │
   │       ├─ action: "get_weather"      │
   │       ├─ input: {city: "Paris"}     │
   │       └─ authorization: Bearer token│
   │                                     │
   │       Response:                     │
   │       ├─ status: "success"          │
   │       ├─ output: {...}              │
   │       └─ timestamp: ISO-8601        │
   └─────────────────────────────────────┘
```

---

## Instalación

```bash
# Dependencias básicas
pip install strands strands-tools

# Para servidor (02-a2a-server.py)
pip install flask

# Para cliente (03-a2a-client.py)
pip install requests

# Para autenticación JWT (04-a2a-complete-example.py)
pip install pyjwt
```

---

## Ejecución de Ejemplos

### ✨ Opción 1: Ejemplos Independientes (Recomendado para empezar)

**Sin dependencias externas ni servidores en segundo plano**

```bash
# Terminal única
python 01-agent-card.py
```

**Salida esperada:**
```
==================================================================
GOOGLE A2A PROTOCOL - AGENT CARDS
==================================================================

📋 WEATHER AGENT CARD
----------------------------------------------------------------------
{
  "name": "Weather Agent",
  ...
}

📋 SEARCH & ACTIVITIES AGENT CARD
----------------------------------------------------------------------
{
  "name": "Search & Activities Agent",
  ...
}
```

**Tiempo de ejecución:** ~2 minutos

---

```bash
# Terminal única
python 04-a2a-complete-example.py
```

**Salida esperada:**
```
==================================================================
AGENTES A2A DISPONIBLES
==================================================================

📋 Weather Agent:
{...}

📋 Activities Agent:
{...}

======================================================================
✈️  PLANIFICADOR DE VIAJES A2A
======================================================================

Destino: París

📡 Paso 1: Consultando clima...
✓ Clima obtenido
  [respuesta del agente]

📡 Paso 2: Consultando actividades...
✓ Actividades obtenidas
  [recomendaciones]

...
```

**Tiempo de ejecución:** ~3 minutos

---

### 🔄 Opción 2: Servidor A2A + Cliente (Configuración más realista)

**Requiere 2 terminales ejecutándose simultáneamente**

#### Terminal 1 - Iniciar Servidor A2A

```bash
pip install flask
python 02-a2a-server.py
```

**Salida esperada:**
```
==================================================================
A2A SERVER - GOOGLE A2A PROTOCOL
==================================================================

Endpoints disponibles:
  GET  /.well-known/agent.json     - Descubrimiento del agente (AgentCard)
  GET  /v1/status                  - Estado del agente
  POST /v1/actions/get_weather     - Acción: obtener clima

Iniciando servidor en http://localhost:5000...
 * Serving Flask app 'app'
 * Running on http://127.0.0.1:5000
```

**Estado:** El servidor está escuchando en puerto 5000 (mantener abierta)

#### Terminal 2 - Ejecutar Cliente A2A

```bash
pip install requests
python 03-a2a-client.py
```

**Salida esperada:**
```
==================================================================
A2A CLIENT - CLIENTE DEL PROTOCOLO A2A DE GOOGLE
==================================================================

📡 DESCUBRIMIENTO DE AGENTES
----------------------------------------------------------------------
Intentando descubrir agentes A2A...

✓ Descubierto: Weather Agent
  URL: http://localhost:5000
  Acciones: 1
    - Get Weather: Obtiene información del clima para una ciudad

==================================================================
AGENTES DESCUBIERTOS
==================================================================

🤖 Weather Agent
   URL: http://localhost:5000
   ...
```

**Tiempo de ejecución:** ~2 minutos (cliente) + ∞ (servidor)

---

### 📊 Matriz de Ejecución

| Escenario | Comando | Duración | Terminales | Complejidad |
|-----------|---------|----------|-----------|------------|
| **Aprender AgentCard** | `python 01-agent-card.py` | 2 min | 1 | ⭐ |
| **Demo Completa** | `python 04-a2a-complete-example.py` | 3 min | 1 | ⭐ |
| **Servidor A2A** | `python 02-a2a-server.py` | ∞ | 1 | ⭐⭐ |
| **Cliente Descubre** | `python 03-a2a-client.py` | 2 min | 1 (+ servidor) | ⭐⭐ |
| **Full Stack** | Ambos (02+03) | 2 min + ∞ | 2 | ⭐⭐⭐ |

---

### Troubleshooting de Ejecución

#### Problema: "No such file or directory"
```bash
# Verifica que estás en el directorio correcto
pwd  # debe mostrar .../module2/a2a/
ls   # debe mostrar los archivos .py
```

#### Problema: "ModuleNotFoundError: No module named 'strands'"
```bash
# Instala las dependencias
pip install strands strands-tools
```

#### Problema: "Connection refused" (al ejecutar cliente)
```bash
# Verifica que el servidor (02-a2a-server.py) está ejecutándose
# En Terminal 1, debería ver: "Running on http://127.0.0.1:5000"
```

#### Problema: "Port 5000 already in use"
```bash
# Otro proceso está usando el puerto
# Opción 1: Encuentra y cierra el proceso
lsof -i :5000
kill -9 <PID>

# Opción 2: Usa otro puerto (requiere editar 02-a2a-server.py y 03-a2a-client.py)
```

#### Problema: "JWT token expired"
```bash
# Los tokens JWT tienen validez de 1 hora
# Ejecuta nuevamente para obtener token fresco
python 04-a2a-complete-example.py
```

---

## Casos de Uso del Protocolo A2A

| Caso de Uso | Descripción |
|------------|-------------|
| **Descubrimiento** | Encontrar qué agentes están disponibles en una red |
| **Delegación** | Un agente delega tareas a otros especializados |
| **Coordinación** | Múltiples agentes trabajan juntos en un proyecto |
| **Orquestación** | Un orquestador coordina flujos complejos |
| **Interoperabilidad** | Agentes de diferentes plataformas colaboran |

---

## Ventajas del Protocolo A2A

✅ **Estandarización**: Formato JSON-RPC consistente
✅ **Descubrimiento**: Agentes se anuncian automáticamente
✅ **Seguridad**: Autenticación mediante OAuth2/JWT
✅ **Escalabilidad**: Soporta múltiples agentes
✅ **Interoperabilidad**: Funciona con diferentes frameworks

---

## Comparación: A2A vs MCP

| Aspecto | A2A | MCP |
|--------|-----|-----|
| **Propósito** | Agent-to-Agent | Model Context Protocol |
| **Scope** | Comunicación entre agentes | Herramientas para LLMs |
| **Complejidad** | Más complejo | Más simple |
| **Uso** | Orquestación multi-agente | Integración de herramientas |
| **Red** | Sí (HTTP APIs) | Local (tools) |

---

## Próximos Pasos

1. **Expandir ejemplos**: Agrega más tipos de agentes
2. **Implementar SSE**: Para comunicación asincrónica en tiempo real
3. **Base de datos**: Almacena historial de agentes
4. **Rate limiting**: Protege contra abuso
5. **Logging avanzado**: Monitoreo y debugging
6. **Tests**: Pruebas unitarias e integración

---

## Referencias

- [Google A2A Protocol - Medium](https://medium.com/@shamim_ru/google-agent-to-agent-a2a-protocol-explained-with-real-working-examples-99e362b61ba8)
- [A2A Protocol - Atlan](https://atlan.com/know/google-a2a-protocol/)
- [A2A Project - GitHub](https://github.com/a2aproject/A2A)
- [Strands Documentation](https://github.com/strands-ai/strands)

---

## Notas

- Los ejemplos usan localhost. En producción, usar HTTPS y dominios reales.
- La autenticación es simplificada. En producción, usar OAuth2 completo.
- Los agentes usan Strands pero cualquier framework LLM funciona con A2A.
