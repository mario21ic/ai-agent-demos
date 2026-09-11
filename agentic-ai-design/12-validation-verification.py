"""Pattern 12: Validation & Verification Pattern"""
from strands import Agent
from typing import Dict

class ValidationVerificationPattern:
    def __init__(self):
        self.agent = Agent(system_prompt="Eres generador de contenido")
        self.validator = Agent(system_prompt="Eres validador experto")

    def validate_output(self, task: str) -> Dict:
        print(f"\n{'='*70}\nVALIDATION & VERIFICATION\n{'='*70}\n")

        # Generar
        print("📝 Generating content...")
        output = str(self.agent(task))
        print(f"Generated: {output[:100]}...\n")

        # Validar
        print("✓ Validating output...")
        validation = str(self.validator(f"¿Es válido y correcto?: {output[:150]}"))
        is_valid = "sí" in validation.lower() or "válido" in validation.lower()
        print(f"Valid: {is_valid}")
        print(f"Validation: {validation[:100]}...\n")

        return {"output": output, "valid": is_valid, "validation": validation}

def main():
    pattern = ValidationVerificationPattern()
    result = pattern.validate_output("Genera una descripción de producto")
    print("="*70)
    print("VALIDATION & VERIFICATION CHARACTERISTICS")
    print("="*70)
    print("""
Ventajas:
  ✓ Garantiza calidad
  ✓ Detecta errores
  ✓ Mejora confiabilidad

Desventajas:
  ✗ Overhead computacional
  ✗ Falsos positivos/negativos
    """)

if __name__ == "__main__":
    main()
