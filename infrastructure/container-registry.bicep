@description('El nombre del registro de contenedores')
param containerRegistryName string

@description('La ubicación de los recursos')
param location string = resourceGroup().location

@description('El SKU del registro de contenedores')
param skuName string = 'Basic'

// Container Registry
resource registry 'Microsoft.ContainerRegistry/registries@2021-09-01' = {
  name: containerRegistryName
  location: location
  sku: {
    name: skuName
  }
  properties: {
    adminUserEnabled: true
  }
}

// Outputs
output loginServer string = registry.properties.loginServer