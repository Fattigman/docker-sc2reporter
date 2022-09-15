# Loading data into the database
Start by creating a docker container which will contain all the scripts necessary to load the data into the database. We will later configure the data.env file such that right files and right mongo daemon is located.

```
docker build -t sc2-data-import .
```
## Configure environment variables

Then we need to configure the data.env file. 
LOAD_DATA_RESULTS: The output files from the arctic pipeline
LOAD_DATA_META: meta data from the arctic pipeline
LOAD_DATA_QPCR: quantstudio output file contain Ct scores.
MONGO_HOST: the mongodb host url to load the data into.

## Load the data using the docker image.

```
docker run -v <folder with all your data>:/data/ --network <docker network if you host your mongo on docker>  --env-file data.env sc2-data-import
```