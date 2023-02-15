# SarsCov2 Reporter
SarsCov2 reporter is a fullstack web application, which can be hosted locally, that monitors local Sars-Cov 2 outbreaks. It processes the output from the [gms arctic pipeline](https://github.com/genomic-medicine-sweden/gms-artic) and visualizes the data so the user can see and share the spread of different virus classification. The user can annotate samples with metadata, qc, pangolin classification, and more.

## Getting Started
To run the application with dummy data, make sure you have docker-compose installed on your system, and then run the following commands:
```bash
git clone https://github.com/genomic-medicine-sweden/docker-sc2reporter
cd docker-sc2reporter
docker-compose -f docker-compose.demo.yml up
```
Once the application is running, you can access the front-end by navigating to \`localhost:3000\`, and the back-end by navigating to \`localhost:8000\`.
## Prefix URL Configuration
The prefix URL in this project is controlled by the environment variable \`REACT_APP_PREFIX_URL\`. By default, it is set to \`/\` to prevent any potential interference with Firebase hosting actions. When the project is run in production, the \`REACT_APP_PREFIX_URL\` variable can be configured with a different value as needed.

