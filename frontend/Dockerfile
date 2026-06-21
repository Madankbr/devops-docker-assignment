FROM node:20-slim

WORKDIR /app

# Install dependencies first (better layer caching)
COPY package*.json ./
RUN npm install --production

# Copy application code
COPY . .

EXPOSE 3000

CMD ["node", "server.js"]
