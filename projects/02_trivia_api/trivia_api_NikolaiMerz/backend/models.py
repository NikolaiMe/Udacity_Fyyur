import os
import random
from sqlalchemy import Column, String, Integer, create_engine, and_
from flask_sqlalchemy import SQLAlchemy
import json

database_name = "trivia"
database_path = "postgresql://{}:{}@{}/{}".format('nikol', 'hallo', 'localhost:5432', database_name)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()
    return db

'''
Question

'''
class Question(db.Model):  
  __tablename__ = 'questions'

  id = Column(Integer, primary_key=True)
  question = Column(String)
  answer = Column(String)
  category = Column(String)
  difficulty = Column(Integer)

  def __init__(self, question, answer, category, difficulty):
    self.question = question
    self.answer = answer
    self.category = category
    self.difficulty = difficulty

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'question': self.question,
      'answer': self.answer,
      'category': self.category,
      'difficulty': self.difficulty
    }
  

  '''
  Method to get one question, which fits to a given category and is not a question, contained in 'last_question'
  '''
  @staticmethod
  def getRandomQuestion(last_questions, category):
    questions = (Question.query
                .filter_by(category = str(category))
                .filter(and_(Question.id != question for question in last_questions))
                .order_by(Question.id).all()
      ) 
    if len(questions)>1:
      random_item = random.randrange(len(questions)-1)
      question = questions[random_item].format()
    elif len(questions)==1:
      question = questions[0].format()
    else:
      question = None
    
    return question


'''
Category

'''
class Category(db.Model):  
  __tablename__ = 'categories'

  id = Column(Integer, primary_key=True)
  type = Column(String)

  def __init__(self, type):
    self.type = type

  def format(self):
    return {
      'id': self.id,
      'type': self.type
    }

  def insert(self):
    db.session.add(self)
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()