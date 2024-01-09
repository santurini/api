## Project structure
The structure involves controllers, models, and handlers. It is a modular and organized approach to buildthe API. Let's break down these components:

1. **Controllers:**
   - **Role:** Controllers handle incoming requests, process user input, interact with models, and manage the flow of data.
   - **Responsibilities:**
     - Receive requests from the user or external systems.
     - Interpret and validate user input.
     - Interact with models to retrieve or update data.
     - Decide which response to send back to the user.

2. **Models:**
   - **Role:** Models represent the data structure of the application.
   - **Responsibilities:**
     - Define the structure of the data (e.g., database tables, object properties).
     - Handle data validation and manipulation.
     - Interact with the database or other data sources.

3. **Handlers:**
   - **Role:** Handlers are components that deal with specific tasks or operations within the application.
   - **Responsibilities:**
     - Execute specific actions or operations in response to events or requests.
     - Coordinate the flow of data between controllers and models.
     - Handle specific tasks that don't fit neatly into the controller or model responsibilities.

**Relationships:**
- **Controller-Model Interaction:**
  - Controllers use models to retrieve or update data.
  - Models provide a structured way to handle and represent data.

- **Controller-Handler Interaction:**
  - Controllers delegate specific tasks to handlers.
  - Handlers execute tasks and report back to controllers.

- **Model-Handler Interaction:**
  - Handlers utilize models to perform specific data-related operations.
 
**Tweaks:**
- **Async Functions:**
   - The controller is built upon asynchronous functions that offer the advantage of improved responsiveness and scalability.
- **Advantages:**
   - Tasks are executed concurrently without waiting for each other to complete, asynchronous programming enables the API to handle multiple requests simultaneously.
   - Prevent delays and ensures efficient utilization of system resources, leading to better performance and responsiveness, especially in scenarios with high concurrency or I/O-bound operations.

In this way, the controllers orchestrates the overall flow, delegates data-related tasks to the models, and involve the handlers for specific actions.
This structure promotes separation of concerns, making the code more modular, maintainable, and easier to understand.

```
├── backend                                       # root folder of the applicative
│   ├── app                                       # folder containing the source code of the applicative 
│   │   ├── controllers                           # controllers folder, functions handling the database operations and HTTP response
│   │   │   ├── __init__.py
│   │   │   └── item_controller.py                # code for router, mongodb setup and database injection and retrieval
│   │   ├── handlers                              # handlers folder, helper functions for ingestion and retrieve API
│   │   │   ├── __init__.py
│   │   │   ├── item_handler.py                   # implementation of ingestion and retrieval function
│   │   │   └── key_handler.py                    # implementation of API authentication via api token
│   │   ├── models                                # models folder, definition of item specifications and constraints
│   │   │   ├── __init__.py
│   │   │   └── item_model.py                     # model definition for items to be ingested
│   │   ├── __init__.py    
│   │   └── main.py                               # main script with app definition and initialization
│   ├── Dockerfile                                # Dockerfile to build the applicative as a docker service exposing port 8000
│   └── requirements.txt                          # pip requirements to be installed via Dockerfile
├── bin                                           # bin folder with scripts to launch and stop docker
│   ├── start.sh                                  # this script starts mongodb and applicative as services via Docker container
│   └── stop.sh                                   # this script stops the services
├── api.json                                      # api specification file
├── docker-compose.yml                            # script to launch the Docker services, called inside ./bin/start.sh
└── README.md                                     # documentation file
```

