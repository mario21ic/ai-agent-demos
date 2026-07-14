#!/usr/bin/env python
import requests
import subprocess, shlex

from fastmcp.dependencies import CurrentContext


"""
Ejemplo del Tema 1: Las 4 primitivas de MCP
============================================

Este fichero acompaña el Tema 1 del curso y muestra las cuatro
primitivas que define el protocolo MCP:

    1. Tool     → el modelo ejecuta una acción en el mundo real
    2. Resource → el modelo lee datos de solo lectura
    3. Prompt   → plantilla de instrucciones reutilizable
    4. Sampling → el servidor le pide al modelo que genere texto

Usamos FastMCP, la API de alto nivel del SDK oficial de Python.
FastMCP oculta el protocolo JSON-RPC y deja que te concentres
en la lógica de tu servidor.

Instalación:
    pip install fastmcp

Arranque:
    python primitivas.py

Prueba sin Claude Desktop (abre una interfaz web interactiva):
    npx @modelcontextprotocol/inspector python primitivas.py
"""

from fastmcp import Context, FastMCP

# FastMCP es el punto de entrada del servidor.
# El nombre que le pasamos aparece en el handshake inicial:
# es lo que el host (Claude Desktop, Cursor...) ve cuando conecta.
mcp = FastMCP("servidor-primitivas")


# =============================================================
# PRIMITIVA 1: TOOL
# =============================================================
#
# Una Tool es una función que el modelo puede invocar.
# El modelo la llama cuando decide que necesita ejecutar
# una acción — leer archivos, consultar APIs, escribir datos...
#
# El modelo NUNCA ve el código. Solo ve:
#   - el nombre de la función
#   - el docstring (su "contrato" para decidir cuándo usarla)
#   - los tipos de los parámetros
#
# Si el docstring es vago, el modelo no sabrá cuándo usarla.
# Si el docstring es claro, el modelo la usará en el momento justo.

@mcp.tool()
def read_file(path: str) -> str:
    """Lee el contenido de un archivo del sistema de ficheros local.

    Usa esta tool cuando el usuario pida ver, analizar o procesar
    el contenido de un archivo específico. No la uses para listar
    directorios ni para comprobar si un archivo existe.
    """
    # El modelo nos pasará el path que él considere correcto
    # basándose en la conversación. En un servidor de producción
    # habría que validar esta ruta (ver Tema 5).
    with open(path, "r", encoding="utf-8") as f:
        return f.read()
    

@mcp.tool()
def execute_command(cmd_params: str) -> str:
    """Ejecuta un comando en el sistema y devuelve su salida."""
    print(f"Ejecutando comando: {cmd_params.split(' ')}")
    result_ok = ""
    result_err = 0
    try:
        # Run the command and capture results
        result = subprocess.run(
            # ["python", "--version"],
            #cmd_params.split(' '),
            #shlex.split(cmd_params), # respeta comillas/espacios, mejor que split(' ')
            cmd_params, # string crudo, pero RCE
            shell=True, # permite | > * &&
            capture_output=True, 
            text=True, 
            check=True,
            timeout=15,
        )

        if result.returncode != 0:
            return f"[exit {result.returncode}] {result.stderr.strip() or result.stdout.strip()}"
        return result.stdout.strip() or "(sin salida)"
    
    except subprocess.TimeoutExpired:
        return "[error] el comando excedió el timeout de 15s"
    except Exception as e:
        return f"[error] {type(e).__name__}: {e}"
        
    #except subprocess.CalledProcessError as e:
    #    print("The command failed!")
    #    print("Error details:", e.stderr)
    #return result_ok

@mcp.tool()
def create_file(path: str, contenido: str) -> str:
    """Crear archivo en una ruta definida
    """
    with open(path, "w", encoding="utf-8") as f:
        #f.write("creado mediante MCP")
        f.write(contenido)
    return f"Archivo {path} creado"

@mcp.tool()
def get_weather(city: str) -> dict:
    """Devuelve el clima de una ciudad
    """
    url = "http://api.weatherapi.com/v1/current.json"
    params = {
        "key": os.environ['WEATHER_API_KEY'],
        "q": city,
        "aqi": "yes"
    }

    # Realizar el GET request
    response = requests.get(url, params=params)
    clima = {}

    # Verificar si la solicitud fue exitosa
    if response.status_code == 200:
        data = response.json()

        # Extraer los valores deseados
        clima = {
            "temperatura": data["current"]["temp_c"],
            "condicion": data["current"]["condition"]["text"],
            "dia": data["current"]["is_day"]
        }
    else:
        clima["msg"] = "Error en la solicitud " + response.status_code

    return clima


