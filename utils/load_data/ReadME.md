# Loading data into the database

## Constructing a docker image
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

Your data should be all in one folder, this will allow the docker image to mount that folder into its own environment.

```
docker run -rm -v <folder-with-all-your-data>:/data/ --network <docker-network-if-you-host-your-mongo-on-docker>  --env-file data.env sc2-data-import

# Explanation of the command
# -v: Mounts your data folder into the docker container
# -rm: removes the docker container when it done running, may be omitted for troubleshooting
# --network: If you run the mongodb as a docker container, you will need to mount the container into it's network. Otherwise you can ommit this whole part
# --env-file: Environment file which defines the input parameters as well as mongo db url
```