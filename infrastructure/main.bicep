@description('Especifica la ubicación de los recursos')
param location string = resourceGroup().location

@description('El nombre del registro de contenedores')
param containerRegistryName string = 'smarttravelplanneracr${uniqueString(resourceGroup().id)}'

@description('El nombre de la aplicación del backend')
param backendAppName string = 'smart-travel-planner-api'

@description('El nombre de la aplicación del frontend')
param frontendAppName string = 'smart-travel-planner-web'

@description('Etiqueta de la imagen del backend')
param backendImageTag string = 'latest'

@description('Etiqueta de la imagen del frontend')
param frontendImageTag string = 'latest'

// Variables para los nombres de las imágenes
var backendImageName = '${containerRegistryName}.azurecr.io/${backendAppName}:${backendImageTag}'
var frontendImageName = '${containerRegistryName}.azurecr.io/${frontendAppName}:${frontendImageTag}'

// Azure Container Registry
module registry './container-registry.bicep' = {
  name: 'registry-deployment'
  params: {
    containerRegistryName: containerRegistryName
    location: location
  }
}

// Backend Container App
module backendApp './container-app.bicep' = {
  name: 'backend-app-deployment'
  params: {
    name: backendAppName
    location: location
    containerRegistryName: containerRegistryName
    imageName: backendImageName
    targetPort: 8000
    isExternalIngress: true
    environmentVariables: [
      {
        name: 'AZURE_OPENAI_API_KEY'
        secretRef: 'azure-openai-api-key'
      }
      {
        name: 'AZURE_OPENAI_API_VERSION'
        value: '2023-05-15'
      }
      {
        name: 'AZURE_OPENAI_ENDPOINT'
        secretRef: 'azure-openai-endpoint'
      }
      {
        name: 'AZURE_OPENAI_API_LLM_DEPLOYMENT_ID'
        secretRef: 'azure-openai-deployment-id'
      }
      {
        name: 'AZURE_OPENAI_LLM_MODEL'
        value: 'gpt-4'
      }
    ]
  }
  dependsOn: [
    registry
  ]
}

// Frontend Container App
module frontendApp './container-app.bicep' = {
  name: 'frontend-app-deployment'
  params: {
    name: frontendAppName
    location: location
    containerRegistryName: containerRegistryName
    imageName: frontendImageName
    targetPort: 3000
    isExternalIngress: true
    environmentVariables: [
      {
        name: 'API_URL'
        value: 'https://${backendApp.outputs.fqdn}/api/v1'
      }
    ]
  }
  dependsOn: [
    registry
    backendApp
  ]
}

// Outputs
output backendUrl string = 'https://${backendApp.outputs.fqdn}'
output frontendUrl string = 'https://${frontendApp.outputs.fqdn}'