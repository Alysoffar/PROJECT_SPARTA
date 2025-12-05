FROM node:18-alpine

WORKDIR /app

# Copy package files, patch script, and patches directory BEFORE install
COPY package*.json ./
COPY scripts ./scripts
COPY patches ./patches

# Clean install with yarn (respects postinstall and patch-package)
RUN rm -rf node_modules yarn.lock package-lock.json && \
    yarn install

# Copy rest of source
COPY . .

EXPOSE 3000

CMD ["yarn", "start"]
