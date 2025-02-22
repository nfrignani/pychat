FROM node:18

WORKDIR /app

COPY package*.json ./

# Installa le dipendenze
RUN npm ci --silent

# Installa react-scripts
RUN npm install react-scripts --save-dev

COPY . .

# Esegui il comando build
RUN npm run build

# Avvia il server di sviluppo
CMD ["npm", "start"]