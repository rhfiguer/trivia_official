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
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question = {
            'question': 'Question_test 1',
            'answer': 'Answer_test 1',
            'difficulty': 1,
            'category': 1
        }

        self.new_category = {
            'type':2
        }

        self.search_phrase = {
            'search_phrase':'Question'
        }

        self.quiz_category = {
            'category': 'a'
        }


        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    # Test display paginated questions endpoint
    def test_get_paginated_questions(self):
        res = self.client().get('/questions/')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))

    # Test display categories endpoint
    def test_get_categories(self):
        res= self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['categories'])

    # Test delete question endpoint
#   def test_delete_questions(self):
#       res= self.client().delete('/questions/3')
#       data = json.loads(res.data)
#
#       question = Question.query.filter(Question.id == 3).one_or_none()
#
#       self.assertEqual(res.status_code, 200)
#       self.assertEqual(data['success'], True)
#       self.assertEqual(data['deleted'], 3)
#       self.assertTrue(data['questions'])
#       self.assertTrue(data['total_questions'])
#       self.assertTrue(data['categories'])
#       self.assertEqual(question, None) # Question no longer exists

    # Test error handle if deleting non existing question
    def test_422_if_question_does_not_exist(self):
        res = self.client().delete('/questions/100')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable entity error')

    # Test create new question endpoint
    def test_create_new_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])

    # Test error handle if creating is not allowed
    def test_405_if_method_not_allowed(self):
        res = self.client().post('/questions/1000', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Method not allowed')

    # Test search question endpoint
    def test_search(self):
        res = self.client().post('/search', json=self.search_phrase)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertEqual(data['total_questions'])

    # Test error handle if search not found
    def test_404_if_not_found(self):
        res = self.client().post('/search/1', json=self.search_phrase)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found error')
    
    # Test display question by category endpoint
    def test_get_by_category(self):
        res= self.client().get('/categories/2/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])

    # Test error handle if non getting questions by category
    def test_404_if_not_get_by_category(self):
        res = self.client().get('/categories/a/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found error')

    # Test quizzes endpoint
   #def test_get_quiz(self):
   #    res = self.client().post('/quizzes'), json= self.quiz_category)
   #    data = json.loads(res.data)
#
   #    self.assertEqual(res.status_code, 200)
   #    self.assertEqual(data['success'], True)
   #    self.assertTrue(data['question'])

    # Test error handle if quiz not processable
    def test_404_if_quiz_not_processable(self):
        res = self.client().post('/quizzes/15', json=self.quiz_category)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found error')
   
   
    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()