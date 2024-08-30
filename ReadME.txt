# Yahoo Finance Extractor API
Overview

The Yahoo Finance Extractor API is a FastAPI application that provides endpoints to interact with Yahoo Finance data. This application is containerized using Docker and includes automated tests to ensure its functionality.
Requirements

    Python 3
    Docker and Docker Compose for containerization
    FastAPI and SQLAlchemy for the web framework and database interaction
    pytest for automated testing

Features

    REST API Endpoints:
        /api/instrument/{symbol}: Fetch details for a specific financial instrument.
        /api/portfolio: Retrieve the user's portfolio, optionally filtered by symbol.
        /api/purchase_instrument: Purchase a specific number of shares for an instrument.
        /api/sell_instrument: Sell a specific number of shares for an instrument.
        /api/transactions: Retrieve all transactions or filter by symbol.

    Logging and Tracing:
        Configured to use OpenTelemetry for tracing and logging requests.

    Configuration:
        API keys and other settings are configurable via environment variables and a .env file.

    Automated Testing:
        Includes automated tests for endpoints using pytest.

Setup and Launch
1. Clone the Repository

bash
$ git clone <repository_url>
$ cd <repository_directory>

2. Create a .env File

Create a .env file in the root of the project directory with the following content:

env
API_KEY=your_yahoo_finance_api_key

Replace your_yahoo_finance_api_key with your actual Yahoo Finance API key.
3. Build and Run the Docker Containers

Ensure Docker and Docker Compose are installed on your system. Then, build and start the Docker containers using the following commands:

bash
$ docker compose up --build

This command will:

    Build the Docker images for the application.
    Start the containers and set up the necessary services.

These will generate 2 images, one for the web application and another for the testing:

$ docker images

4. Access the API

Once the containers are running, you can access the API at:

http://localhost:8000

5. View Logs

To view the logs of the running containers, use the following command:

bash
$ sudo docker logs <container_id_web>

To check the active containers:

bash
$ docker ps

To stop the container:

bash
docker stop <container_id_web>

To remove the container:

bash
$ docker rm <container_id_web>

To remove the images:

bash
$ docker rmi <image_id_web> && <image_id_test>


6. Run Automated Tests

The docker compose automatically perfoms the tests when it is run.
To manually run the automated tests, execute the following command:

bash
$ pytest -v

Ensure that the Docker containers are running before executing the tests, as they depend on the application being available.
Configuration

The application uses a .env file for configuration. This can modifed to update settings such as the API key. Other configuration options are handled via environment variables and the Docker Compose file.
Error Handling

The API includes standard error handling for various scenarios, such as invalid input or issues with fetching data from Yahoo Finance. Errors are returned with appropriate HTTP status codes and messages.

7. Database

The app will automatically generate a database "api.db" that will contain 3 tables:
 - Transactions
 - Portfolio
 - Logs - contains the logs of all requests on the API.
 
The automated testing also generates an equivalent database inside Tests for testing purposes.
