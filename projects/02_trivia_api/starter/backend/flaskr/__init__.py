import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import not_
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
  @DONE: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  """
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    """
  @DONE: Use the after_request decorator to set Access-Control-Allow
  """

    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type, Authorization"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET, PATCH, POST, DELETE, OPTIONS"
        )
        return response

    def paginate_questions(request, selection):

        page = request.args.get("page", 1, type=int)

        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        questions = [question.format() for question in selection]
        questions = questions[start:end]

        return questions

    """
  @DONE: 
  Create an endpoint to handle GET requests 
  for all available categories.
  """

    @app.route("/categories", methods=["GET"])
    def get_categories():

        categories = Category.query.all()

        if len(categories) == 0:
            abort(404)

        categories = [category.type for category in categories]

        return jsonify(
            {
                "success": True,
                "categories": categories,
                "total_categories": len(categories),
            }
        )

    """
  @DONE: 
  Create an endpoint to handle GET requests 
  for all available categories.
  """

    @app.route("/categories", methods=["POST"])
    def create_categories():

        body = request.get_json()

        category_type = body.get("type", None)

        if category_type is None:
            abort(422)

        category = Category(category_type)
        category.insert()

        return jsonify({"success": True, "category": category.format()})

    """
  @DONE: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  """

    @app.route("/questions", methods=["GET"])
    def get_questions():

        questions = Question.query.all()

        len_questions = len(questions)

        questions = paginate_questions(request, questions)

        if len(questions) == 0:
            abort(404)

        categories = Category.query.all()

        categories = [category.type for category in categories]

        return jsonify(
            {
                "success": True,
                "questions": questions,
                "total_questions": len_questions,
                "current_category": categories,
                "categories": categories,
            }
        )

    """
  @DONE: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  """

    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_questions_by_id(question_id):

        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()

            question.delete()

            return jsonify({"success": True, "deleted": question_id})
        except:
            abort(404)

    """
  @DONE: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  """

    @app.route("/questions", methods=["POST"])
    def create_questions():

        body = request.get_json()

        question = body.get("question", None)
        answer = body.get("answer", None)
        category = body.get("category", None)
        difficulty = body.get("difficulty", None)

        if question is None or answer is None or category is None or difficulty is None:
            abort(422)

        category = int(category) + 1

        question = Question(
            question=question, answer=answer, category=category, difficulty=difficulty
        )

        question.insert()

        return jsonify({"success": True, "question": question.format()})

    """
  @DONE: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  """

    @app.route("/search_questions", methods=["POST"])
    def search_questions():

        body = request.get_json()

        search_term = body.get("searchTerm", None)

        if not search_term:
            abort(422)

        questions = Question.query.filter(
            Question.question.ilike(f"%{search_term}%")
        ).all()

        questions = [question.format() for question in questions]

        return jsonify({"success": True, "questions": questions})

    """
  @DONE: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  """

    @app.route("/categories/<int:category_id>/questions", methods=["GET"])
    def get_questions_by_category(category_id):

        category_id = 1 + int(category_id)
        category = Category.query.filter(Category.id == category_id).one_or_none()

        if category is None:
            abort(404)

        questions = Question.query.filter(Question.category == category.id).all()

        if len(questions) == 0:
            abort(404)

        questions = [question.format() for question in questions]

        return jsonify(
            {"success": True, "questions": questions, "current_category": category.type}
        )

    """
  @DONE: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  """

    @app.route("/quizzes", methods=["POST"])
    def quizzes():

        body = request.get_json()

        previous_questions = body.get("previous_questions", None)
        category = body.get("quiz_category", None)

        if category is None:
            abort(422)

        category["id"] = int(category["id"])

        if category["id"] == -1:
            question = Question.query.filter(
                Question.id.notin_(previous_questions)
            ).first()
        else:
            question = (
                Question.query.filter(Question.category == (category["id"] + 1))
                .filter(Question.id.notin_(previous_questions))
                .first()
            )

        if question is None and len(previous_questions) != 0:
            return jsonify({"success": True, "question": None})

        if question is None:
            abort(404)

        return jsonify({"success": True, "question": question.format()})

    """
  @DONE: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  """

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"success": False, "error": 404, "message": "Not found"}), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422, "message": "Unprocessable"}),
            422,
        )

    return app
