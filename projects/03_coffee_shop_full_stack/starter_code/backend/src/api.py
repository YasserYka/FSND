#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

db_drop_and_create_all()


## ROUTES

@app.route('/drinks', methods=['GET'])
def get_drinks():

    drinks = Drink.query.all()

    if len(drinks) == 0:
        abort(404)

    return {'drinks': [drink.short() for drink in drinks],
            'success': True}


@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drinks_detauls(jwt):

    drinks = Drink.query.all()

    if len(drinks) == 0:
        abort(404)

    return {'drinks': [drink.long() for drink in drinks],
            'success': True}


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drink(token):

    body = request.get_json()

    (title, recipe) = (body.get('title'), body.get('recipe'))

    if title is None or recipe is None:
        abort(422)

    drink = Drink(recipe=json.dumps(([recipe] if type(recipe)
                  == dict else recipe)), title=title)
    drink.insert()

    return {'drinks': [drink.long()], 'success': True}


@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(token, id):

    drink = Drink.query.filter(Drink.id == id).one_or_none()

    if drink is None:
        abort(404)

    body = request.get_json()

    (title, recipe) = (body.get('title'), body.get('recipe'))

    if title is not None:
        drink.title = title

    if recipe is not None:
        drink.recipe = recipe

    drink.update()

    return {'drinks': [drink.long()], 'success': True}


@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(token, id):

    drink = Drink.query.filter(Drink.id == id).one_or_none()

    if drink is None:
        abort(404)

    drink.delete()

    return jsonify({'success': True, 'deleted': id})


## Error Handling

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
