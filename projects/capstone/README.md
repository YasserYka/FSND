

# FSND Capstone

Cars desposel system, final project in Udacity Full Stack Web Develpment Nanodegree 

# Motivation

Cars disposal system is used to dispose old cars to be recycled. A person might come and ask to dispose mutiple cars. I developed this project to make use of the knowledge I acquired in the Nnaodegree program, to gain confidence in these skills.  

# Deployment

The app is hosted live on heroku at
https://capstonefsndproject.herokuapp.com


# Getting Started

## Clone repository

To clone the repository, run

```
git clone https://github.com/YasserYka/FSND.git
```

## Python

To install Python, follow instructions to intsall the latest version of python for your platform in [Python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

## Key dependencies

- [Flask] (https://palletsprojects.com/p/flask/) Backend framework

- [SqlAlchemy] (https://www.sqlalchemy.org) Python SQL toolkit and ORM

- [Flask-CORS] (https://flask-cors.readthedocs.io/en/latest/) Handle corss origin requests

and other dependencies 

Dependecies |
--- |
alembic	1.4.2 |
click	7.1.2 |
ecdsa	0.15 |
Flask	1.1.2 |
Flask-Cors	3.0.8 |
Flask-Migrate	2.5.3 |
Flask-Moment	0.10.0 |
Flask-Script	2.0.6 |
Flask-SQLAlchemy	2.4.4 |
future	0.18.2 |
gunicorn	20.0.4 |
itsdangerous	1.1.0 |
Jinja2	2.11.2 |
jose	1.0.0 |
Mako	1.1.3 |
MarkupSafe	1.1.1 |
psycopg2-binary	2.8.5 |
pyasn1	0.4.8 |
pycryptodome	3.3.1 |
python-dateutil	2.8.1 |
python-editor	1.0.4 |
python-jose	3.1.0 |
python-jose-cryptodome	1.3.2 |
rsa	4.6 |
six	1.15.0 |
SQLAlchemy	1.3.18 |
Werkzeug	1.0.1 |

## Pip dependencies

Navigate to starter folder, inside FSND folder run

```
cd /projects/capstone/starter
```

Setup virtual enviroment

```
python -m venv venv && venv/bin/activate
```

Install pip dependencies, run

```
pip3 install -r requirements.txt
```

Local database setup

```
flask db init
flask db migrate -m "Init migration"
flask db upgrade
```

Setup Environment variable, run

```
source setup.sh
```

# Local Testing

To test you local installation, run

```
python3 test_app
```

If all tests pass, your installation is set up correctly

# Run code

To run the application locally, run

```
python app.py
```

Application can be found already running in

https://capstonefsndproject.herokuapp.com

# Roles

To get ACCESS TOKEN for Employee or Helpdesk import capstone.postman_collection.json postman collection into postman and invoke Auth0's Employee/Helpdesk endpoints

## Manager

GET Cars and Persons
POST Cars and Persons
Patch Persons
DELETE Persons

## Helpdesk

GET Cars and Persons
Patch Persons

# API Documentation

GET '/cars'
GET '/persons'
POST '/cars'
POST '/persons'
PATCH '/persons'
DELETE '/persons'

GET '/cars'
- Fetches a list of categories
- Request Arguments: None
- Returns: A list of cars (n which the car object contain car id, color and release) and total of categories
```
{
    "cars": [
        {
            "color": "red",
            "id": 1,
            "release": "2021"
        }
    ],
    "success": true
}
```

GET '/persons'
- Fetches a list of objects of type person
- Returns:  A list of persons of type person (in which the person object contain person id, name, cars and age)
```
{
    "persons": [
        {
            "age": 24,
            "id": 2,
            "name": 2
        }
    ],
    "success": true
}
```

POST '/cars'
- Creats a car
- Request Arguments: color, release
- Returns: objects of type car. 
```
{
    "cars": [
        {
            "color": "rexd",
            "id": 2,
            "release": "2021"
        }
    ],
    "success": true
}
```

POST '/persons'
- Creats a person
- Request Arguments: name, age
- Returns: objects of type person. 
```
{
    "persons": [
        {
            "age": 24,
            "id": 3,
            "name": "Yasser"
        }
    ],
    "success": true
}
```

PATCH '/persons'
- Updates a person
- Request Arguments: name, age
- Returns: objects of type persons. 
```
{
    "persons": [
        {
            "age": 24,
            "id": 3,
            "name": "Yasser"
        }
    ],
    "success": true
}
```

DELETE '/persons'
- Delets a person
- Request Arguments: person id
- Returns: deleted person id.
```
{
    "deleted": 2,
    "success": true
}
```

Error handlers

Unprocessable 422
- Retuned when request can't be processed
- Returns: error code and a message 
```
{
    sucess: False,
    error: 422,
    message: "unprocessable"
}
```

Not found 404
- This error is showen when a resource can't be found
- Returns: error code and a message 
```
{
    sucess: False,
    error: 404,
    message: "Not found"
}
```

auth error 400|403|401
- When issue is related to authentication and access token
- Returns: error code and a message 

400
```
{
    code: 'invalid_claims',
    description: 'Permissions not included in JWT.'
}
{
    code: 'invalid_header',
    description: 'Unable to parse authentication token.'
}
{
    code: 'invalid_header',
    description: 'Unable to find the appropriate key.'
}
```

403
```
{
    code: 'unauthorized',
    description: 'Permission not found.'
}
```

401
```
{
    code: 'invalid_header',
    description: 'Authorization malformed.'
}
{
    code: 'invalid_claims',
    description: 'Incorrect claims. Please, check the audience and issuer.'
}
```

Not found 500
- This error is showen when server faced an error
- Returns: error code, status and a message

500
```
{
    'success': False,
    'error': 500,
    'message': 'Internal server error'
}
```