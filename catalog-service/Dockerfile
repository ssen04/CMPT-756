# Dockerfile básico para Node.js/TypeScript
FROM node:20-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

RUN npm run build   # si usas TypeScript

EXPOSE 3000
CMD ["node", "dist/index.js"]  # o el archivo principal de tu app