# docker-sc2reporter v2
Dockerized version of the sc2reporter program. But version 2.

## To run:
First you will need to set up the database (assuming you the test data folder).
These instructions were hastily thrown together, make sure that PATH is correctly set up.
```
docker run --name mongodb -d mongo
conda create --name sc2rep
conda activate sc2rep
conda install perl
cpanm MongoDB
cp /path/to/testdata/vcf2.pm /path/to/perllibs
bash /path/to/testdata/load_data.sh
```

Then run the following commands:
```bash

git clone https://github.com/genomic-medicine-sweden/docker-sc2reporter/
cd docker-sc2reporter
git checkout fastapi
conda install --file requirements.txt
uvicorn main:app --reload
```
