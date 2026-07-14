from pydantic import BaseModel, Field
from strands import Agent

class Address(BaseModel):
    street: str
    city: str
    country: str

class Person(BaseModel):
    name: str = Field(description="Full name of the person") # decimos al modelo que debe considerar
    age: int
    occupation: str
    address: Address
    skills: list[str]


agent = Agent()
result = agent(
    "John Smith is a 30-year-old Software Engineer, expert DevOps and Cloud Architect. Living on Av Canevaro 255 apartment 1106 - Lima, Peru",
    structured_output_model=Person
)

print(result.structured_output.name) # John Smith
print(result.structured_output.age) # 30 (int, no string)
print(result.structured_output.occupation)
print(result.structured_output.address)
print(result.structured_output.skills)
