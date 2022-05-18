# docker-sc2reporter v2
Dockerized version of the sc2reporter program. But version 2.

## To run:
First you will need to set up the database, which is not described here.
Then run the following commands:
```bash
conda create --name sc2rep
conda activate sc2rep
git clone https://github.com/genomic-medicine-sweden/docker-sc2reporter/
cd docker-sc2reporter
git checkout fastapi
conda install --file requirements.txt
uvicorn main:app --reload
```
