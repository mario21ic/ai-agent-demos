# A2A avanzado con AWS Strands + servidor MCP

Ejemplo de nivel intermedio-avanzado que combina dos protocolos abiertos y
complementarios:

- **A2A (Agent2Agent, Google)**: comunicación agente ↔ agente. Cada agente se
  expone como un servidor HTTP con un *AgentCard* (nombre, descripción,
  *skills*) que otros agentes pueden descubrir y con el que pueden conversar
  en lenguaje natural.
- **MCP (Model Context Protocol, Anthropic)**: comunicación agente ↔
  herramienta. Un servidor MCP expone funciones (tools) que cualquier
  cliente MCP puede descubrir y ejecutar.

Un mismo agente puede ser **cliente MCP** (para obtener herramientas) y, al
mismo tiempo, **servidor A2A** (para que otros agentes lo descubran y le
deleguen tareas). Ese es el punto central de este ejemplo.

## Arquitectura

```
                     A2A                          A2A
Usuario -> Orquestador  <---------->  Investigador  <---------->  (MCP) Servidor MCP
           (cliente A2A)              (servidor A2A               "Datos Financieros"
                |                      + cliente MCP)              (precios, noticias)
                |  A2A
                v
             Redactor
           (servidor A2A)
```

1. **`mcp_server.py`** — Servidor MCP que expone `consultar_precio_accion` y
   `consultar_noticias_empresa` (datos simulados) vía streamable-HTTP en
   `http://127.0.0.1:8000/mcp`.
2. **`agente_investigador.py`** — Servidor A2A en el puerto `9001`. Al
   arrancar, se conecta como *cliente MCP* al servidor MCP y usa sus
   herramientas para responder preguntas financieras.
3. **`agente_redactor.py`** — Servidor A2A en el puerto `9002`. No tiene
   herramientas propias; solo sabe redactar resúmenes ejecutivos a partir de
   los datos que le pasen.
4. **`agente_orquestador.py`** — Cliente A2A. Descubre a los dos agentes
   anteriores con `A2AClientToolProvider` (que los expone como herramientas)
   y coordina el flujo: primero pide datos al Investigador, luego pide al
   Redactor que arme el informe con esos datos.

## Requisitos

```bash
pip install -r requirements.txt
```

Strands usa Amazon Bedrock con un modelo Claude por defecto, así que se
necesitan credenciales de AWS configuradas (`aws configure` o variables de
entorno) con acceso a Bedrock.

## Ejecución

Cada componente corre en su propia terminal, en este orden:

```bash
# Terminal 1
python mcp_server.py

# Terminal 2 (espera a que el servidor MCP esté arriba)
python agente_investigador.py

# Terminal 3
python agente_redactor.py

# Terminal 4 (ejecuta el flujo de ejemplo y termina)
python agente_orquestador.py
```

El Orquestador le pide un informe ejecutivo sobre la acción de Amazon
(`AMZN`). En los logs de la Terminal 2 se puede ver cómo el Agente
Investigador llama a las herramientas MCP (`consultar_precio_accion`,
`consultar_noticias_empresa`) antes de responderle al Orquestador por A2A.

## Puntos clave del ejemplo

- **AgentCard con `skills`**: a diferencia del ejemplo básico, aquí se
  declaran `AgentSkill` explícitos para cada agente A2A, lo que permite a un
  cliente decidir a quién delegar según la tarea, no solo según el nombre.
- **Agente híbrido (A2A + MCP)**: `agente_investigador.py` demuestra que un
  mismo proceso puede ser servidor A2A "hacia afuera" y cliente MCP "hacia
  adentro" — un patrón común en arquitecturas multiagente reales, donde cada
  agente encapsula sus propias fuentes de datos/herramientas detrás de una
  interfaz A2A uniforme.
- **Orquestación multi-salto**: el Orquestador no sabe nada de MCP ni de
  cómo el Investigador obtiene sus datos; solo conoce el protocolo A2A. Esto
  permite intercambiar o escalar la implementación interna de cualquier
  agente sin tocar a los demás.
