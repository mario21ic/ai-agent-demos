"""
AWS Pattern: Observer and Monitoring Agent
===========================================
Agente que monitorea sistemas, detecta anomalías y actúa
sobre eventos de observación.

Principios AWS:
- Asincrónico: Monitorea continuamente
- Autonomía: Detecta y actúa sin intervención
- Agencia: Responde a cambios de estado
"""

from strands import Agent
from typing import Dict, List, Any
from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class AlertSeverity(Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


class SystemMetric(Enum):
    CPU_USAGE = "cpu_usage"
    MEMORY_USAGE = "memory_usage"
    DISK_SPACE = "disk_space"
    API_LATENCY = "api_latency"
    ERROR_RATE = "error_rate"
    THROUGHPUT = "throughput"


@dataclass
class SystemObservation:
    """Una observación del sistema"""
    timestamp: datetime
    metric: SystemMetric
    value: float
    threshold: float
    status: str  # "normal", "warning", "critical"


@dataclass
class Alert:
    """Una alerta generada"""
    timestamp: datetime
    severity: AlertSeverity
    metric: SystemMetric
    message: str
    recommended_action: str


class ObserverMonitoringAgent:
    """Agente que monitorea sistemas y genera alertas"""

    def __init__(self):
        # Agente monitor
        self.monitor = Agent(
            system_prompt="""Eres un agente monitor de sistemas.
            Tu tarea es:
            1. Observar métricas del sistema
            2. Detectar anomalías
            3. Evaluar severidad
            4. Recomendar acciones

            Sé proactivo en la detección."""
        )

        # Agente responder
        self.responder = Agent(
            system_prompt="""Eres un agente responder de incidentes.
            Tu tarea es:
            1. Analizar alertas
            2. Determinar causa raíz
            3. Ejecutar acciones remediales
            4. Escalar si es necesario"""
        )

        self.observations: List[SystemObservation] = []
        self.alerts: List[Alert] = []
        self.alert_log: List[Dict] = []

    def collect_metric(self, metric: SystemMetric, value: float, threshold: float):
        """Recolecta una métrica del sistema"""

        # Determinar status
        if value > threshold:
            status = "critical" if value > threshold * 1.5 else "warning"
        else:
            status = "normal"

        observation = SystemObservation(
            timestamp=datetime.now(),
            metric=metric,
            value=value,
            threshold=threshold,
            status=status
        )

        self.observations.append(observation)

        if status != "normal":
            self._generate_alert(observation)

    def _generate_alert(self, observation: SystemObservation):
        """Genera una alerta para una observación crítica"""

        severity = AlertSeverity.CRITICAL if observation.status == "critical" else AlertSeverity.WARNING

        # Usar agente monitor para describir
        analysis_prompt = f"""
        Métrica: {observation.metric.value}
        Valor: {observation.value}
        Umbral: {observation.threshold}
        Estado: {observation.status}

        Genera:
        1. Un mensaje de alerta claro
        2. Una acción recomendada

        Formato:
        Mensaje: ...
        Acción: ...
        """

        analysis = self.monitor(analysis_prompt)

        # Parsear respuesta
        lines = analysis.split('\n')
        message = lines[0] if lines else "System anomaly detected"
        action = lines[1] if len(lines) > 1 else "Review system status"

        alert = Alert(
            timestamp=datetime.now(),
            severity=severity,
            metric=observation.metric,
            message=message,
            recommended_action=action
        )

        self.alerts.append(alert)

    def simulate_system_monitoring(self):
        """Simula monitoreo de un sistema"""

        print(f"\n{'='*70}")
        print("OBSERVER & MONITORING AGENT")
        print(f"{'='*70}\n")

        print("🔍 System Monitoring Simulation\n")

        # Recolectar métricas (simuladas)
        metrics_data = [
            (SystemMetric.CPU_USAGE, 45.0, 80.0, "Normal CPU usage"),
            (SystemMetric.MEMORY_USAGE, 92.0, 85.0, "High memory usage"),
            (SystemMetric.DISK_SPACE, 95.0, 90.0, "Critical disk space"),
            (SystemMetric.API_LATENCY, 2500, 1000, "High API latency"),
            (SystemMetric.ERROR_RATE, 5.2, 2.0, "Elevated error rate"),
            (SystemMetric.THROUGHPUT, 1200, 1500, "Lower than expected throughput"),
        ]

        for metric, value, threshold, description in metrics_data:
            print(f"📊 {metric.value}: {value}")
            print(f"   Threshold: {threshold}")
            print(f"   Status: {'✓' if value <= threshold else '⚠️'} ({description})")

            self.collect_metric(metric, value, threshold)
            print()

    def respond_to_alerts(self):
        """Responde a las alertas generadas"""

        if not self.alerts:
            print("✓ No alerts to respond to\n")
            return

        print(f"\n{'='*70}")
        print("ALERT RESPONSE")
        print(f"{'='*70}\n")

        print(f"Total Alerts: {len(self.alerts)}\n")

        for i, alert in enumerate(self.alerts, 1):
            print(f"{i}. [{alert.severity.value.upper()}] {alert.metric.value}")
            print(f"   Message: {alert.message}")

            # Responder a la alerta
            response_prompt = f"""
            Alerta de {alert.metric.value}:
            {alert.message}

            Acción recomendada: {alert.recommended_action}

            ¿Cuáles son los pasos concretos para resolver esto?
            Prioridad: {alert.severity.value}

            Proporciona:
            1. Diagnóstico
            2. Pasos a tomar
            3. Urgencia
            """

            response = self.responder(response_prompt)
            print(f"   Response: {response[:150]}...")

            self.alert_log.append({
                "alert": alert,
                "response": response,
                "timestamp": datetime.now()
            })

            print()

    def detect_anomalies(self):
        """Detecta patrones anómalos en los datos"""

        print(f"\n{'='*70}")
        print("ANOMALY DETECTION")
        print(f"{'='*70}\n")

        if len(self.observations) < 3:
            print("Not enough observations for anomaly detection\n")
            return

        # Análisis de patrones
        anomaly_prompt = f"""
        Observaciones del sistema:
        """

        for obs in self.observations[-5:]:
            anomaly_prompt += f"\n- {obs.metric.value}: {obs.value} (threshold: {obs.threshold})"

        anomaly_prompt += f"""

        Analiza estos datos para:
        1. Patrones inusuales
        2. Tendencias preocupantes
        3. Anomalías potenciales
        4. Correlaciones entre métricas

        ¿Hay algún patrón anómalo?
        """

        analysis = self.monitor(anomaly_prompt)
        print("Anomaly Analysis:")
        print(analysis)

    def print_monitoring_summary(self):
        """Imprime resumen del monitoreo"""

        print(f"\n{'='*70}")
        print("MONITORING SUMMARY")
        print(f"{'='*70}\n")

        print(f"Total Observations: {len(self.observations)}")
        print(f"Total Alerts: {len(self.alerts)}")
        print(f"Critical Alerts: {len([a for a in self.alerts if a.severity == AlertSeverity.CRITICAL])}")
        print(f"Warning Alerts: {len([a for a in self.alerts if a.severity == AlertSeverity.WARNING])}")

        if self.alerts:
            print(f"\nRecent Alerts:")
            for alert in self.alerts[-3:]:
                print(f"  • [{alert.severity.value}] {alert.metric.value}: {alert.message}")

        print("\n" + "="*70)
        print("OBSERVER & MONITORING AGENT CHARACTERISTICS")
        print("="*70)
        print("""
Ventajas:
  ✓ Monitoreo 24/7
  ✓ Detección automática de anomalías
  ✓ Respuesta rápida
  ✓ Escalable a múltiples sistemas
  ✓ Historial auditado

Desventajas:
  ✗ Falsos positivos
  ✗ Tuning de thresholds complejo
  ✗ Latencia en detección
  ✗ Costo computacional

AWS Pattern: OBSERVER & MONITORING
  → CloudWatch integration
  → EventBridge para eventos
  → SNS para notificaciones
  → Lambda para respuesta automática

Casos de Uso:
  • Monitoreo de infraestructura
  • Detección de fraude
  • Alertas de performance
  • Compliance monitoring
        """)


def main():
    """Ejecuta ejemplo de Observer Monitoring Agent"""

    agent = ObserverMonitoringAgent()

    # Monitoreo del sistema
    agent.simulate_system_monitoring()

    # Responder a alertas
    agent.respond_to_alerts()

    # Detectar anomalías
    agent.detect_anomalies()

    # Resumen
    agent.print_monitoring_summary()


if __name__ == "__main__":
    main()
