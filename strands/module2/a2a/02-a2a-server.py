"""
Google A2A Protocol - Simple A2A Server
========================================
Ejemplo 2: Servidor A2A que implementa el protocolo y expone un AgentCard
"""

from flask import Flask, jsonify, request
from strands import Agent
import json
from datetime import datetime
from typing import Dict, Any


app = Flask(__name__)


# Configurar el agente Strands
weather_agent = Agent(
    system_prompt="""Eres un agente meteorológico. Proporcionas información del clima
    de forma estructurada en JSON. Responde siempre en formato JSON válido."""
)


# AgentCard del protocolo A2A
AGENT_CARD = {
    "name": "Weather Agent",
    "description": "Agente A2A que proporciona información meteorológica",
    "version": "1.0.0",
    "contact": "weather@agent.local",
    "url": "http://localhost:5000",
    "actions": [
        {
            "id": "get_weather",
            "name": "Get Weather",
            "description": "Obtiene información del clima para una ciudad",
            "parameters": [
                {
                    "name": "city",
                    "type": "string",
                    "description": "Nombre de la ciudad",
                    "required": True
                },
                {
                    "name": "units",
                    "type": "string",
                    "description": "Unidades: celsius o fahrenheit",
                    "required": False
                }
            ]
        }
    ],
    "authentication": {
        "type": "bearer_token",
        "provider": "local",
        "required": False
    }
}


@app.route('/.well-known/agent.json', methods=['GET'])
def agent_card():
    """
    Endpoint del protocolo A2A que expone el AgentCard.
    Otros agentes pueden descubrir nuestras capacidades aquí.
    """
    return jsonify(AGENT_CARD)


@app.route('/v1/actions/get_weather', methods=['POST'])
def get_weather():
    """
    Endpoint A2A que implementa la acción 'get_weather'.
    Recibe una tarea en formato A2A y retorna el resultado.

    Formato de entrada (A2A):
    {
        "id": "task-uuid",
        "action": "get_weather",
        "input": {
            "city": "Paris",
            "units": "celsius"
        }
    }
    """
    try:
        data = request.get_json()

        # Extraer parámetros
        action = data.get('action')
        task_input = data.get('input', {})
        task_id = data.get('id', 'unknown')

        city = task_input.get('city')
        units = task_input.get('units', 'celsius')

        if not city:
            return jsonify({
                "id": task_id,
                "status": "error",
                "error": "Parámetro 'city' requerido"
            }), 400

        # Usar el agente Strands para obtener el clima
        prompt = f"Proporciona información del clima para {city} en {units}. Responde en JSON."
        response = weather_agent(prompt)

        # Respuesta en formato A2A
        return jsonify({
            "id": task_id,
            "action": action,
            "status": "success",
            "output": {
                "city": city,
                "units": units,
                "weather": response,
                "timestamp": datetime.now().isoformat()
            }
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500


@app.route('/v1/status', methods=['GET'])
def status():
    """
    Endpoint de estado del agente
    """
    return jsonify({
        "status": "operational",
        "agent": "Weather Agent",
        "timestamp": datetime.now().isoformat()
    })


def main():
    """Inicia el servidor A2A"""

    print("\n" + "="*70)
    print("A2A SERVER - GOOGLE A2A PROTOCOL")
    print("="*70)
    print(f"""
Este servidor implementa el protocolo A2A de Google.

Endpoints disponibles:
  GET  /.well-known/agent.json     - Descubrimiento del agente (AgentCard)
  GET  /v1/status                  - Estado del agente
  POST /v1/actions/get_weather     - Acción: obtener clima

Prueba con:
  curl http://localhost:5000/.well-known/agent.json

  curl -X POST http://localhost:5000/v1/actions/get_weather \\
    -H "Content-Type: application/json" \\
    -d '{{"action": "get_weather", "input": {{"city": "Paris"}}}}'

Iniciando servidor en http://localhost:5000...
    """)

    app.run(debug=True, port=5000)


if __name__ == "__main__":
    main()
