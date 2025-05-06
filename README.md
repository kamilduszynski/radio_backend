# RestHits API

This is a Django-based API that allows you to manage a collection of music hits, including functionality to list, create, update, and delete hits. It uses Django REST Framework to expose API endpoints for interacting with the data.

## Features

- List the latest hits sorted by creation date
- Create new hits and associate them with artists
- Update existing hits
- Delete hits from the database
- Validate and generate `title_url` automatically
- API endpoint for fetching hit details by `title_url`

## Requirements

- Docker (recommended)
- Docker Compose (recommended)
- Python 3.8 or later (if running locally without Docker)
- PostgreSQL (configured in Docker)

## Setup

1. Build the Docker image

    ```docker compose build```

2. Create `.env` file based on `.env_template`
3. Start the Docker containers (including the Django app and PostgreSQL database):

    ```docker compose up```

    This will start both the Django development server and the PostgreSQL database in Docker. You can access the API at http://localhost:8000/

4. Create initial data (optional):

    ```docker compose exec web python manage.py create_initial_data```

5. Stopping the containers - if you want to shut down application

    To stop the Docker containers, use the following command:

    ```docker compose down```

## Running the tests in Docker

To run tests inside the Docker container, you can use the following command:

    docker compose exec web pytest

This will execute all the tests inside the Docker container. To run a specific test file or function:

    docker compose exec web pytest RestHits/tests/test_models.py
    
    docker compose exec web pytest RestHits/tests/test_models.py::test_hit_creation

### Run with coverage:

    docker compose exec web coverage run -m pytest

Show coverage report in terminal:
 
     docker compose exec web coverage report

## API Endpoints - cURL Requests

1. **GET /api/v1/hits** - List all hits
    
    This endpoint retrieves a list of the latest 20 hits, sorted by the creation date.

    ```bash
    curl -X GET http://localhost:8000/api/v1/hits

2. **GET /api/v1/hits/{title_url}** - Get a specific hit

    This endpoint retrieves the details of a hit by its `title_url`.

    ```bash
    curl -X GET http://localhost:8000/api/v1/hits/everlong
    ```

    Replace everlong with the title_url of the hit you want to get details of.

3. **POST /api/v1/hits** - Create a new hit

    This endpoint allows you to create a new hit. You must include the `artist_id` and `title`.

    ```bash
    curl -X POST http://localhost:8000/api/v1/hits \
     -H "Content-Type: application/json" \
     -d '{"artist_id": 1, "title": "Everlong"}'
    ```

4. **PUT /api/v1/hits/{title_url}** - Update a hit

    This endpoint updates an existing hit. You can change the title, artist_id, and title_url.

    ```bash
    curl -X PUT http://localhost:8000/api/v1/hits/everlong \
     -H "Content-Type: application/json" \
     -d '{"title": "Updated Hit", "artist_id": 2}'
    ```

    Replace everlong with the title_url of the hit you want to update.

5. **DELETE /api/v1/hits/{title_url}** - Delete a hit

    This endpoint deletes a specific hit based on the title_url.

    ```bash
    curl -X DELETE http://localhost:8000/api/v1/hits/everlong
    ```

    Replace everlong with the title_url of the hit you want to delete.

## 3. Development Tools

### Pre-commit Hooks

In this project pre-commit is used to automatically run tools like black, pycln, and isort before every commit to ensure that the code remains consistent and properly formatted.

### Setting up pre-commit hooks

1. Install dependencies:

    ```pip install -r requirements-dev.txt```


2. Install the pre-commit hooks:

    ```pre-commit install```

    This command installs the necessary Git hooks that will automatically run checks when you make a commit.

3. The following hooks will run automatically on each commit:

    **Black**: Automatically formats code using Black with settings defined in pyproject.toml.

    **PyCln**: Cleans up unused imports with PyCln, using settings in pyproject.toml.

    **Isort**: Automatically sorts imports with Isort, using settings from .isort.cfg.

