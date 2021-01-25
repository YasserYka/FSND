import os
import unittest
from app import create_app
import json
from flask_sqlalchemy import SQLAlchemy

from models import setup_db, Car, Person, database_path, db_drop_and_create_all

MANAGER_TOKEN = os.environ.get('MANAGER_TOKEN')
HELPDESK_TOKEN = os.environ.get('HELPDESK_TOKEN')


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        setup_db(self.app)
        db_drop_and_create_all()
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_persons(self):

        self.client().post(
            "/persons",
            headers={
                'Authorization': MANAGER_TOKEN},
            json={
                'name': 'Yasser',
                'age': 18,
            })

        res = self.client().get("/persons",
                                headers={'Authorization': MANAGER_TOKEN})

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["persons"])

    def test_get_404_persons(self):

        # remove all rows
        Person.query.delete()

        res = self.client().get("/persons",
                                headers={'Authorization': MANAGER_TOKEN})

        self.assertEqual(res.status_code, 404)

    def test_get_cars(self):

        self.client().post(
            "/persons",
            headers={
                'Authorization': MANAGER_TOKEN},
            json={
                'name': 'Yasser',
                'age': 18,
            })

        self.client().post(
            "/cars",
            headers={
                'Authorization': MANAGER_TOKEN},
            json={
                'color': 'red',
                'release': 2021,
                'person_name': 'Yasser'})

        res = self.client().get("/cars",
                                headers={'Authorization': MANAGER_TOKEN})

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["cars"])

    def test_get_404_cars(self):

        # remove all rows
        Car.query.delete()

        res = self.client().get("/cars",
                                headers={'Authorization': MANAGER_TOKEN})

        self.assertEqual(res.status_code, 404)

    def test_post_car(self):

        self.client().post(
            "/persons",
            headers={
                'Authorization': MANAGER_TOKEN},
            json={
                'name': 'Yasser',
                'age': 18,
            })

        res = self.client().post(
            "/cars",
            headers={
                'Authorization': MANAGER_TOKEN},
            json={
                'color': 'red',
                'release': 2021,
                'person_name': 'Yasser'})

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["cars"])

    def test_post_persons(self):

        res = self.client().post(
            "/persons",
            headers={
                'Authorization': MANAGER_TOKEN},
            json={
                'name': 'Yasser',
                'age': 18,
            })

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["persons"])

    def test_fail_post_car(self):
        Person.query.delete()

        res = self.client().post(
            "/cars",
            headers={
                'Authorization': MANAGER_TOKEN},
            json={
                'color': 'red',
                'release': 2021,
                'person_name': 'Yasser'})

        self.assertEqual(res.status_code, 422)

    def test_fail_post_persons(self):

        res = self.client().post(
            "/persons",
            headers={
                'Authorization': MANAGER_TOKEN},
            json={
                'age': 18,
            })

        self.assertEqual(res.status_code, 422)

    def test_patch_person(self):
        res = self.client().post(
            "/persons",
            headers={
                'Authorization': MANAGER_TOKEN},
            json={
                'name': 'Sam',
                'age': 18,
            })

        old_person = json.loads(res.data)['persons'][0]

        res = self.client().patch(
            "/persons/" + str(
                old_person['id']), headers={
                'Authorization': MANAGER_TOKEN}, json={
                'name': 'Sam', 'age': 19, })

        self.assertNotEqual(
            old_person['age'], json.loads(
                res.data)['persons'][0]['age'])

    def test_patch_person(self):

        res = self.client().patch(
            "/persons/213213",
            headers={
                'Authorization': MANAGER_TOKEN},
            json={
                'name': 'DontExists',
                'age': 19,
            })

        self.assertEqual(res.status_code, 404)

    def test_delete_person(self):
        res = self.client().post(
            "/persons",
            headers={
                'Authorization': MANAGER_TOKEN},
            json={
                'name': 'NewPerson',
                'age': 18,
            })

        res = self.client().delete(f"/persons/" +
                                   str(json.loads(res.data)['persons'][0]['id']
                                       ),
                                   headers={'Authorization': MANAGER_TOKEN})

        self.assertEqual(res.status_code, 200)

    def test_fail_delete_person(self):
        res = self.client().delete(
            f"/persons/23423432",
            headers={
                'Authorization': MANAGER_TOKEN})

        self.assertEqual(res.status_code, 404)

    def manager_post_person(self):

        res = self.client().post(
            '/persons',
            headers={
                'Authorization': MANAGER_TOKEN},
            json={
                'name': 'Sam',
                'age': 18,
            })

        records = json.loads(res.data)

        self.assertEqual(res.status_code, 200)

    def fail_helpdesk_post_person(self):

        res = self.client().post(
            '/persons',
            headers={
                'Authorization': HELPDESK_TOKEN},
            json={
                'name': 'Sam',
                'age': 18,
            })

        records = json.loads(res.data)

        self.assertEqual(res.status_code, 403)

    def help_desk_patch_person(self):

        res = self.client().post(
            '/persons',
            headers={
                'Authorization': HELPDESK_TOKEN},
            json={
                'name': 'Sam',
                'age': 18,
            })

        records = json.loads(res.data)

        self.assertEqual(res.status_code, 200)

    def manager_delete_person(self):

        res = self.client().post(
            '/persons',
            headers={
                'Authorization': MANAGER_TOKEN},
            json={
                'name': 'Sam',
                'age': 18,
            })

        res = self.client().delete('/persons/' +
                                   str(json.loads(res.data)['persons']
                                       [0]['id']),
                                   headers={'Authorization': MANAGER_TOKEN})

        records = json.loads(res.data)

        self.assertEqual(res.status_code, 200)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
