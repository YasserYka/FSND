import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import Car, Person, setup_db
from auth.auth import AuthError, requires_auth

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    CORS(app)
    setup_db(app)

    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type, Authorization"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET, PATCH, POST, DELETE, OPTIONS"
        )
        return response

    @app.route('/persons', methods=['GET'])
    @requires_auth('get:persons')
    def get_persons(token):

        persons = Person.query.all()

        if len(persons) == 0:
            abort(404)

        return {'persons': [person.json() for person in persons], 'success': True}

    @app.route('/cars', methods=['GET'])
    @requires_auth('get:cars')
    def get_cars(token):

        cars = Car.query.all()

        if len(cars) == 0:
            abort(404)

        return {'cars': [car.json() for car in cars],
                'success': True}

    @app.route('/cars', methods=['POST'])
    @requires_auth('post:cars')
    def create_car(token):

        body = request.get_json()

        (color, release, person_name) = (body.get('color'), body.get('release'), body.get('person_name'))

        person = Person.query.filter(Person.name == person_name).one_or_none()

        if color is None or release is None or person is None:
            abort(422)

        car = Car(release=release, color=color)
        
        person.cars.append(car)

        person.update()

        return {'cars': [car.json()], 'success': True}


    @app.route('/persons', methods=['POST'])
    @requires_auth('post:persons')
    def create_person(token):

        body = request.get_json()

        (name, age) = (body.get('name'), body.get('age'))

        if name is None or age is None:
            abort(422)

        person = Person(name=name, age=age)
        person.insert()

        return {'persons': [person.json()], 'success': True}

    @app.route('/persons/<int:id>', methods=['DELETE'])
    @requires_auth('delete:persons')
    def delete_person(token, id):

        person = Person.query.filter(Person.id == id).one_or_none()

        if person is None:
            abort(404)

        person.delete()

        return jsonify({'success': True, 'deleted': id})

    @app.route('/persons/<int:id>', methods=['PATCH'])
    @requires_auth('patch:persons')
    def update_person(token, id):

        person = Person.query.filter(Person.id == id).one_or_none()

        if person is None:
            abort(404)

        body = request.get_json()

        (name, age) = (body.get('name'), body.get('age'))

        if name is not None:
            person.name = name

        if age is not None:
            person.age = age

        person.update()

        return {'persons': [person.json()], 'success': True}

    @app.errorhandler(422)
    def unprocessable(error):
        return (jsonify({'success': False, 'error': 422,
                'message': 'unprocessable'}), 422)

    @app.errorhandler(404)
    def not_found(error):
        return (jsonify({'success': False, 'error': 404,
                'message': 'Resource not found'}), 404)

    @app.errorhandler(AuthError)
    def handle_auth_error(ex):
        response = jsonify(ex.error)
        response.status_code = ex.status_code
        return response
    
    return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)