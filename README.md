# Sc2reporter
Finalized version of the SarsCov2 Reporter app, dubbed sc2reporter.


# Usage

TLDR:
have docker-compose installed on your system and run following to get a demo with test data going
```bash
git clone https://github.com/genomic-medicine-sweden/docker-sc2reporter
cd docker-sc2reporter
docker-compose -f docker-compose-demo.yml up
```

Follow the two options described here:
  * [Development](https://github.com/Fattigman/docker-sc2reporter/blob/main/docs/development.md)
  * [Production](https://github.com/Fattigman/docker-sc2reporter/blob/main/docs/production.md)

## Good to know
Thing that are good to know for working on, and setting up this project:
 * [Apache configuration files](https://httpd.apache.org/docs/2.4/configuring.html)
 * [Setting up SSL certificate on your apache web server](https://httpd.apache.org/docs/2.4/ssl/ssl_howto.html)
 * [Docker Compose](https://docs.docker.com/compose/)
 * [GrapeTree (The phyllogenetic tree visualizer)](https://achtman-lab.github.io/GrapeTree/documentation/developer/index.html)
 * [Connecting docker application to pre-existing mongo daemon](https://stackoverflow.com/questions/24319662/from-inside-of-a-docker-container-how-do-i-connect-to-the-localhost-of-the-mach/24326540#24326540)
