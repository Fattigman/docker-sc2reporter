# SarsCov2 Reporter FastAPI

## TL;DR
To run the back end locally in a conda environment run the following standing in this folder:
```bash
conda create --name sc2rep
conda activate sc2rep
conda install --file requirements.txt
uvicorn api.main:app
```