# =============================================================
# PRIMITIVA 2: RESOURCE
# =============================================================
#
# Un Resource expone datos de solo lectura.
# A diferencia de las Tools, no ejecuta acciones ni produce
# efectos secundarios: simplemente devuelve información.
#
# Se identifica por un URI único con cualquier esquema:
#   file://   → ficheros locales
#   db://     → tablas de base de datos
#   https://  → endpoints HTTP
#
# El modelo añade el contenido del resource a su contexto
# cuando necesita esa información para responder.

@mcp.resource("resource://greeting")
def get_greeting() -> str:
    """Devuelve el mensaje de bienvenida configurado en el sistema."""
    # En un servidor real este valor vendría de una base de datos
    # o de un fichero de configuración.
    return "¡Hola, mundo desde el MCP!"


@mcp.resource("data://users")
def get_users() -> list[str]:
    """Lista de usuarios activos registrados en el sistema."""
    # Aquí iría una consulta real a la base de datos.
    return ["Juan", "Maria", "Pedro", "Anya"]


# =============================================================
# PRIMITIVA 3: PROMPT
# =============================================================
#
# Un Prompt en MCP NO es un prompt de usuario.
# Es una plantilla de instrucciones que el SERVIDOR define
# para que el HOST la use cuando construye mensajes al modelo.
#
# Útil para workflows repetitivos donde siempre necesitas
# el mismo marco de instrucciones pero con datos distintos
# cada vez (code reviews, análisis de logs, generación de docs...).

@mcp.prompt()
def code_review_prompt(language: str, file_content: str) -> str:
    """Genera el prompt estándar de code review para el lenguaje indicado.

    El host llama a este prompt cuando el usuario pide una revisión
    de código, para no tener que escribir las instrucciones completas
    cada vez.
    """
    # f-string simple aquí, pero en producción podrías cargar
    # la plantilla desde un fichero .txt para editarla sin tocar código.
    return f"""
    Eres un experto en {language}. Revisa el siguiente código y señala:

    1. Bugs potenciales
    2. Problemas de performance
    3. Violaciones de estilo

    Para cada problema indica: línea afectada, severidad (alta/media/baja)
    y una sugerencia de corrección concisa.

    Código a revisar:
    {file_content}
    """


# =============================================================
# PRIMITIVA 4: SAMPLING
# =============================================================
#
# Sampling invierte la dirección habitual:
#   Dirección normal  → el modelo llama al servidor (Tool, Resource)
#   Sampling          → el servidor le pide al modelo que genere texto
#
# Permite que tu servidor use la capacidad del modelo como parte
# de su lógica interna, sin necesitar su propia API key:
# usa la del host que ya está conectado.
#
# IMPORTANTE: no todos los hosts lo soportan todavía.
# Requiere que el host lo habilite explícitamente.
#
# En FastMCP moderno no existe un decorador @mcp.sampling().
# Sampling se usa desde una tool, recibiendo Context y llamando
# a ctx.sample(...).

@mcp.tool()
async def generate_text(topic: str, ctx: Context) -> str:
    """Genera texto en markdown usando la capacidad de sampling del host."""
    result = await ctx.sample(
        messages=(
            f"Genera un texto de 100 palabras sobre '{topic}'. "
            "El texto debe estar en español y en formato markdown."
        ),
        temperature=0.7,
        max_tokens=220,
    )
    return result.text or ""

@mcp.tool()
async def extract_task_titles(notes: str, ctx: Context = CurrentContext()) -> list[str]:
    """Extract 3-7 actionable task title from notes.
    Return short imperative titles (verb first)
    """
    result = await ctx.sample(
        messages=(
            "From the text below, extract 3 to 7 actionable tasks,\n"
            "Return only a json array of strings (tasks titles). "
            "No markdown, no extra text.\n\n"
            f"TEXT:\n{notes}"
        ),
        system_prompt="You are a strict project manager. Tasks must be concrete and doable.",
        temperature=0.1,
        max_tokens=120,
        result_type=list[str]
    )
    return result.result

# =============================================================
# ARRANQUE DEL SERVIDOR
# =============================================================
#
# mcp.run() lanza el servidor en modo stdio:
#   - stdin  → recibe peticiones JSON-RPC del host
#   - stdout → emite respuestas JSON-RPC al host
#
# Claude Desktop lo lanza como proceso hijo usando la
# configuración de claude_desktop_config.json.
# MCP Inspector lo lanza igual, pero te abre una UI web
# para interactuar directamente sin pasar por el modelo.

if __name__ == "__main__":
    #mcp.run() # stdio
    mcp.run(
        #transport="http",
        transport="streamable-http",
        host="127.0.0.1",       # Use "0.0.0.0" to expose to your local network
        port=8000,              # Specify your desired network port
        stateless_http=True, # evitar modo stateful (el default de streamable-http), y la sesión SSE se cae → Session terminated
    )
