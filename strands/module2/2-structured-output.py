"""
Usar cuando:
- Agente se integra en una app (no hay humano del otro lado)
- Necesitas datos para procesar despues
- Integracion con APIs, frontends o bases de datos
- Validacion automatica de tipos
NO:
- La respuesta es conversacional
- EL usuario espera texto libre
"""

from pydantic import BaseModel
from strands import Agent

class PersonInfo(BaseModel):
    name: str
    age: int
    occupation: str


agent = Agent()
result = agent(
    "John Smith is a 30-year-old software engineer",
    structured_output_model=PersonInfo
)

print(result.structured_output.name) # John Smith
print(result.structured_output.age) # 30 (int, no string)
