import random
import time
import boto3
from botocore.config import Config
from botocore.exceptions import ClientError

# 1. Configurar los reintentos nativos de Boto3 con Jitter
# El modo 'standard' utiliza retroceso exponencial con jitter de forma automática
configuracion_retry = Config(
    retries={
        'max_attempts': 5,          # Número máximo de reintentos
        'mode': 'standard'          # Aplica jitter exponencial automáticamente
    }
)

# 2. Inicializar el cliente de Bedrock con la configuración
cliente_bedrock = boto3.client(
    service_name='bedrock-runtime',
    region_name='us-east-1',
    config=configuracion_retry
)

def invocar_modelo_con_jitter_manual(prompt: str):
    """
    Ejemplo de invocación con lógica manual de jitter para un control total.
    """
    intentos_maximos = 5
    base_backoff = 2  # Segundos
    
    for intento in range(intentos_maximos):
        try:
            # Reemplazar con el ID de modelo deseado (ej. Anthropic Claude, Meta Llama)
            #id_modelo = 'amazon.titan-text-express-v1'
            id_modelo = 'amazon.nova-2-lite-v1:0'
            
            response = cliente_bedrock.invoke_model(
                modelId=id_modelo,
                body=f'{{"inputText": "{prompt}"}}'
            )
            return response
            
        except ClientError as e:
            codigo_error = e.response['Error']['Code']
            
            # Verificar si es un error de saturación (429 / Throttling)
            if codigo_error in ['ThrottlingException', 'TooManyRequestsException']:
                if intento == intentos_maximos - 1:
                    print("Se alcanzó el límite máximo de reintentos.")
                    raise e
                
                # --- ALGORITMO DE JITTER TOTAL (Full Jitter) ---
                # Retroceso exponencial: base * (2 ^ intento)
                backoff_maximo = base_backoff * (2 ** intento)
                
                # Jitter: Elegir un tiempo aleatorio entre 0 y el backoff máximo
                tiempo_espera = random.uniform(0, backoff_maximo)
                
                print(f"Saturación detectada. Intento {intento + 1}. Esperando {tiempo_espera:.2f} segundos...")
                time.sleep(tiempo_espera)
            else:
                # Si es otro tipo de error, lanzarlo inmediatamente
                raise e

# Ejemplo de uso
if __name__ == "__main__":
    try:
        resultado = invocar_modelo_con_jitter_manual("¿Cuál es el origen del jitter?")
        print("Solicitud exitosa.")
    except Exception as e:
        print(f"Error final en la ejecución: {e}")

