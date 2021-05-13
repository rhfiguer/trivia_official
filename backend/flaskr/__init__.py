import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

# TODO (1/10): Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  #CORS(app)
  #CORS(app, resources={"r*/api/*": {"origins": "*"}})
  cors = CORS(app, resources={r"*": {"origins": "*"}})
 
# TODO (2/10): Use the after_request decorator to set Access-Control-Allow

  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
    return response
  

  # TODO (3/10): Create an endpoint to handle GET requests for all available categories.
  @app.route('/categories')
  def get_categories():
    # No pagination
    categories = Category.query.all()
    disc_categories = {category.id: category.type for category in categories} # Changed method. Source here: https://knowledge.udacity.com/questions/503892
   
    
    return jsonify({
      'success': True,
      'categories': disc_categories,
      'current_category': None
    })


  #TODO (4/10): Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). 
                #This endpoint should return a list of questions, 
                #number of total questions, current category, categories. 

  #TEST: At this point, when you start the application you should see questions and categories generated,
  #ten questions per page and pagination at the bottom of the screen for three pages.
  #Clicking on the page numbers should update the questions. 
  

  @app.route('/questions/', methods=['GET'])
  def get_questions():
    #pagination
    page = request.args.get('page', 1, type=int)
    start = (page-1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    
    categories = Category.query.all()
    disc_categories = {category.id:category.type for category in categories}
   
    questions = Question.query.all()
    formatted_questions = [question.format() for question in    questions]
    return jsonify({
        'success': True,
        'questions': formatted_questions[start:end],
        'total_questions': len(formatted_questions),
        'categories': disc_categories,
        'current_category': None
    })



  #TODO (5/10): Create an endpoint to DELETE question using a question ID. 
      #TEST: When you click the trash icon next to a question, the question will be removed.
        #This removal will persist in the database and when you refresh the page. 
  @app.route('/questions/<int:id>', methods=['DELETE'])
  def delete_question(id):
    try:
      question = Question.query.filter_by(id=id).one_or_none()
      
      # Handle error 404
      if question is None:
        abort(404)
      question.delete()

      # Paginate
      page = request.args.get('page', 1, type=int)
      start = (page-1) * QUESTIONS_PER_PAGE
      end = start + QUESTIONS_PER_PAGE
      
      # Display categories
      categories = Category.query.all()
      disc_categories = {category.id:category.type for category in categories}
      
      # Display questions
      questions = Question.query.all()
      formatted_questions = [question.format() for question in    questions]
      
      # Return jsonify to frontend
      return jsonify({
          'success': True,
          'deleted': id,
          'questions': formatted_questions[start:end],
          'total_questions': len(formatted_questions),
          'categories': disc_categories,
          'current_category': None
      })
    #Handle error 422
    except:
      abort(422)

  #TODO (6/10): Create an endpoint to POST a new question, 
  #which will require the question and answer text, category, and difficulty score.

  #TEST: When you submit a question on the "Add" tab, 
  #the form will clear and the question will appear at the end of the last page
  #of the questions list in the "List" tab.  
  
  # Set decorator
  @app.route('/questions', methods=['POST'])
  def add_question():
    try:
      data=request.get_json()
      new_question   = data.get('question', None)
      new_answer     = data.get('answer', None)
      new_difficulty = data.get('difficulty', None)
      new_category   = data.get('category', None)

      # Paginate
      page = request.args.get('page', 1, type=int)
      start = (page-1) * QUESTIONS_PER_PAGE
      end = start + QUESTIONS_PER_PAGE
      
      # Display categories
      categories = Category.query.all()
      disc_categories = {category.id:category.type for category in categories}
      
      
      question = Question(question=new_question, answer=new_answer,difficulty=new_difficulty, category=new_category)
      question.insert()
      
      # Display questions
      
      questions=Question.query.order_by(Question.id.desc()).all()
      formatted_questions = [question.format() for question in questions]
      
      # Return jsonify to frontend
      return jsonify({
        'success': True,
        'questions': formatted_questions[start:end],
        'total_questions': len(formatted_questions),
        'categories': disc_categories,
        'current_category': None
      })
    #Handle error 422
    except:
      abort(422)

# TODO(7/10): 
# Create a POST endpoint to get questions based on a search term. 
# It should return any questions for whom the search term 
# is a substring of the question. 

# TEST: Search by any phrase. The questions list will update to include 
# only question that include that string within their question. 
# Try using the word "title" to start. 

  @app.route('/search', methods=['POST'])
  def submit_search():
    try:
      # Search by phrase. 
      # Source to this solution: https://www.youtube.com/watch?v=2pbbUMmsWL0&ab_channel=Cairocoders
      phrase = request.get_json() # Requesting the searchTerm
      search_phrase = phrase.get('searchTerm', None) # Get searchTerm     
      search_list = Question.query.filter(Question.question.ilike('%{}%'.format(search_phrase))).all() # Do the search within the Model
    
      # Display listed questions
      searched_questions = [question.format() for question in search_list]
      
      # Paginate
      page = request.args.get('page', 1, type=int)
      start = (page-1) * QUESTIONS_PER_PAGE
      end = start + QUESTIONS_PER_PAGE

      # Return jsonify to frontend
      return jsonify({
        'success': True,
        'questions': searched_questions[start:end],
        'total_questions':len(searched_questions),
        #'categories':disc_categories,
        'current_category':None
      })
    
    #Handle error 422
    except:
        abort(422)

# TODO (8/10): 
# Create a GET endpoint to get questions based on category. 
#
# TEST: In the "List" tab / main screen, clicking on one of the 
# categories in the left column will cause only questions of that 
# category to be shown.     

      

  @app.route('/categories/<int:category_id>/questions', methods=['GET'])
  def get_by_category(category_id):
 
    try:
      
      questions_by= Question.query.filter(Question.category== str(category_id)).all()
      formatted_questions = [question.format() for question in questions_by]
      
      # Paginate
      page = request.args.get('page', 1, type=int)
      start = (page-1) * QUESTIONS_PER_PAGE
      end = start + QUESTIONS_PER_PAGE

      return jsonify({
      'success': True,
      'questions':formatted_questions[start:end],
      'total_questions':len(formatted_questions),
      'current_category': None
      })
    #Handle error 422
    except:
        abort(422)

#TODO (9/10): 
# Create a POST endpoint to get questions to play the quiz. 
# This endpoint should take category and previous question parameters 
# and return a random questions within the given category, 
# if provided, and that is not one of the previous questions. 
#
# TEST: In the "Play" tab, after a user selects "All" or a category,
# one question at a time is displayed, the user is allowed to answer
# and shown whether they were correct or not. 

  @app.route('/quizzes', methods=['POST'])
  def get_next_question():
    try:
      data = request.get_json()
      quiz_category = data.get('quiz_category', None).get('id')
      previousQuestions="hola"
      #quiz_category = 4 #=> Tengo que asignar data del click
      questions = Question.query.filter(Question.category==quiz_category).all()
      formatted_question=[question.format() for question in questions]
      last_question = len(formatted_question)
      number= random.randint(0, (last_question + 1))

      return jsonify({
        'success': True,
        #'previousQuestions':previousQuestions,
        'question':formatted_question[number],
        #'quiz_category': quiz_category
      })
    except:
      abort(422)

  return app














# '''
# '''
#
# '''
# @TODO: 
# Create error handlers for all expected errors 
# including 404 and 422. 
# '''
# 
  

    