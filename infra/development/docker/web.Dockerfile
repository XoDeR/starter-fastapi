FROM node:22-alpine

WORKDIR /app

COPY web/ /app/

EXPOSE 5173

# Placeholder until the React 19 Vite app lands in web/.
# Intended later:
#   npm install
#   npm run dev -- --host 0.0.0.0 --port 5173
CMD ["sleep", "infinity"]
