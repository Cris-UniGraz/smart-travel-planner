from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from .api.routes import router as api_router
from .core.config import settings
import os

# Crear la aplicación FastAPI
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rutas de API
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {"message": "Bienvenido a Smart Travel Planner API"}

@app.get("/api")
async def api_redirect():
    """Redirecciona a /api/v1/test para facilitar las pruebas"""
    return RedirectResponse(url="/api/v1/test")

@app.get("/check-env")
async def check_env():
    """Endpoint para verificar las variables de entorno"""
    env_vars = {
        "AZURE_OPENAI_API_KEY": "configurado" if os.getenv("AZURE_OPENAI_API_KEY") else "no configurado",
        "AZURE_OPENAI_API_VERSION": os.getenv("AZURE_OPENAI_API_VERSION"),
        "AZURE_OPENAI_ENDPOINT": os.getenv("AZURE_OPENAI_ENDPOINT"),
        "AZURE_OPENAI_API_LLM_DEPLOYMENT_ID": os.getenv("AZURE_OPENAI_API_LLM_DEPLOYMENT_ID"),
        "AZURE_OPENAI_LLM_MODEL": os.getenv("AZURE_OPENAI_LLM_MODEL"),
    }
    
    return {
        "status": "Variables de entorno verificadas",
        "variables": env_vars
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)