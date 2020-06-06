import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
db = setup_db(app)
CORS(app)

db_drop_and_create_all()

## HELPER FUNCTIONS

def checkRecipeWellformed(recipe):
    success = True
    try:
        for ingredient in recipe:
            if 'color' not in ingredient:
                success = False
            if 'name' not in ingredient:
                success = False
            if 'parts' not in ingredient:
                success = False
        return success
    except BaseException:
        return False



## ROUTES
'''
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''

@app.route('/drinks', methods=['GET'])
def getDrinks():
    abort_code = None
    try:
        drinks = Drink.query.all()
        short_drinks = [drink.short() for drink in drinks]

        return jsonify({
                'success': True,
                'drinks': short_drinks
            })
    except BaseException:
        db.session.rollback()
        abort_code = 422
    finally:
        db.session.close

    if abort_code:
        abort(abort_code)

'''
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def getDrinksDetails(token):
    abort_code = None
    try:
        drinks = Drink.query.all()
        long_drinks = [drink.long() for drink in drinks]

        return jsonify({
                'success': True,
                'drinks': long_drinks
            })
    except BaseException:
        db.session.rollback()
        abort_code = 422
    finally:
        db.session.close

    if abort_code:
        abort(abort_code)


'''
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def createNewDrink(token):
    abort_code = None

    title = None
    recipe = None

    body = request.get_json()

    if body is not None:
        title = body.get('title', None)
        recipe = body.get('recipe', None)
    
    if (title is None
            or recipe is None):
        abort_code = 422

    if(checkRecipeWellformed(recipe) == False):
        abort_code = 400

    try:
        if abort_code is None:
            drink_to_insert = Drink(title=title, recipe=json.dumps(recipe))
            drink_to_insert.insert()
            return jsonify({
                'success': True,
                'drinks': [drink_to_insert.long()]
            })
    except BaseException as exception:
        db.session.rollback()
        abort_code = 422
        print(exception)
    finally:
        db.session.close

    if abort_code:
        abort(abort_code)

'''
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def patchDrink(token, drink_id):
    abort_code = None

    title = None
    recipe = None

    body = request.get_json()

    if body is not None:
        title = body.get('title', None)
        recipe = body.get('recipe', None)
    
    if (title is None
            and recipe is None):
        abort_code = 422

    if(recipe is not None):
        if(checkRecipeWellformed(recipe) == False):
            abort_code = 400
    
    try:
        drink = Drink.query.filter(Drink.id == drink_id).one_or_none()

        if drink is None:
            abort_code = 404

        if abort_code is None:
            if title is not None:
                drink.title = title
            if recipe is not None:
                drink.recipe = json.dumps(recipe)
            drink.update()
            return jsonify({
                'success': True,
                'drinks': [drink.long()]
            })

    except BaseException as exception:
        db.session.rollback()
        abort_code = 422
        print(exception)
    finally:
        db.session.close

    if abort_code:
        abort(abort_code)


'''
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def deleteDrink(token, drink_id):

    abort_code = None

    try:
        drink = Drink.query.filter(Drink.id == drink_id).one_or_none()

        if drink is None:
            abort_code = 404

        if abort_code is None:
            drink.delete()
            return jsonify({
                'success': True,
                'delete': drink_id
            })

    except BaseException as exception:
        db.session.rollback()
        abort_code = 422
        print(exception)
    finally:
        db.session.close

    if abort_code:
        abort(abort_code)


## Error Handling

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422

@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "bad request"
    }), 400


@app.errorhandler(AuthError)
def auth_error(e):
    return jsonify({
        "success": False,
        "error": e.status_code,
        "message": e.error
    }), e.status_code
