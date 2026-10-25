
FROM node:22-alpine

WORKDIR /app

EXPOSE 3000

CMD ["sh", "-c", "if [ ! -f package.json ]; then npx nuxi@latest init . --packageManager npm --no-gitInit; fi && npm install && npm run dev -- --host 0.0.0.0"]
