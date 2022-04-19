# Deployment to production
The following instructions will describe how to deploy this application on an apache server. These instructions will assume the following:
* You have an apache server with a registred domain
* You have docker, and docker compose installed on the server
* You have sudo to the server where you deploy the application

## Installation

First clone the repository to where you want it:
```
git clone https://github.com/Fattigman/docker-sc2reporter
```
Then we need to start the docker network. The docker network will first be built, which we will see in the terminal. However when the build is done, the containers will be launched in detached mode, because of the -d, so you won't see the outputs of the docker.
```
cd docker-sc2reporter
docker-compose up -d
```
