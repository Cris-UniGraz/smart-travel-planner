from fastapi import APIRouter, Depends, HTTPException
from ..core.llm_service import LLMService
from ..models.chat import ChatRequest, ChatResponse, Message, Conversation
import uuid
import os
from typing import Dict

router = APIRouter()

# Simulación de base de datos en memoria
conversations: Dict[str, Conversation] = {}

# Creamos una instancia del servicio LLM
llm_service = LLMService()

@router.get("/test")
async def test_endpoint():
    """Endpoint de prueba para verificar si la API está funcionando"""
    env_status = {
        "AZURE_OPENAI_API_KEY": "configurado" if os.getenv("AZURE_OPENAI_API_KEY") else "no configurado",
        "AZURE_OPENAI_API_VERSION": os.getenv("AZURE_OPENAI_API_VERSION"),
        "AZURE_OPENAI_ENDPOINT": os.getenv("AZURE_OPENAI_ENDPOINT"),
        "AZURE_OPENAI_API_LLM_DEPLOYMENT_ID": os.getenv("AZURE_OPENAI_API_LLM_DEPLOYMENT_ID"),
        "AZURE_OPENAI_LLM_MODEL": os.getenv("AZURE_OPENAI_LLM_MODEL")
    }
    return {
        "status": "API funcionando correctamente",
        "variables_entorno": env_status,
        "llm_client_status": "inicializado" if llm_service.client is not None else "no inicializado"
    }

@router.get("/test-azure")
async def test_azure_connection():
    """Endpoint para probar la conexión con Azure OpenAI"""
    result = llm_service.test_connection()
    return result

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    # Si no se proporciona ID de conversación, crear uno nuevo
    conversation_id = request.conversation_id or str(uuid.uuid4())
    
    # Obtener o crear la conversación
    if conversation_id not in conversations:
        conversations[conversation_id] = Conversation(id=conversation_id)
    
    conversation = conversations[conversation_id]
    
    # Convertir mensajes para el formato requerido por el LLM
    messages_history = [{"role": msg.role, "content": msg.content} for msg in conversation.messages]
    
    # Generar respuesta
    response_text = llm_service.generate_response(request.message, messages_history)
    
    # Formatear respuesta y extraer entidades
    formatted_response = llm_service.format_response(response_text)
    
    # Actualizar el historial de la conversación
    conversation.messages.append(Message(role="user", content=request.message))
    conversation.messages.append(Message(role="assistant", content=response_text))
    
    # Devolver respuesta
    return ChatResponse(
        message=formatted_response["text"],
        extracted_entities=formatted_response["extracted_entities"],
        conversation_id=conversation_id
    )

@router.get("/conversations/{conversation_id}", response_model=Conversation)
async def get_conversation(conversation_id: str):
    if conversation_id not in conversations:
        raise HTTPException(status_code=404, detail="Conversación no encontrada")
    
    return conversations[conversation_id]