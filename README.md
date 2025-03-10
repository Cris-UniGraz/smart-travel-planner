# Smart Travel Planner

Asistente de viajes inteligente para la Universidad de Graz utilizando Azure OpenAI.

## Requisitos para desarrollo local en Windows 11

- [Python 3.11](https://www.python.org/downloads/) o superior
- [Node.js 18](https://nodejs.org/en/download/) o superior
- [Docker Desktop para Windows](https://www.docker.com/products/docker-desktop/)
- [VS Code](https://code.visualstudio.com/download) (recomendado)

## Configuración del entorno

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/smart-travel-planner.git
cd smart-travel-planner
```

### 2. Configurar variables de entorno para el backend

Crea un archivo `.env` en la carpeta `backend` basado en el archivo `.env.example`:

```bash
cd backend
copy .env.example .env
```

Edita el archivo `.env` con tus credenciales de Azure OpenAI.

### 3. Configurar variables de entorno para el frontend

Crea un archivo `.env.local` en la carpeta `frontend` basado en el archivo `.env.local.example`:

```bash
cd ../frontend
copy .env.local.example .env.local
```

## Ejecución local

### Opción 1: Ejecución directa

#### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend

En otra terminal:

```bash
cd frontend
npm install
npm run dev
```

Accede a la aplicación en http://localhost:3000

### Opción 2: Ejecución con Docker Compose

La forma más sencilla de ejecutar ambos servicios es utilizando Docker Compose:

```bash
docker-compose up -d
```

Esto iniciará tanto el backend como el frontend. Accede a la aplicación en http://localhost:3000

## Pruebas

Una vez que la aplicación esté en funcionamiento, podrás interactuar con el asistente de viajes. 
El asistente resaltará lugares o servicios específicos que menciona entre corchetes, 
como [Museo de Historia Natural], para facilitar la identificación de entidades.

## Nota importante

Asegúrate de tener credenciales válidas para Azure OpenAI. Puedes obtenerlas desde 
el portal de Azure si tienes acceso a Azure OpenAI Service.