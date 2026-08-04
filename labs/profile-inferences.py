import boto3

# Inicializa el cliente de Bedrock Runtime en tu región de origen (Source Region)
client = boto3.client(
    service_name='bedrock-runtime', 
    region_name='us-east-1'
)

# 1. IN-REGION: Usa el ID tradicional del modelo sin prefijos geográficos
model_in_region = 'anthropic.claude-3-5-sonnet-20241022-v2:0'

# 2. GEO CROSS-REGION: Añade el prefijo de la geografía (ej. 'us.' o 'eu.')
model_geo_cross = 'us.anthropic.claude-3-5-sonnet-20241022-v2:0'

# 3. GLOBAL CROSS-REGION: Añade el prefijo 'global.' para enrutamiento mundial
model_global_cross = 'global.anthropic.claude-3-5-sonnet-20241022-v2:0'

# Realiza la petición usando cualquiera de los IDs anteriores
response = client.converse(
    modelId=model_geo_cross,  # Cambia esta variable según lo que necesites
    messages=[
        {
            'role': 'user',
            'content': [{'text': 'Hola, dime un dato curioso.'}]
        }
    ]
)

print(response['output']['message']['content'][0]['text'])

