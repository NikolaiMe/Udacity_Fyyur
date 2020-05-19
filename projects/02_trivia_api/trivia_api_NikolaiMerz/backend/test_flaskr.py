import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format('nikol', 'hallo', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        
    
    def tearDown(self):
        pass        

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_all_categorys(self):

        
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
       
    def test_404_get_all_categorys(self):
        res = self.client().get('/categorys')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_get_all_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])
        self.assertIsNone(data['current_category'])
    
    def test_404_get_all_questions(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_delete_question(self):
        question_id_to_delete = Question.query.first().id
        res = self.client().delete('/questions/{}'.format(question_id_to_delete))
        data = json.loads(res.data)
        deleted_question = Question.query.get(question_id_to_delete)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], question_id_to_delete)
        self.assertIsNone(deleted_question)

    def test_404_delete_question(self):
        question_id_to_delete = Question.query.order_by(Question.id.desc()).first().id + 1
        res = self.client().delete('/questions/{}'.format(question_id_to_delete))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_create_new_question(self):
        question_to_be_created={
            'question': 'How are you?',
            'answer': 'Fine, Thanks!',
            'difficulty': 1,
            'category': '2'
        }

        res = self.client().post('/questions', json = question_to_be_created)
        data = json.loads(res.data)

        new_question = Question.query.get(data['created'])

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertEqual(new_question.question, question_to_be_created['question'])
        self.assertEqual(new_question.answer, question_to_be_created['answer'])
        self.assertEqual(new_question.difficulty, question_to_be_created['difficulty'])
        self.assertTrue(new_question.category)

    def test_422_create_new_question(self):
        question_to_be_created={
            'question': 'How are you?',
            'answer': 'Fine, Thanks!',
            'difficulty': 1,
        }

        res = self.client().post('/questions', json = question_to_be_created)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_search_question(self):
        search_term = {
            'searchTerm': 'how'
        }

        res = self.client().post('/questions', json = search_term)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertIsNone(data['current_category'])

    def test_404_search_question(self):
        search_term = {
            'searchTerm': 'asdfasdf'
        }

        res = self.client().post('/questions', json = search_term)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_get_questions_by_category(self):
        res = self.client().get('/categories/2/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])
    
    def test_404_questions_by_category(self):
        res = self.client().get('/categories/2000/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_play_quiz(self):
        request_body={
            'previous_questions': [1,2,3],
            'quiz_category': {
                'id' : '3',
                'type': 'Test'
            }
        }

        res = self.client().post('/quizzes', json = request_body)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

    def test_404_play_quiz(self):
        request_body={
            'previous_questions': [],
            'quiz_category': {
                'id' : 100,
                'type': 'Test'
            }
        }

        res = self.client().post('/quizzes', json = request_body)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
    



        

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()