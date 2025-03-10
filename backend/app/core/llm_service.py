import os
import re
from openai import AzureOpenAI
from ..core.config import settings

class LLMService:
    def __init__(self):
        try:
            self.system_prompt = self.load_system_prompt()
            
            # Verificar si las variables de entorno están configuradas
            if not settings.AZURE_OPENAI_API_KEY:
                print("ADVERTENCIA: AZURE_OPENAI_API_KEY no está configurada.")
                self.client = None
                return
                
            if not settings.AZURE_OPENAI_ENDPOINT:
                print("ADVERTENCIA: AZURE_OPENAI_ENDPOINT no está configurada.")
                self.client = None
                return
                
            if not settings.AZURE_OPENAI_API_LLM_DEPLOYMENT_ID:
                print("ADVERTENCIA: AZURE_OPENAI_API_LLM_DEPLOYMENT_ID no está configurada.")
                self.client = None
                return
                
            # Si todas las variables están configuradas, crear el cliente
            print("Intentando crear cliente AzureOpenAI con los siguientes parámetros:")
            print(f"  API Key: {'***' + settings.AZURE_OPENAI_API_KEY[-4:] if settings.AZURE_OPENAI_API_KEY else 'No configurada'}")
            print(f"  API Version: {settings.AZURE_OPENAI_API_VERSION}")
            print(f"  Endpoint: {settings.AZURE_OPENAI_ENDPOINT}")
            print(f"  Deployment ID: {settings.AZURE_OPENAI_API_LLM_DEPLOYMENT_ID}")
            print(f"  Model: {settings.AZURE_OPENAI_LLM_MODEL}")
            
            # Mostrar información sobre la versión de openai
            import sys
            print(f"Python versión: {sys.version}")
            
            try:
                # Para la versión 1.3.0 de OpenAI, la inicialización correcta es:
                self.client = AzureOpenAI(
                    api_key=settings.AZURE_OPENAI_API_KEY,
                    api_version=settings.AZURE_OPENAI_API_VERSION,
                    azure_endpoint=settings.AZURE_OPENAI_ENDPOINT
                )
                print(f"Cliente inicializado con endpoint: {settings.AZURE_OPENAI_ENDPOINT}")
                print("Cliente AzureOpenAI creado exitosamente.")
            except TypeError as type_error:
                print(f"Error de tipo al crear el cliente: {str(type_error)}")
                # Intentar con un enfoque alternativo si hay error de tipo
                try:
                    import openai
                    print(f"Versión OpenAI: {openai.__version__}")
                    
                    # Configuración alternativa
                    openai.api_key = settings.AZURE_OPENAI_API_KEY
                    openai.api_base = settings.AZURE_OPENAI_ENDPOINT
                    openai.api_version = settings.AZURE_OPENAI_API_VERSION
                    openai.api_type = "azure"
                    
                    self.client = openai
                    print("Cliente OpenAI configurado usando método alternativo.")
                except Exception as alt_error:
                    print(f"Error al intentar configuración alternativa: {str(alt_error)}")
                    self.client = None
        except Exception as e:
            print(f"Error al inicializar LLMService: {str(e)}")
            self.client = None
    
    def test_connection(self):
        """Prueba la conexión con Azure OpenAI"""
        if self.client is None:
            return {
                "success": False, 
                "message": "Cliente no inicializado. Verifica las credenciales."
            }
            
        try:
            # Intentar una llamada simple al API
            deployment_id = settings.AZURE_OPENAI_API_LLM_DEPLOYMENT_ID
            print(f"Usando deployment_id para la petición: {deployment_id}")
            
            # Verificar si estamos usando el cliente de la API nueva o la vieja
            import openai
            print(f"OpenAI API version: {openai.__version__}")
            
            if hasattr(self.client, "chat") and hasattr(self.client.chat, "completions"):
                # Nueva API (Cliente AzureOpenAI)
                print("Usando el cliente AzureOpenAI nuevo")
                response = self.client.chat.completions.create(
                    model=deployment_id,
                    messages=[{"role": "user", "content": "Hola, esta es una prueba de conexión."}]
                )
                return {
                    "success": True,
                    "message": "Conexión exitosa con Azure OpenAI.",
                    "response": response.choices[0].message.content
                }
            else:
                # API Legacy
                print("Usando el cliente OpenAI legacy")
                response = self.client.ChatCompletion.create(
                    engine=deployment_id,
                    messages=[{"role": "user", "content": "Hola, esta es una prueba de conexión."}]
                )
                return {
                    "success": True,
                    "message": "Conexión exitosa con Azure OpenAI (API legacy).",
                    "response": response.choices[0].message["content"]
                }
        except Exception as e:
            print(f"Error detallado en test_connection: {str(e)}")
            return {
                "success": False,
                "message": f"Error al conectar con Azure OpenAI: {str(e)}"
            }
    
    def load_system_prompt(self):
        prompt_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "prompts", "systemprompt.txt")
        try:
            with open(prompt_path, "r", encoding="utf-8") as file:
                return file.read().strip()
        except FileNotFoundError:
            raise FileNotFoundError(f"El archivo de prompt del sistema no fue encontrado en: {prompt_path}")
    
    def generate_response(self, prompt: str, messages_history: list) -> str:
        # Si el cliente no está inicializado, devolver un mensaje de error
        if self.client is None:
            return "Lo siento, no puedo generar una respuesta en este momento porque las credenciales de Azure OpenAI no están configuradas correctamente. Por favor, contacta al administrador del sistema."
            
        try:
            conversation_messages = [{"role": "system", "content": self.system_prompt}]
            conversation_messages.extend(messages_history)
            conversation_messages.append({"role": "user", "content": prompt})
            
            # Usar el deployment_id como modelo
            deployment_id = settings.AZURE_OPENAI_API_LLM_DEPLOYMENT_ID
            
            # Verificar si estamos usando el cliente de la API nueva o la vieja
            if hasattr(self.client, "chat") and hasattr(self.client.chat, "completions"):
                # Nueva API (Cliente AzureOpenAI)
                print("Generando respuesta con cliente AzureOpenAI nuevo")
                response = self.client.chat.completions.create(
                    model=deployment_id,
                    messages=conversation_messages
                )
                return response.choices[0].message.content
            else:
                # API Legacy
                print("Generando respuesta con cliente OpenAI legacy")
                response = self.client.ChatCompletion.create(
                    engine=deployment_id,
                    messages=conversation_messages
                )
                return response.choices[0].message["content"]
        except Exception as e:
            print(f"Error al generar respuesta: {str(e)}")
            return f"Lo siento, ocurrió un error al procesar tu mensaje: {str(e)}"
    
    @staticmethod
    def format_response(response_text: str) -> dict:
        # Extraer texto entre corchetes para posibles acciones o entidades
        bracketed_items = re.findall(r'\[(.*?)\]', response_text)
        
        return {
            "text": response_text,
            "extracted_entities": bracketed_items
        }