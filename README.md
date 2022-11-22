# SarsCov2 Reporter
SarsCov2 reporter is a fullstack web application, which can be hosted locally, that monitors local Sars-Cov 2 outbreaks. It processes the output from the [gms arctic pipeline](https://github.com/genomic-medicine-sweden/gms-artic) and visualizes the data so the user can see and share the spread of different virus classification. The user can annotate samples with metadata, qc, pangolin classification, and more.

# TL;DR
## To run with dummy data:
Make sure you have docker-compose installed on your system, and then
```bash
git clone https://github.com/genomic-medicine-sweden/docker-sc2reporter
cd docker-sc2reporter
docker-compose -f docker-compose.yaml up
```

Then navigate to localhost:3000 for the front end and localhost:8000 for the back-end