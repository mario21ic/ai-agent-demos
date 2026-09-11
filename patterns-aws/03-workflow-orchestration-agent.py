"""
AWS Pattern: Workflow Orchestration Agent
==========================================
Agente que orquesta flujos de trabajo complejos coordinando
múltiples pasos, agentes y decisiones.

Principios AWS:
- Asincrónico: Coordina tareas asincrónicas
- Autonomía: Toma decisiones sobre el flujo
- Agencia: Actúa para mantener el flujo en movimiento
"""

from strands import Agent
from typing import Dict, List, Any
from enum import Enum
from dataclasses import dataclass


class StepStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class WorkflowStep:
    """Un paso en el flujo de trabajo"""
    id: str
    name: str
    description: str
    status: StepStatus = StepStatus.PENDING
    result: Any = None
    error: str = None
    dependencies: List[str] = None

    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []


class WorkflowOrchestrationAgent:
    """Agente que orquesta flujos de trabajo"""

    def __init__(self):
        # Orquestrador principal
        self.orchestrator = Agent(
            system_prompt="""Eres un orquestador de flujos de trabajo.
            Tu responsabilidad es:
            1. Coordinar múltiples pasos en orden
            2. Gestionar dependencias
            3. Manejar errores y recuperación
            4. Tomar decisiones sobre bifurcaciones
            5. Reportar progreso

            Sé eficiente y robusto."""
        )

        # Agentes especializados para diferentes tipos de tareas
        self.data_processor = Agent(
            system_prompt="Eres especialista en procesamiento de datos"
        )

        self.quality_checker = Agent(
            system_prompt="Eres especialista en control de calidad"
        )

        self.notification_handler = Agent(
            system_prompt="Eres especialista en notificaciones"
        )

        self.workflow_log: List[WorkflowStep] = []
        self.execution_log: List[Dict] = []

    def create_workflow(self, workflow_name: str) -> List[WorkflowStep]:
        """Define un flujo de trabajo"""

        steps = []

        if workflow_name == "data_pipeline":
            steps = [
                WorkflowStep("step1", "Data Ingestion", "Ingerir datos de fuentes"),
                WorkflowStep("step2", "Data Validation", "Validar datos",
                            dependencies=["step1"]),
                WorkflowStep("step3", "Data Processing", "Procesar datos",
                            dependencies=["step2"]),
                WorkflowStep("step4", "Quality Check", "Verificar calidad",
                            dependencies=["step3"]),
                WorkflowStep("step5", "Notification", "Notificar resultados",
                            dependencies=["step4"]),
            ]

        elif workflow_name == "approval_workflow":
            steps = [
                WorkflowStep("step1", "Submit Request", "Enviar solicitud"),
                WorkflowStep("step2", "Initial Review", "Revisión inicial",
                            dependencies=["step1"]),
                WorkflowStep("step3", "Manager Approval", "Aprobación de gerente",
                            dependencies=["step2"]),
                WorkflowStep("step4", "Finance Check", "Revisión financiera",
                            dependencies=["step3"]),
                WorkflowStep("step5", "Final Execution", "Ejecución final",
                            dependencies=["step4"]),
            ]

        return steps

    def execute_step(self, step: WorkflowStep) -> bool:
        """Ejecuta un paso individual"""

        print(f"  📋 {step.name}: ", end="", flush=True)
        step.status = StepStatus.IN_PROGRESS

        try:
            # Simular ejecución usando agentes especializados
            if "Data" in step.name or "Process" in step.name:
                result = self.data_processor(f"Ejecuta: {step.description}")
            elif "Quality" in step.name or "Check" in step.name:
                result = self.quality_checker(f"Ejecuta: {step.description}")
            elif "Notif" in step.name:
                result = self.notification_handler(f"Ejecuta: {step.description}")
            else:
                result = self.orchestrator(f"Ejecuta: {step.description}")

            step.result = result
            step.status = StepStatus.COMPLETED
            print("✓")
            return True

        except Exception as e:
            step.error = str(e)
            step.status = StepStatus.FAILED
            print(f"✗ ({str(e)[:30]})")
            return False

    def check_dependencies(self, step: WorkflowStep, completed_steps: Dict[str, WorkflowStep]) -> bool:
        """Verifica si todas las dependencias de un paso están completadas"""
        for dep in step.dependencies:
            if dep not in completed_steps or completed_steps[dep].status != StepStatus.COMPLETED:
                return False
        return True

    def execute_workflow(self, workflow_name: str) -> Dict:
        """Ejecuta un flujo de trabajo completo"""

        print(f"\n{'='*70}")
        print(f"WORKFLOW ORCHESTRATION: {workflow_name.upper()}")
        print(f"{'='*70}\n")

        # Crear flujo
        steps = self.create_workflow(workflow_name)
        self.workflow_log = steps

        print("Workflow Steps:")
        for step in steps:
            print(f"  {step.id}: {step.name} (depends on: {step.dependencies if step.dependencies else 'none'})")

        print("\nExecution:")
        print("-" * 70)

        completed_steps = {}
        failed_steps = []

        # Ejecutar pasos en orden, respetando dependencias
        for step in steps:
            # Verificar dependencias
            if not self.check_dependencies(step, completed_steps):
                step.status = StepStatus.SKIPPED
                print(f"  📋 {step.name}: ⊘ (dependencies not met)")
                continue

            # Ejecutar paso
            success = self.execute_step(step)

            if success:
                completed_steps[step.id] = step
            else:
                failed_steps.append(step)

                # Decidir si continuar o detener
                decision_prompt = f"""
                El paso '{step.name}' falló con error: {step.error}

                ¿Debería:
                1. Detener el flujo completamente
                2. Continuar con los pasos siguientes que no dependen de este
                3. Reintentar el paso

                Considera el impacto en los pasos siguientes.
                """

                decision = self.orchestrator(decision_prompt)
                print(f"\n  Decision: {decision[:80]}...\n")

                if "Detener" in decision or "stop" in decision.lower():
                    break

        # Resumen
        print("\n" + "-" * 70)
        print(f"Pasos completados: {len(completed_steps)}")
        print(f"Pasos fallidos: {len(failed_steps)}")
        print(f"Pasos pendientes: {len([s for s in steps if s.status == StepStatus.PENDING])}")

        # Registro
        execution_result = {
            "workflow": workflow_name,
            "total_steps": len(steps),
            "completed": len(completed_steps),
            "failed": len(failed_steps),
            "steps": steps
        }

        self.execution_log.append(execution_result)
        return execution_result

    def print_workflow_summary(self):
        """Imprime resumen del flujo de trabajo"""

        print(f"\n{'='*70}")
        print("WORKFLOW ORCHESTRATION SUMMARY")
        print(f"{'='*70}\n")

        print(f"Total workflows executed: {len(self.execution_log)}")

        for i, execution in enumerate(self.execution_log, 1):
            success_rate = (execution["completed"] / execution["total_steps"]) * 100
            print(f"\n{i}. {execution['workflow']}")
            print(f"   Success Rate: {success_rate:.0f}%")
            print(f"   Completed: {execution['completed']}/{execution['total_steps']}")
            print(f"   Failed: {execution['failed']}")

        print("\n" + "="*70)
        print("WORKFLOW ORCHESTRATION CHARACTERISTICS")
        print("="*70)
        print("""
Ventajas:
  ✓ Coordina flujos complejos
  ✓ Maneja dependencias automáticamente
  ✓ Recuperación ante errores
  ✓ Escalable a cientos de pasos
  ✓ Observable y auditable

Desventajas:
  ✗ Complejo de implementar correctamente
  ✗ Debugging difícil
  ✗ Estados distribuidos
  ✗ Manejo de timeout crítico

AWS Pattern: WORKFLOW ORCHESTRATION
  → Coordina múltiples servicios
  → Maneja transiciones de estado
  → Soporta ramificación condicional
  → Integrable con Step Functions

Casos de Uso:
  • Pipelines de datos ETL
  • Procesos de aprobación
  • Automatización de empleados
  • Orquestación de microservicios
        """)


def main():
    """Ejecuta ejemplo de Workflow Orchestration Agent"""

    agent = WorkflowOrchestrationAgent()

    # Ejecutar flujo 1: Pipeline de datos
    result1 = agent.execute_workflow("data_pipeline")

    # Ejecutar flujo 2: Flujo de aprobación
    result2 = agent.execute_workflow("approval_workflow")

    # Resumen
    agent.print_workflow_summary()


if __name__ == "__main__":
    main()
