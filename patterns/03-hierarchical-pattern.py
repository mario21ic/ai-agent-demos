"""
Hierarchical Agent Pattern
===========================
Un agente supervisor coordina y delega tareas a agentes subordinados.
Útil para estructuras organizacionales, toma de decisiones jerárquica, etc.

Use case: Organizaciones, supervisión de tareas, escalabilidad, etc.
"""

from strands import Agent
from typing import List, Dict
from enum import Enum


class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class Task:
    """Representación de una tarea"""

    def __init__(self, id: str, description: str, assigned_to: str = None):
        self.id = id
        self.description = description
        self.assigned_to = assigned_to
        self.status = TaskStatus.PENDING
        self.result = None

    def to_dict(self):
        return {
            "id": self.id,
            "description": self.description,
            "assigned_to": self.assigned_to,
            "status": self.status.value,
            "result": self.result
        }


class HierarchicalTeam:
    """Equipo con estructura jerárquica"""

    def __init__(self):
        # Supervisor (nivel superior)
        self.supervisor = Agent(
            system_prompt="""Eres un supervisor de proyecto. Tu trabajo es:
            1. Analizar requerimientos
            2. Dividir el trabajo en subtareas
            3. Asignar tareas a especialistas
            4. Revisar resultados
            5. Tomar decisiones finales"""
        )

        # Especialistas (nivel subordinado)
        self.frontend_specialist = Agent(
            system_prompt="""Eres un especialista frontend. Ejecutas tareas relacionadas
            con interfaz de usuario y experiencia del cliente."""
        )

        self.backend_specialist = Agent(
            system_prompt="""Eres un especialista backend. Ejecutas tareas relacionadas
            con lógica de servidor, APIs y bases de datos."""
        )

        self.devops_specialist = Agent(
            system_prompt="""Eres un especialista DevOps. Ejecutas tareas relacionadas
            con infraestructura, deployment y monitoreo."""
        )

        self.specialists = {
            "frontend": self.frontend_specialist,
            "backend": self.backend_specialist,
            "devops": self.devops_specialist
        }

        self.tasks: List[Task] = []
        self.hierarchy_log: List[str] = []

    def supervisor_plan(self, project_description: str) -> str:
        """El supervisor planifica el proyecto"""

        self.hierarchy_log.append("📋 Supervisor: Analizando proyecto...")

        plan = self.supervisor(
            f"""Analiza este proyecto y crea un plan detallado:
            {project_description}

            Para cada tarea, especifica:
            1. Descripción clara
            2. Especialista recomendado (frontend/backend/devops)
            3. Dependencias

            Formato: "[TAREA] descripción -> asignar a: especialista"
            """
        )

        self.hierarchy_log.append("✓ Supervisor: Plan creado")
        return plan

    def assign_task(self, task_id: str, description: str, specialist: str):
        """El supervisor asigna una tarea a un especialista"""

        task = Task(task_id, description, specialist)
        self.tasks.append(task)

        self.hierarchy_log.append(
            f"📤 Supervisor: Asignando tarea {task_id} a {specialist}"
        )

        return task

    def execute_task(self, task: Task) -> str:
        """Un especialista ejecuta una tarea asignada"""

        if task.assigned_to not in self.specialists:
            task.status = TaskStatus.FAILED
            task.result = "Especialista no encontrado"
            return "ERROR: Especialista no encontrado"

        specialist = self.specialists[task.assigned_to]
        task.status = TaskStatus.IN_PROGRESS

        self.hierarchy_log.append(
            f"🔧 {task.assigned_to.title()}: Ejecutando tarea {task.id}"
        )

        try:
            result = specialist(f"Ejecuta esta tarea: {task.description}")
            task.status = TaskStatus.COMPLETED
            task.result = result

            self.hierarchy_log.append(
                f"✓ {task.assigned_to.title()}: Tarea {task.id} completada"
            )

            return result

        except Exception as e:
            task.status = TaskStatus.FAILED
            task.result = str(e)

            self.hierarchy_log.append(
                f"✗ {task.assigned_to.title()}: Tarea {task.id} falló"
            )

            return f"Error: {str(e)}"

    def supervisor_review(self) -> str:
        """El supervisor revisa todos los resultados"""

        self.hierarchy_log.append("📋 Supervisor: Revisando resultados...")

        results_summary = "\n".join([
            f"- {t.assigned_to}: {t.status.value}"
            for t in self.tasks
        ])

        review = self.supervisor(
            f"""Revisa estos resultados de tareas:
            {results_summary}

            Proporciona:
            1. Evaluación general
            2. Puntos fuertes
            3. Áreas de mejora
            4. Decisión final: ¿Aceptar o rechazar?
            """
        )

        self.hierarchy_log.append("✓ Supervisor: Revisión completada")
        return review

    def run_project(self, project_description: str):
        """Ejecuta un proyecto completo con estructura jerárquica"""

        print(f"\n{'='*70}")
        print(f"HIERARCHICAL PROJECT EXECUTION")
        print(f"{'='*70}\n")

        # Fase 1: Planificación
        print("📋 FASE 1: PLANIFICACIÓN")
        print("-" * 70)
        plan = self.supervisor_plan(project_description)
        print(f"Plan del supervisor:\n{plan}\n")

        # Fase 2: Asignación de tareas
        print("📤 FASE 2: ASIGNACIÓN DE TAREAS")
        print("-" * 70)

        # Tareas específicas basadas en el proyecto
        tasks_to_assign = [
            ("task-001", "Diseñar interfaz de usuario", "frontend"),
            ("task-002", "Implementar API REST", "backend"),
            ("task-003", "Configurar infraestructura en cloud", "devops"),
            ("task-004", "Integrar autenticación", "backend"),
        ]

        for task_id, desc, specialist in tasks_to_assign:
            self.assign_task(task_id, desc, specialist)
            print(f"✓ Tarea {task_id} → {specialist}")

        print()

        # Fase 3: Ejecución de tareas
        print("🔧 FASE 3: EJECUCIÓN DE TAREAS")
        print("-" * 70)

        for task in self.tasks:
            result = self.execute_task(task)
            print(f"✓ {task.id}: {result[:80]}...")

        print()

        # Fase 4: Revisión
        print("📋 FASE 4: REVISIÓN DEL SUPERVISOR")
        print("-" * 70)
        review = self.supervisor_review()
        print(f"Revisión:\n{review}\n")

    def print_hierarchy_visualization(self):
        """Visualiza la estructura jerárquica"""

        print(f"\n{'='*70}")
        print("ORGANIZATIONAL HIERARCHY")
        print(f"{'='*70}\n")

        print("""
                        ┌─────────────────┐
                        │   SUPERVISOR    │
                        │   Project Lead  │
                        └────────┬────────┘
                                 │
                    ┌────────────┼────────────┐
                    │            │            │
            ┌───────▼────┐ ┌────▼────┐ ┌────▼─────┐
            │  FRONTEND  │ │ BACKEND  │ │  DEVOPS  │
            │ Specialist │ │Specialist│ │Specialist│
            └────────────┘ └──────────┘ └──────────┘
                    │            │            │
            Task: UI Design  Task: API  Task: Infra
        """)

        print("\nStatus de Tareas:")
        for task in self.tasks:
            status_icon = {
                TaskStatus.PENDING: "⏳",
                TaskStatus.IN_PROGRESS: "🔄",
                TaskStatus.COMPLETED: "✓",
                TaskStatus.FAILED: "✗"
            }
            print(f"{status_icon[task.status]} [{task.assigned_to}] {task.id}: {task.status.value}")

    def print_hierarchy_log(self):
        """Imprime el log de la jerarquía"""

        print(f"\n{'='*70}")
        print("HIERARCHY EXECUTION LOG")
        print(f"{'='*70}\n")

        for i, log_entry in enumerate(self.hierarchy_log, 1):
            print(f"{i:2}. {log_entry}")

        print("\n" + "="*70)
        print("CHARACTERISTICS OF HIERARCHICAL PATTERN")
        print("="*70)
        print("""
Ventajas:
  ✓ Estructura clara y organizada
  ✓ Fácil delegación de tareas
  ✓ Escalabilidad: añadir más especialistas es simple
  ✓ Supervisor toma decisiones finales
  ✓ Ideal para proyectos grandes

Desventajas:
  ✗ Cuello de botella en supervisor
  ✗ Menos flexible que otros patrones
  ✗ Requiere que supervisor entienda todos los dominios
        """)


def main():
    """Ejecuta ejemplo del patrón jerárquico"""

    team = HierarchicalTeam()

    project_description = """
    Proyecto: Desarrollar una aplicación web de e-commerce
    - Interfaz moderna y responsiva
    - Backend escalable con APIs REST
    - Infraestructura en cloud segura
    - Autenticación segura de usuarios
    """

    team.run_project(project_description)
    team.print_hierarchy_visualization()
    team.print_hierarchy_log()


if __name__ == "__main__":
    main()
