# frontend/Dockerfile
FROM node:18-alpine

# Directorio de trabajo
WORKDIR /app

# Copiar archivos de dependencias
COPY package*.json ./

# Instalar dependencias de Angular
RUN npm install
RUN npm install -g @angular/cli

# Copiar el resto del código
COPY . .

# Exponer el puerto de Angular
EXPOSE 4200

# Comando para ejecutar en modo desarrollo, accesible desde fuera del contenedor
CMD ["ng", "serve", "--host", "0.0.0.0"]