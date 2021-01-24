

# FSND Capstone

Cars parking system, final project in Udacity Full Stack Web Develpment Nanodegree 

# Heroku

Base url is https://capstonefsndproject.herokuapp.com

# Getting Started

To run application locally, within the ./starter directory to install dependencies run

```
pip install -r requirements.txt
```

Then to run application, run

```
python app.py
```

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