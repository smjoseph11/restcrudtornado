# widgets-api-service 

A simple RESTful API service using the Tornado framework

___

## Development Environment
### Installing Poetry

this package uses [poetry](https://python-poetry.org/) for dependency management.

Install poetry in the system `site_packages`
    
    > pip install poetry

### Building the Development Environment

1. Clone the repository.
    
    >git clone git@github.com:smjoseph11/restcrudtornado.git
    
    >cd restcrudtornado

2. Install the dependencies

    > poetry install

### Run Unit Tests
    
    > poetry run pytest

### Pre-commit hooks can be installed

    > poetry run pre-commit install

### Running the Service Locally

    > poetry run python -m widgets

    Application runs on localhost:8000 by default
___

### Supported HTTP Method Calls
    

    This application supports CRUDL operations to update a database. 
    These operations are interfaced with through HTTP request methods.

    The following HTTP methods are supported for CRUDL operations on the DB:
    GET(list): ex. GET localhost:8000/widgets
    GET(read): ex. GET localhost:8000/widgets/test_widget
    POST(create): ex. POST localhost:8000/widgets
```json 
   {
    "name":"test_widget",
    "number_of_parts": 1
   }

```

    PUT(update): ex. PUT localhost:8000/widgets/test_widget

```json 
{
    "number_of_parts": 2
}
```

    DELETE(delete): ex. DELETE localhost:8000/widgets/test_widget
