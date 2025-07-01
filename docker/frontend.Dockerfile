FROM node:20-slim
WORKDIR /app
COPY frontend/package.json ./package.json
RUN npm install
COPY frontend ./frontend
RUN npm run build --prefix ./frontend
CMD ["npm", "start", "--prefix", "./frontend"]
