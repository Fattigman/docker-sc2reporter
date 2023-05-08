# Introduction  <!-- omit in toc -->
SC2Reporter for production is built upon three main technologies:
* Docker - To run each service individually
* Docker-compose - To orchestrate the communication and deployment of all services
* Apache2 - Acts as a reverse proxy for the services

This guide will go through the installation and set up for these tools, assuming that you will start from a clean slate, and install everything on a Fedora/CentOS/Red Hat Enterprise Linux system. This set up commands will not be applicable if you are setting this project up on another system than the previously mentioned, but hopefully you will understand the main objectives of each step and replicate them on your system.

- [Installation](#installation)
  - [Docker + docker-compose](#docker--docker-compose)
  - [Apache](#apache)
- [Configuration](#configuration)
  - [Apache](#apache-1)
    - [Package installation](#package-installation)
    - [SSL configuration](#ssl-configuration)
    - [Reverse proxy set up](#reverse-proxy-set-up)
  - [Docker](#docker)
- [Start up](#start-up)

# Installation
## Docker + docker-compose
To install docker on the system, follow a guide written for your specific system as described on [dockers official documenation](https://docs.docker.com/engine/install/)

Example set up. Skip it if you already have docker + docker-compose installed:
```bash
sudo yum install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin # installs docker and docker-compose
sudo systemctl start docker # Starts a systemd service for docker
sudo docker run hello-world # Tests if docker was installed properly
docker-compose version # Verify that docker-compose has been installed properly
```
If you already have docker installed but not docker-compose installed run the following:
```
sudo yum install docker-compose-plugin # installs docker-compose
docker-compose version # Verify that docker-compose has been installed properly
```
## Apache
To install apache2 on your system, you can follow up-to-date guides on [apache's official home page](https://httpd.apache.org/docs/current/install.html)


Example set up. Skip it if you already have a apache2 configuration running:
```bash
sudo yum install httpd # Installs apache2 package
sudo systemctl enable httpd # Enables apache2 systemd service at boot-time
sudo systemctl start httpd # Starts the apache2 systemd service
hostname -I # Return your systems IP adress
```
Navigate to the IPv4 adress returned by your system and you should be greeted with the default html page for your apache2 service.

# Configuration

## Apache
### Package installation
Install the following modules, if the apache2 installation ran succesfully.
```bash
sudo a2enmod proxy # enables mod_proxy apache module for basic proxy capabilities
sudo a2enmod proxy_http # enables mod_proxy_http for http proxy capabilities
sudo a2enmod ssl # enables ssl for safe communication between apache2 and clients
```

### SSL configuration

To enable ssl for your apache2 instance, you will need to create an apache configuration file in your conf.d folder for your system. Any file that lies within that folder that ends with .conf will be automatically included as a apache configuration. The standard path is `/etc/httpd/conf.d` for a clean slate install. Create the following ssl.conf and move it to your conf.d folder.
```apacheconf
# Minimal ssl configuration
LoadModule ssl_module ../modules/mod_ssl.so 

Listen 443
<VirtualHost *:443>
    ServerName www.example.com
    SSLEngine on
    SSLCertificateFile "/path/to/www.example.com.cert"
    SSLCertificateKeyFile "/path/to/www.example.com.key"
</VirtualHost>
```
You should edit `/path/to/www.example.com.cert` and `/path/to/www.example.com.key` to both cert and key which you have acquired. I will not tell you how to acquire these as there many ways to do so, each specific to your set up and situation. I will tell you that you should try to acquire a ssl cert that has been signed by a third party. For example if you have an IT group, you should contact them and ask them for help.

### Reverse proxy set up
Default proxy configuration is available at `apache-conf/sc2.conf`. Copy these configurations to conf.d folder.
```bash
sudo cp apache-conf/sc2.conf /etc/httpd/conf.d/sc2.conf
```

After you have done all this restart your apache2 instance:
```bash
sudo systemctl restart httpd # Restart your apache2 system service
```

## Docker
In the `docker-compose.yml` edit `REACT_APP_PREFIX_URL=/` to `REACT_APP_PREFIX_URL=/frontend`
# Start up

To finally put the project in production run while standing in the root folder of the github project: 
```bash
docker-compose up -d --build
```
Then navigate to www.example.com/api or www.example.com/frontend (where example.com should be renamed with the name of your server) to make sure it is installed correctly.