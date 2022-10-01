FROM node:16.17.1

WORKDIR /usr/src/app

RUN npm install -g npm@latest

COPY package*.json ./
RUN npm cache clear --force
RUN npm install
