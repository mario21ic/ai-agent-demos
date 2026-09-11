"""Pattern 13: Streaming & Partial Responses Pattern"""
from strands import Agent

class StreamingPattern:
    def __init__(self):
        self.agent = Agent(system_prompt="Eres especialista en streaming")

    def stream_response(self, query: str):
        print(f"\n{'='*70}\nSTREAMING & PARTIAL RESPONSES\n{'='*70}\n")
        print(f"Query: {query}\n")
        response = str(self.agent(query))
        chunks = response.split('. ')[:4]
        for i, chunk in enumerate(chunks, 1):
            print(f"📦 Chunk {i}: {chunk.strip()}...")
        print()

def main():
    pattern = StreamingPattern()
    pattern.stream_response("¿Cuáles son los beneficios de la IA?")

if __name__ == "__main__":
    main()
