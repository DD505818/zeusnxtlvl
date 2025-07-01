FROM node:20-alpine
WORKDIR /app
COPY ../frontend /app
RUN npm install
RUN npm run build
CMD ["npm", "start"]
