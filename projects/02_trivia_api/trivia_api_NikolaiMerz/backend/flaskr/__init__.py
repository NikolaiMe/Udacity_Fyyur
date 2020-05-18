import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

''' 

paginate_questions Method takes a set of x-questions and returns a list, containing 10 questions. 
Which questions are returned is decided by the page parameter contained in the request.

'''

def paginate_questions(request, selection):
  page = request.args.get('page', 1, type=int)
  start =  (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE

  questions = [question.format() for question in selection]
  current_questions = questions[start:end]

  return current_questions

'''
Creating the flask app

'''

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  db = setup_db(app)
  CORS(app, resources={r"*": {"origins": '*'}})
  
  '''
  Definition of the CORS response Header
  
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
    return response


  '''
  ENDPOINTS
  '''

  '''
  Endpoint to get all question-categories

  '''
  @app.route('/categories', methods=['GET'])
  def getAllCategories():
    selection = Category.query.all()
    categories = {category.id:category.type for category in selection}

    if len(categories) == 0:
      abort(404)

    return jsonify({
      'success': True,
      'categories': categories
    })

  '''
  Endpoint to get all questions paginated
  
  '''
  @app.route('/questions', methods=['GET'])
  def getAllQuestionsPaginated():
    
    abort_code = None

    try:
      selection = Question.query.order_by(Question.id).all()
      total_questions = len(selection)
      current_questions = paginate_questions(request, selection)
      selection_cat = Category.query.order_by(Category.id).all()
      categories = {category.id:category.type for category in selection_cat}


      if len(current_questions) == 0:
        abort_code = 404

      if abort_code is None:
        return jsonify({
          'success': True,
          'questions': current_questions,
          'total_questions': total_questions,
          'categories': categories,
          'current_category': None
        })
    except:
      db.session.rollback()
      abort_code = 422
    finally:
      db.session.close

    if abort_code:
      abort(abort_code)

  '''
  Endpoint to delete a question based on the given question ID
  
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def deleteQuestion(question_id):
    
    abort_code = None

    try:
      question_to_delete = Question.query.filter(Question.id == question_id).one_or_none()
      
      if question_to_delete is None:
        abort_code = 404

      if abort_code is None:
        question_to_delete.delete()
        return jsonify({
          'success': True,
          'deleted': question_id,
        })
    except:
      db.session.rollback()
      abort_code = 422
    finally:
      db.session.close

    if abort_code:
      abort(abort_code)

  '''
  Endpoint to create a new question, or to search for a specific question. 
  To distinguish between a creation of a new question and a search, the endpoint
  looks for the attribute 'searchTerm' inside the body of the POST request. If there
  is a 'searchTerm' attribute it performs a search if not it tries to create a new
  question with the given data.
  
  '''
  @app.route('/questions', methods=['POST'])
  def createNewQuestion():
    abort_code = None

    new_question = None
    new_answer = None
    new_difficulty = None
    new_category = None
    search = None

    body = request.get_json()


    if body is not None:
      new_question = body.get('question', None)
      new_answer = body.get('answer', None)
      new_difficulty = body.get('difficulty', None)
      new_category = body.get('category', None)
      search = body.get('searchTerm', None)

    if search is None:
      try:
        if new_question is None or new_answer is None or new_difficulty is None or new_category is None:
          abort_code = 422

        if abort_code is None:
          question_to_insert = Question(question = new_question, answer = new_answer, category = new_category, difficulty = new_difficulty)
          question_to_insert.insert()
          return jsonify({
            'success': True,
            'created': question_to_insert.id,
          })
      except:
        db.session.rollback()
        abort_code = 422
      finally:
        db.session.close

      if abort_code:
        abort(abort_code)
    else:
      try:
        search_result = Question.query.filter(Question.question.ilike('%{}%'.format(search))).order_by(Question.id).all()

        if len(search_result) == 0:
          abort_code = 404

        if abort_code is None:
          current_search_result = paginate_questions(request, search_result)

          if current_search_result is None:
            abort_code = 404

        if abort_code is None:
          return jsonify({
            'success': True,
            'questions': current_search_result,
            'total_questions': len(search_result),
            'current_category': None
          })

      except:
        db.session.rollback()
        abort_code = 422
      finally:
        db.session.close

      if abort_code:
        abort(abort_code)

  '''
  Endpoint to get all questions from a given category

  ''' 
  @app.route('/categories/<int:cat_id>/questions')
  def getQuestionsByCategory(cat_id):
    abort_code = None

    try:
      selection = Question.query.filter_by(category = str(cat_id)).order_by(Question.id).all()
      current_category = Category.query.get(int(cat_id))
      total_questions = len(selection)
      current_questions = paginate_questions(request, selection)

      if len(current_questions) == 0:
        abort_code = 404

      if abort_code is None:
        return jsonify({
          'success': True,
          'questions': current_questions,
          'total_questions': total_questions,
          'current_category': current_category.type
        })
    except:
      db.session.rollback()
      abort_code = 422
    finally:
      db.session.close

    if abort_code:
      abort(abort_code)

  '''
  This endpoint takes category and previous question parameters 
  and returns a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  '''
  @app.route('/quizzes', methods = ['POST'])
  def getNextQuestion():
    abort_code = None
    try:
      body = request.get_json()
      last_questions = body.get('previous_questions', None)
      quiz_category = body.get('quiz_category', None)
      category = Category.query.get(quiz_category['id'])
      if category is None:
        abort_code = 404
      question = Question.getRandomQuestion(last_questions, quiz_category['id'])
      if abort_code is None:
        return jsonify({
                'success': True,
                'question': question
              })
    except:
      abort_code = 422
    finally:
      db.session.close

    if abort_code:
      abort(abort_code)

  '''
  ERROR HANDLER
  '''

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
  
  return app

    