FROM node:20.10.0

WORKDIR /usr/src/app

RUN npm install -g npm@latest

COPY package*.json ./
RUN npm cache clear --force
RUN npm install