## Getting started
#### 1. Launch the docker service
```
bash bin/start.sh
```
```
[+] Building 1.8s (11/11) FINISHED                                                                                                                                             docker:desktop-linux
 => [backend internal] load build definition from Dockerfile                                                                                                                                   0.0s
 => => transferring dockerfile: 292B                                                                                                                                                           0.0s
 => [backend internal] load .dockerignore                                                                                                                                                      0.0s
 => => transferring context: 2B                                                                                                                                                                0.0s
 => [backend internal] load metadata for docker.io/library/python:3.10                                                                                                                         1.8s
 => [backend 1/6] FROM docker.io/library/python:3.10@sha256:ba7e6f1feea05621dec8a6525e1bb9edf30a3897bc6fd047d72f860ff0b73706                                                                   0.0s
 => [backend internal] load build context                                                                                                                                                      0.0s
 => => transferring context: 1.36kB                                                                                                                                                            0.0s
 => CACHED [backend 2/6] RUN mkdir -p /backend/app                                                                                                                                             0.0s
 => CACHED [backend 3/6] WORKDIR /backend                                                                                                                                                      0.0s
 => CACHED [backend 4/6] COPY requirements.txt /                                                                                                                                               0.0s
 => CACHED [backend 5/6] RUN pip install --requirement /requirements.txt                                                                                                                       0.0s
 => CACHED [backend 6/6] COPY ./app /backend/app                                                                                                                                               0.0s
 => [backend] exporting to image                                                                                                                                                               0.0s
 => => exporting layers                                                                                                                                                                        0.0s
 => => writing image sha256:3e48b082a5d911680f432a38ea4c8d2975d6c237ecad31d4c6f42e763960e0a1                                                                                                   0.0s
 => => naming to docker.io/library/backend                                                                                                                                                     0.0s
[+] Running 3/3
 ✔ Network api_default      Created                                                                                                                                                   0.0s 
 ✔ Container api-backend-1  Started                                                                                                                                                   0.0s 
 ✔ Container api-mongo-1    Started 
```

#### 2. Connect to API endpoint

The API will be reachable from the Swagger UI at `http://0.0.0.0:8000/docs`. \
To send requests click on the **_Authorize_** button and insert **BigProfiles-API** as value.

<img width="1418" alt="image" src="https://github.com/santurini/api/assets/91251307/5ebbcfd1-5611-44a5-bb6a-ba248ebe5671">

#### 3. Send GET and POST requests

To send an ingestion request (POST) use the following command:
```
curl -X 'POST' 'http://0.0.0.0:8000/api/v1/ingest' \
     -H 'accept: application/json' \
     -H 'x-api-key: BigProfiles-API' \
     -H 'Content-Type: application/json' \
     -d '{
          "key": 1,
          "payload": "stringa esempio"
      }'
```
```
{
  "message": "Access granted!",
  "payload": {
    "key": 1,
    "payload": "stringa esempio",
    "response_time": 29,
    "response_code": 200,
    "time": "2024-01-07 11:56:55.246789",
    "_id": "659a918796286b4669b70f98"
  }
}
```

To send a retrieve request (GET) the date is expected to be in this format: **_YYYY-MM-DD hh:mm:ss_**.
```
curl -X 'GET' 'http://0.0.0.0:8000/api/v1/retrieve?date_from=2023-01-01%2000%3A00%3A00&date_to=2025-01-01%2000%3A00%3A00' \
     -H 'accept: application/json' \
     -H 'x-api-key: BigProfiles-API'
```
```
{
  "message": "Access granted!",
  "statistics": [
    {
      "key": 1,
      "total_response_time_ms": 29,
      "total_requests": 1,
      "total_errors": 0,
      "creation_datetime": "2024-01-07 11:56:00"
    }
  ],
  "logs": [
    {
      "key": 1,
      "payload": "stringa esempio",
      "response_time": 29,
      "response_code": 200,
      "creation_datetime": "2024-01-07 11:56:55.246000"
    }
  ],
  "status_code": 200
}
```
#### 4. Stop the service
```
bash bin/stop.sh
```
```
[+] Running 3/2
 ✔ Container api-backend-1  Removed                                                                                                                                                                                          0.4s 
 ✔ Container api-mongo-1    Removed                                                                                                                                                                                          0.4s 
 ✔ Network api_default      Removed 
```
