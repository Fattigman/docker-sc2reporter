# Set base image
FROM node:18-alpine

# Copy the directory for making a build
COPY . /build_dir/

# Change the workdir for easier execution of command
WORKDIR /build_dir

# Install all the dependencies, creates a build then remove everything that isn't necessary for the app
RUN yarn install && \
    npm install -g serve && \
    yarn build && \
    mkdir /app && \
    mv build /app/build && \
    rm -rf /build_dir
    
# Create new workdir from which the build is served
WORKDIR /app

# Port number
EXPOSE 3000

# Start the app
CMD ["serve", "-s", "build", "-l", "3000"]