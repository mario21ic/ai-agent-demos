"""Pattern 19: Long Context Understanding Pattern"""
from strands import Agent

class LongContextPattern:
    def __init__(self):
        self.agent = Agent(system_prompt="Eres especialista en contextos extensos")

    def summarize_long_context(self, long_text: str) -> str:
        print(f"\n{'='*70}\nLONG CONTEXT UNDERSTANDING\n{'='*70}\n")

        print(f"📄 Contexto largo ({len(long_text)} caracteres)")
        print(f"Primeros 100 chars: {long_text[:100]}...\n")

        prompt = f"""
        Contexto muy largo:
        {long_text[:300]}... [continúa]

        Resume los puntos clave en máximo 3 frases.
        """

        summary = str(self.agent(prompt))
        print(f"✓ Resumen:")
        print(f"  {summary[:150]}...\n")

        return summary

def main():
    pattern = LongContextPattern()
    long_text = """
    La Inteligencia Artificial es revolucionaria. Machine Learning permite
    que sistemas aprendan de datos. Deep Learning utiliza redes neuronales.
    NLP procesa lenguaje natural. Computer Vision analiza imágenes.
    Estos campos transforman la tecnología moderna.
    """ * 20

    pattern.summarize_long_context(long_text)

if __name__ == "__main__":
    main()
