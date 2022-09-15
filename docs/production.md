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
Then we need to add a user for us to access the site. You will get some prompts which tells you fill in the required fields. After this we should have a site that is reachable via IP. Remember the user name and password!
```
cd utils
python add_user.py 
```

Now we need to configure the apache web server to listen at port 8000 from the localhost. The sc2.conf file tells your apache server to add /sc2rep endpoint to the existing domain, and relay the traffic from that endpoint to the docker container. So we need to move the conf files to where you keep your other conf files.

```
cd ..
mv conf.d/sc2.conf /etc/apachefolder/modulefolder/conf.d/
sudo apachectl restart
```

This will move apache config file to the module directory and restart the server. Now you should be able to open the application at \<your-domain-name\>/sc2rep

## Populating the database
To populate the database you will need to install on your system from:
https://www.perl.org/get.html
And then install mongodb
```
cpanm MongoDB
```
You will also need to move vcf2.pm to the module library of your perl.

Then configure load_data.sh from utils/ such that it point towards the output data from the Arctic pipeline.
Run it the using:
```
bash load_data.sh
```
