@description('El nombre de la aplicación')
param name string

@description('La ubicación de los recursos')
param location string = resourceGroup().location

@description('El nombre del registro de contenedores')
param containerRegistryName string

@description('El nombre completo de la imagen')
param imageName string

@description('El puerto que expone el contenedor')
param targetPort int

@description('Si la aplicación debe ser accesible desde internet')
param isExternalIngress bool = false

@description('Variables de entorno para el contenedor')
param environmentVariables array = []

// Variables
var containerAppEnvName = '${name}-env'
var registryLoginServer = '${containerRegistryName}.azurecr.io'

// Entorno de Container Apps
resource containerAppEnvironment 'Microsoft.App/managedEnvironments@2022-03-01' = {
  name: containerAppEnvName
  location: location
  properties: {
    appLogsConfiguration: {
      destination: 'log-analytics'
      logAnalyticsConfiguration: {
        customerId: logAnalyticsWorkspace.properties.customerId
        sharedKey: logAnalyticsWorkspace.listKeys().primarySharedKey
      }
    }
  }
}

// Log Analytics Workspace
resource logAnalyticsWorkspace 'Microsoft.OperationalInsights/workspaces@2022-10-01' = {
  name: '${name}-logs'
  location: location
  properties: {
    sku: {
      name: 'PerGB2018'
    }
    retentionInDays: 30
    features: {
      enableLogAccessUsingOnlyResourcePermissions: true
    }
  }
}

// Container App
resource containerApp 'Microsoft.App/containerApps@2022-03-01' = {
  name: name
  location: location
  properties: {
    managedEnvironmentId: containerAppEnvironment.id
    configuration: {
      ingress: {
        external: isExternalIngress
        targetPort: targetPort
        allowInsecure: false
        traffic: [
          {
            latestRevision: true
            weight: 100
          }
        ]
      }
      registries: [
        {
          server: registryLoginServer
          identity: 'system'
        }
      ]
    }
    template: {
      containers: [
        {
          name: name
          image: imageName
          env: environmentVariables
          resources: {
            cpu: json('0.5')
            memory: '1.0Gi'
          }
        }
      ]
      scale: {
        minReplicas: 1
        maxReplicas: 10
      }
    }
  }
  identity: {
    type: 'SystemAssigned'
  }
}

// Outputs
output fqdn string = containerApp.properties.configuration.ingress.fqdn