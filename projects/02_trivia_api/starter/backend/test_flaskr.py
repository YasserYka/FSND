import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from models import Category

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}/{}".format(
            "postgres:postgres@localhost:5432", self.database_name
        )
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    @DONE:
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_questions(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_questions"])
        self.assertTrue(len(data["questions"]))

    def test_404_get_questions(self):
        res = self.client().get("/questions?page=50")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Not found")

    def test_get_categories(self):

        res = self.client().post("/categories", json={"type": "Sport"})

        res = self.client().get("/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_categories"])
        self.assertTrue(len(data["categories"]))

    def test_405_categories(self):

        res = self.client().put("/categories", json={"type": "Sport"})

        self.assertEqual(res.status_code, 405)

    def test_post_question(self):

        res = self.client().post(
            "/questions",
            json={
                "question": "Who am I",
                "answer": "You",
                "difficulty": 1,
                "Category": 1,
            },
        )

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["question"])

    def test_fail_post_question(self):

        res = self.client().post(
            "/questions",
            json={"question": "Who am I", "answer": "You", "difficulty": 1},
        )

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)

    def test_search_questions(self):

        self.client().post(
            "/questions",
            json={
                "question": "Who am I",
                "answer": "You",
                "difficulty": 1,
                "Category": 1,
            },
        )

        res = self.client().post("/search_questions", json={"searchTerm": "Who"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["questions"]))

    def test_fail_search_questions(self):

        self.client().post(
            "/questions",
            json={
                "question": "Who am I",
                "answer": "You",
                "difficulty": 1,
                "Category": 1,
            },
        )

        res = self.client().post("/search_questions", json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)

    def test_get_questions_by_category(self):

        res = self.client().get("/categories/1/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["questions"]))

    def test_fail_get_questions_by_category(self):

        res = self.client().get("/categories/123/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)

    def test_quizzes(self):

        res = self.client().post(
            "/quizzes",
            json={
                "previous_questions": [],
                "quiz_category": {"type": "Science", "id": 1},
            },
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["question"])

    def test_fail_quizzes(self):

        res = self.client().post("/quizzes", json={"previous_questions": []})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)

    def test_post_question(self):

        res = self.client().post("/categories", json={"type": "Sport"})

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["category"])

    def test_fail_post_question(self):

        res = self.client().post("/categories", json={})

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
