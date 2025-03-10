import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Cargar variables de entorno
# Buscar el archivo .env en diferentes ubicaciones
env_paths = [
    '.env',
    '/.env',
    '/app/.env',
    os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env')
]

# Intentar cargar desde cada ubicación
for env_path in env_paths:
    if os.path.exists(env_path):
        load_dotenv(env_path)
        print(f"Archivo .env cargado desde: {env_path}")
        break
else:
    print("ADVERTENCIA: No se encontró ningún archivo .env. Las variables de entorno deben estar definidas en el sistema.")

# Imprimir todas las variables de entorno para debug
print("Variables de entorno cargadas:")
print(f"AZURE_OPENAI_API_KEY: {'configurado' if os.getenv('AZURE_OPENAI_API_KEY') else 'no configurado'}")
print(f"AZURE_OPENAI_API_VERSION: {os.getenv('AZURE_OPENAI_API_VERSION')}")
print(f"AZURE_OPENAI_ENDPOINT: {os.getenv('AZURE_OPENAI_ENDPOINT')}")
print(f"AZURE_OPENAI_API_LLM_DEPLOYMENT_ID: {os.getenv('AZURE_OPENAI_API_LLM_DEPLOYMENT_ID')}")
print(f"AZURE_OPENAI_LLM_MODEL: {os.getenv('AZURE_OPENAI_LLM_MODEL')}")

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Smart Travel Planner"
    
    # Azure OpenAI Settings
    AZURE_OPENAI_API_KEY: str = os.getenv("AZURE_OPENAI_API_KEY")
    AZURE_OPENAI_API_VERSION: str = os.getenv("AZURE_OPENAI_API_VERSION")
    AZURE_OPENAI_ENDPOINT: str = os.getenv("AZURE_OPENAI_ENDPOINT")
    AZURE_OPENAI_API_LLM_DEPLOYMENT_ID: str = os.getenv("AZURE_OPENAI_API_LLM_DEPLOYMENT_ID", "gpt-4")
    AZURE_OPENAI_LLM_MODEL: str = os.getenv("AZURE_OPENAI_LLM_MODEL", "gpt-4-0613")
    
    # CORS Settings
    CORS_ORIGINS: list = ["*"]
    
    class Config:
        case_sensitive = True

settings = Settings()