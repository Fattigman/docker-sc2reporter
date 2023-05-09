# SarsCov2 Reporter
SarsCov2 reporter is a fullstack web application, which can be hosted locally, that monitors local Sars-Cov 2 outbreaks. It processes the output from the [gms arctic pipeline](https://github.com/genomic-medicine-sweden/gms-artic) and visualizes the data so the user can see and share the spread of different virus classification. The user can annotate samples with metadata, qc, pangolin classification, and more.

## Getting Started
To run the application with dummy data, make sure you have docker-compose installed on your system, and then run the following commands:
```bash
git clone https://github.com/genomic-medicine-sweden/docker-sc2reporter
cd docker-sc2reporter
docker-compose -f docker-compose.demo.yml up
```
Once the application is running, you can access the front-end by navigating to [localhost:3000](http://localhost:3000) and the back-end by navigating to [localhost:8000](http://localhost:8000).

For more information on how to set it up in production, navigate to [setup](docs/setup.md)

# Project structure
## Frontend
The front end is written in React and uses the backends API to fetch information.
For more information: see [Frontend documentation](docs/frontend.md)

To run just the frontend locally:
```bash
cd frontend
yarn install
yarn run start
```
## Backend
The backend is a combination is a combination of [mongodb](https://www.mongodb.com/) and [fastapi](https://fastapi.tiangolo.com/), which allows for self documenting endpoints that follows the [openapi specification](https://en.wikipedia.org/wiki/OpenAPI_Specification#:~:text=In%20July%202017%2C%20the%20OpenAPI%20Initiative%20released%20version,which%20can%20generate%20OAS%20documents%20from%20RAML%20input.).

For more information: see [Backend documentation](docs/backend.md)

To run the API locally:
```bash
cd backend
conda create --name sc2rep --file requirements.txt && conda activate sc2rep # Creates a virtual environment from requirements file and activates it
uvicorn --reload api.main:app # Starts the api application, it will reload the whole application on code changes
```
## Grapetree

A production implementation of [GrapeTree](https://github.com/achtman-lab/GrapeTree), a self hosted phylogenetic tree visualizer that uses [minimum spanning trees](https://en.wikipedia.org/wiki/Minimum_spanning_tree), in this case to show the genetic distance between three or more isolates. It's not identical to the original implementation as the wsgi was changed for safety reasons, to gunicorn. For more information, visit their official github linked previously.