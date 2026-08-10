from strands import Agent
from strands.models.llamacpp import LlamaCppModel
from strands_tools import calculator

model = LlamaCppModel(
    base_url="http://192.168.2.29:8080",
    # **model_config
    model_id="default",
    params={
        "max_tokens": 1000,
        "temperature": 0.7,
        "repeat_penalty": 1.1,
    }
)

agent = Agent(model=model, tools=[calculator])
response = agent("What is 2+2")
print(response)
