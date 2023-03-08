# Set base image
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy package.json and install packages
COPY package.json yarn.lock ./
RUN yarn install

# Copy other project files
COPY . .

# Port number
EXPOSE 3000

# Start the app
CMD ["yarn", "start"]