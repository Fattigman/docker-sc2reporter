# Table of Contents <!-- omit in toc -->
- [How to develop](#how-to-develop)
  - [Setting up a local instance](#setting-up-a-local-instance)
    - [1. Setting up MongoDB with test data using Docker](#1-setting-up-mongodb-with-test-data-using-docker)
    - [2. Creating a local virtual environment](#2-creating-a-local-virtual-environment)
    - [3. Starting the application](#3-starting-the-application)
    - [4. Accessing the local instance](#4-accessing-the-local-instance)
    - [5. Repopulating the database with test data](#5-repopulating-the-database-with-test-data)
  - [Simplified Module Import using \_\_init\_\_.py](#simplified-module-import-using-__init__py)
  - [Pydantic Models for Data Validation](#pydantic-models-for-data-validation)
  - [FastAPI Endpoints](#fastapi-endpoints)
    - [Example Endpoint File (`example.py`)](#example-endpoint-file-examplepy)
    - [Main Application File (`main.py`)](#main-application-file-mainpy)
  - [CRUD Operations with CRUDBase](#crud-operations-with-crudbase)
- [Backend structure](#backend-structure)
  - [File structure](#file-structure)
  - [MongoDB](#mongodb)
# How to develop

## Setting up a local instance

To set up a local instance for development, follow these steps:

### 1. Setting up MongoDB with test data using Docker
The simplest solution is to utilize Docker along with the `docker-compose.demo.yml` file. Open your terminal and run the following command:
```
docker-compose -f docker-compose.demo.yml up -d --build
```
This command will set up a MongoDB instance with the required test data.

### 2. Creating a local virtual environment
To create a local virtual environment for the Python application, we recommend using conda. Execute the following commands:
```
conda create --name sc2reporter
conda activate sc2reporter
conda install --yes --file requirements.txt 
```
These commands will create a virtual environment named `sc2reporter`, activate it, and install the necessary dependencies specified in the `requirements.txt` file.

### 3. Starting the application
To start the application, specify an available port on your computer. In your terminal, run the following command:
```
uvicorn --reload api.main:app --port 8080
```
This will start the application using Uvicorn with automatic reloading enabled.

### 4. Accessing the local instance
Open a web browser and navigate to `localhost:8080/docs` to access the local instance of sc2reporter, which includes the preloaded test data. Please note that the application requires authentication for most endpoints. If you make any code changes, the application will recognize them and automatically reload. In such cases, you may need to reauthenticate.

### 5. Repopulating the database with test data
If you need to repopulate the database with test data at any point, simply re-run the following command:
```
docker-compose -f docker-compose.demo.yml up -d --build
```
This command will recreate the Docker container with the test data, ensuring the database is populated accordingly.

## Simplified Module Import using \_\_init__.py

This project utilizes the `__init__.py` file to facilitate the export of modules. By organizing multiple Python scripts within folders, importing specific modules becomes more convenient through a single file. To import modules from the appropriate directory, follow the example below:

```python
# Import modules defined in the __init__.py file within the directory
from path.to.directory import module_1, module_2
```

By employing this approach, you can import multiple modules at once by specifying their names after the `from` statement, simplifying the import process and reducing the need to import each module individually.

## Pydantic Models for Data Validation

In the application powered by fastAPI, one of the notable features is the use of pydantic models for data validation. This approach offers two significant advantages: self-documenting endpoints and rigorous data validation.

All data managed by the API needs to be formatted as pydantic data models. These models define the structure, types, and validation rules for the incoming and outgoing data.

You can find the pydantic models in the `backend/models` folder. If you need to create a new object, you can either add it to one of the existing `.py` files or create a new file if it has unique requirements.

To make the model accessible throughout the application, import it in the `__init__.py` file. By doing so, you ensure that the model is readily available for import and usage in other parts of the application.
## FastAPI Endpoints

The main application logic can be found in `backend/api/main.py`, where the application is defined and initialized. New routes are created using fastAPI's `APIRouter` in specific `endpoint.py` files. These endpoint files are then imported into the `main.py` file, where they are appended to the `app` object.

Here's an example to illustrate the structure and usage of fastAPI endpoints:

### Example Endpoint File (`example.py`)

```python
from fastapi import APIRouter, Depends
from api.models import pydanticModel
from api.dependencies import get_current_active_user

router = APIRouter()

@router.get("/", response_model=pydanticModel)
async def get_dashboard_data(current_user: User = Depends(get_current_active_user)):
    # Perform necessary operations...
    return pydanticModel

@router.post("/", response_model=pydanticModel)
async def post_dashboard_data(current_user: User = Depends(get_current_active_user)):
    # Perform necessary operations...
    return pydanticModel
```

In the above example, the `example.py` file contains two endpoints: `GET /` and `POST /`. These endpoints are defined using the `router` object from `APIRouter` and decorated with appropriate HTTP methods (`@router.get` and `@router.post`). The endpoints have their own request and response models, such as `pydanticModel` in this case.

### Main Application File (`main.py`)

```python
from fastapi import FastAPI
from api.endpoints import example

app = FastAPI()

app.include_router(
    example.router,
    prefix="/example",
    tags=["example"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}},
)
```

In the `main.py` file, the `example` endpoint file is imported, and its router (`example.router`) is included in the `app` using `app.include_router()`. This connects the endpoints defined in `example.py` under the `/example` path.

Both the `GET` and `POST` endpoints defined in `example.py` will be represented in the API. They will be accessible as `/example/` (GET) and `/example/` (POST), respectively. The specified `pydanticModel` will be used for validating the request payload and generating the response.

By organizing endpoints in separate files and utilizing `APIRouter`, the codebase remains modular and easier to maintain, allowing for scalability and reusability of endpoint logic.

## CRUD Operations with CRUDBase

To achieve code reusability and maintainability, a CRUDBase object has been implemented. This object utilizes a Pydantic model, representing objects in MongoDB, as input and generates a new object that can be used to interact with the database. The CRUDBase object provides simple CRUD functions, including Create, Read, Update, and Delete operations.

Here's an example of how to use the CRUDBase object:

```python
from db import *
from .crud_base import CRUDBase
from models import pydanticModel

class CRUDExample(CRUDBase):
    def __init__(self):
        super().__init__(pydanticModel, "pydanticModel")

new_model = CRUDExample()
```

In the code snippet above, a `CRUDExample` class is created by inheriting from the `CRUDBase` class. The `CRUDBase` class takes the `pydanticModel` and a string identifier as input to define the model and the collection name in the MongoDB database, respectively. By creating an instance of `CRUDExample`, you can perform CRUD operations on objects of `pydanticModel`.

However, in some cases, certain functions may require additional specificity, such as applying filters. In such scenarios, you can extend the CRUD object by appending custom functions. Here's an example of how to add a custom function to retrieve specific examples based on a filter:

```python
class CRUDExample(CRUDBase):
    def __init__(self):
        super().__init__(pydanticModel, "pydanticModel")
    
    async def get_specific_example(self, example: str):
        curr = db.sample.find({"really_weird_example_that_only_happens_once.type": example})
        docs = [parse_json(x) for x in await curr.to_list(None)]
        return docs
```

In the above code snippet, a `get_specific_example` function is added to the `CRUDExample` class. This function queries the database using a specific filter condition (`{"really_weird_example_that_only_happens_once.type": example}`) and retrieves the matching documents.

By leveraging the CRUDBase object and extending it with custom functions as needed, you can streamline CRUD operations and ensure code maintainability and scalability.
# Backend structure

## File structure
```tree
📦backend
 ┣ 📂api
 ┃ ┣ 📂endpoints # Contains all the endpoints exposed by the api
 ┃ ┣ 📜config.py # The configurations of the application, can/should be modified to fit your deployment
 ┃ ┗ 📜main.py # The main entrypoint for the application
 ┣ 📂crud # Contains all the crud objects, including the base from which (almost all of) the others are generated
 ┃ ┣ 📜all_crud_objects
 ┣ 📂db # Contains database scripts for startup and database driver
 ┃ ┣ 📜__init__.py
 ┃ ┣ 📜db.py
 ┃ ┗ 📜init_db.py
 ┣ 📂models # Contains all pydantic models used by fastapi and swagger to generate documentation and validate data
 ┃ ┣ 📜all pydantic models
 ┣ 📂tests # Tests for the application (which are yet to be implemented)
 ┃ ┣ 📜all the tests
 ┣ 📜Dockerfile
 ┣ 📜README.md
 ┣ 📜authentication.py # Contains authorization scripts such as hashing+salting passwords
 ┗ 📜requirements.txt
```
## MongoDB

MongoDB serves as the backbone of the application, handling the creation, storage, and updating of data through various methods. The database is composed of several collections, each serving a specific purpose:

1. **Consensus**: Contains the consensus sequence of each isolate. For more information on consensus sequences, refer to [this link](https://en.wikipedia.org/wiki/Consensus_sequence). It includes the following fields:
   - sample_oid: The ObjectID of the sample entry to which the consensus belongs.
   - seq: The consensus sequence of the isolate.
   - qual: The quality of each call in the seq field.
   - sample_id: The common name of the sample represented by the entry.

2. **Depth**: Represents the calls of each position in a sequenced isolate. Different calls are represented by the fields [DEL, A, G, C, T, REFSKIP]. Additional fields include:
   - pos: The position of the calls.
   - sample_id: The common name of the isolate to which the information belongs.
   - sample_oid: The ObjectID of the sample entry to which the depth entry belongs.

3. **Sample**: Contains sample information, including metadata, quality control (QC) data, variants, and more. Common fields found in a Sample entry are:
   - Variants: A list of variants, where each variant contains:
     - aa: The associated amino acid. More details can be found [here](https://www.nature.com/articles/s41598-020-70812-6).
     - dp: The sequencing depth of the mutation.
     - alt_freq: The frequency of the variant, ranging from 0 to 1 (equivalent to 0% to 100%).
   - QC: Quality control data comprising several QC fields.
   - time_added: Timestamp indicating when the entry was inserted into the database.
   - collection_date: Date when the isolate was extracted from the patient.
   - pangolin: Information related to the Pangolin classification, which categorizes viral lineages. More details can be found [here](https://cov-lineages.org/).
   - nextclade: Information related to the Nextclade classification, providing clade assignment for viral sequences. Learn more [here](https://clades.nextstrain.org/).
   - sample_id: The common name or identifier for the sample.
   - age: Age of the patient associated with the sample.
   - lab: Name of the laboratory where the isolate was extracted.
   - selection_criterion: Indicates the circumstances or criteria under which the isolate was extracted.
   - seqfacility: Specifies the facility or location where the sequencing of the isolate took place.
   - Ct: Threshold cycle, a parameter used in real-time PCR analysis. Further information can be found [here](https://www.thermofisher.com/se/en/home/life-science/pcr/real-time-pcr/real-time-pcr-learning-center/real-time-pcr-basics/real-time-pcr-understanding-ct.html).

4. **Variant**: Provides in-depth information about each genetic variant, such as its position and mutation. The fields include:
   - _id: The ObjectID of each entry. This field is set to the position and mutation of the variant (e.g., 204_G>T).
   - csq: An object field that consists of metadata describing the variant.

5. **Significant Variants**: Contains a single entry that defines which variants are considered of heightened importance. It includes the following fields:
   - variants: A list of significant amino acid variants (aa) from the sample's variants field.
   - pango_lineages: A list of significant Pangolin classifications.
   - positions: