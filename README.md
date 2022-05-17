# docker-sc2reporter v2
Dockerized version of the sc2reporter program. But version 2.

## To run:
```bash
conda create --name sc2rep
conda activate sc2rep
conda install --file requirements.txt
uvicorn main:app --reload
```
