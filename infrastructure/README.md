# Smart Travel Planner - Infraestructura en Azure

Este directorio contiene los archivos de infraestructura como código (IaC) necesarios para desplegar la aplicación Smart Travel Planner en Azure usando Bicep.

## Arquitectura

La infraestructura está compuesta por:

- Azure Container Registry: Para almacenar las imágenes Docker
- Azure Container Apps: Para ejecutar las aplicaciones en contenedores
- Log Analytics Workspace: Para almacenar y analizar los logs de la aplicación

## Prerrequisitos

- Azure CLI instalado
- Suscripción de Azure
- Permisos para crear recursos en Azure

## Configuración de secretos

Antes de desplegar la aplicación, necesitas configurar los siguientes secretos:

```bash
# Crear un grupo de recursos si no existe
az group create --name smart-travel-planner-rg --location eastus

# Configurar los secretos para Azure OpenAI
az containerapp secret set \
  --name smart-travel-planner-api \
  --resource-group smart-travel-planner-rg \
  --secrets "azure-openai-api-key=su-api-key" \
                "azure-openai-endpoint=https://su-recurso-openai.openai.azure.com/" \
                "azure-openai-deployment-id=su-deployment-id"
```

## Despliegue

Para desplegar la infraestructura:

```bash
# Login en Azure
az login

# Desplegar usando Bicep
az deployment group create \
  --resource-group smart-travel-planner-rg \
  --template-file ./main.bicep \
  --parameters location=eastus
```

## Verificación del despliegue

Después del despliegue, puedes verificar la aplicación con:

```bash
# Obtener la URL del frontend
az containerapp show \
  --name smart-travel-planner-web \
  --resource-group smart-travel-planner-rg \
  --query properties.configuration.ingress.fqdn -o tsv

# Obtener la URL del backend
az containerapp show \
  --name smart-travel-planner-api \
  --resource-group smart-travel-planner-rg \
  --query properties.configuration.ingress.fqdn -o tsv
```