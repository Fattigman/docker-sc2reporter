# Loading data into the database

- [Loading data into the database](#loading-data-into-the-database)
  - [Constructing a docker image](#constructing-a-docker-image)
  - [Configure environment variables](#configure-environment-variables)
  - [Load the data using the docker image.](#load-the-data-using-the-docker-image)
  - [Data requirements for input files](#data-requirements-for-input-files)
    - [LOAD_DATA_RESULTS](#load_data_results)
    - [LOAD_DATA_META](#load_data_meta)
    - [LOAD_DATA_QPCR](#load_data_qpcr)
    - [MONGO_HOST](#mongo_host)
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

## Data requirements for input files

### LOAD_DATA_RESULTS
Output from the [GMS-Arctic pipeline](https://github.com/genomic-medicine-sweden/gms-artic).
Will consist of: 
 - Fastq files
 - Consensus files
 - Pangolin classifications
 - Nextclade classification
 - Auspice information

For more information, visit arctic [github](https://github.com/genomic-medicine-sweden/gms-artic).

### LOAD_DATA_META

The metadata file should be a csv formatted file, with a column called "Labbnummer".
The "Labbnummer" column will be linked to the sample_id field in the database and ensures that data is associated with the right sample.
Here is an example of how one of this files might look:

| Provtagningsdatum | Labbnummer | Beställare | Postadress | Kön    | Ålder | Analys        | Sample.Laboratorium | Urval            | Ska rapporteras till FoHM |
|-------------------|------------|------------|------------|--------|-------|---------------|---------------------|------------------|---------------------------|
| 2021-03-03        | sc2-1001   | SKÅNE      | MALMÖ      | KVINNA | 23    | SARS-COV2 NGS | MLU                 | Vaccingenombrott | Ja                        |
| ##########        | sc2-1002   | SKÅNE      | MALMÖ      | KVINNA | 32    | SARS-COV2 NGS | MLU                 | Övrig            | Nej                       |
| ##########        | sc2-1003   | SKÅNE      | MALMÖ      | KVINNA | 36    | SARS-COV2 NGS | MLU                 | Vaccingenombrott | Ja                        |
| ##########        | sc2-1004   | SKÅNE      | MALMÖ      | KVINNA | 48    | SARS-COV2 NGS | MLU                 | Vaccingenombrott | Ja                        |

### LOAD_DATA_QPCR

The LOAD_DATA_QPCR generated from [quantstudio command line tool](https://tools.thermofisher.com/content/sfs/manuals/MAN0010409_QuantStudio_CLA_UG.pdf).
It requires the input from the **Presence/Absence** experiment.


### MONGO_HOST

The [connection url](https://www.mongodb.com/docs/manual/reference/connection-string/) for the mongodb which you use as database, whether hosted locally or not.
```mongo
mongodb://[username:password@]host1[:port1][,...hostN[:portN]][/[defaultauthdb][?options]]
```
