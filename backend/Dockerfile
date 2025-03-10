FROM python:3.11-slim

WORKDIR /app

# Copiar los archivos de requerimientos
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente
COPY . .

# Exponer el puerto
EXPOSE 8000

# Crear un script para imprimir las variables de entorno antes de iniciar la aplicación
RUN echo '#!/bin/bash\necho "Variables de entorno al iniciar:"\necho "AZURE_OPENAI_API_KEY: ${AZURE_OPENAI_API_KEY:0:3}..."\necho "AZURE_OPENAI_API_VERSION: $AZURE_OPENAI_API_VERSION"\necho "AZURE_OPENAI_ENDPOINT: $AZURE_OPENAI_ENDPOINT"\necho "AZURE_OPENAI_API_LLM_DEPLOYMENT_ID: $AZURE_OPENAI_API_LLM_DEPLOYMENT_ID"\necho "AZURE_OPENAI_LLM_MODEL: $AZURE_OPENAI_LLM_MODEL"\nuvicorn app.main:app --host 0.0.0.0 --port 8000' > /app/start.sh && chmod +x /app/start.sh

# Comando para iniciar la aplicación
CMD ["/app/start.sh"]