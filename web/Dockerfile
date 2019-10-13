FROM node:12.2.0-alpine

# set working directory
WORKDIR /app

# add `/app/node_modules/.bin` to $PATH
ENV PATH /app/node_modules/.bin:$PATH

COPY package.json /app/
COPY yarn.lock /app/
RUN yarn install

COPY . .

ENTRYPOINT [ "yarn" ]
CMD [ "start" ]
