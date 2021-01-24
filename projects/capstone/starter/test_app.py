import os
import unittest
from app import create_app
import json
from flask_sqlalchemy import SQLAlchemy

from models import setup_db, Car, Person, database_path, db_drop_and_create_all


MANAGER_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlNJTFd6YkFzbTQySHdSaFo4ek0zSCJ9.eyJpc3MiOiJodHRwczovL2RldmhhcmRjb2RpbmcudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYwMGM5NTFiZGY3YjVhMDA3MThkOThmNCIsImF1ZCI6ImNhcHN0b25lIiwiaWF0IjoxNjExNTAwMjM4LCJleHAiOjE2MTE1ODY2MzgsImF6cCI6ImhqdGRWUVlRSUQ4dHl5OVo1Q1BEVFBxcllwdER2RVptIiwiZ3R5IjoicGFzc3dvcmQiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6cGVyc29ucyIsImdldDpjYXJzIiwiZ2V0OnBlcnNvbnMiLCJwYXRjaDpwZXJzb25zIiwicG9zdDpjYXJzIiwicG9zdDpwZXJzb25zIl19.OOYxP06e674L0DF28tBNkqA8O73NtiUZAggKIq05rKiVhXAUJzLkNLx5TtEmXrnx_5bmK_FBfwtv37G8IopVcDqFgi2Ob3k2a0hMsEmVvFXJTD-P8Feij_IgP1nobEPXOt75pOSJdl1RsNsBMLAJRXtkbO5fsJ16hPQ43spoMa6_vY12nNnEMEVnaLyGq5LE2uFpAjCVy3fetay1q4pJSEkjlZBUvKDCLVClCjw3AVfjSJnvIiW1dgq9QHH6EbtByCQnrM_dXPm8D6T9zIypCKETF7uopSP5-wo5LCW9TRLHCcHnnR9WdfTR6QTG_sV9IjuifFOFhPrhjqfipD-0cw'
HELPDESK_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlNJTFd6YkFzbTQySHdSaFo4ek0zSCJ9.eyJpc3MiOiJodHRwczovL2RldmhhcmRjb2RpbmcudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYwMGM5NTFiZGY3YjVhMDA3MThkOThmNCIsImF1ZCI6ImNhcHN0b25lIiwiaWF0IjoxNjExNTAwMjY2LCJleHAiOjE2MTE1ODY2NjYsImF6cCI6ImhqdGRWUVlRSUQ4dHl5OVo1Q1BEVFBxcllwdER2RVptIiwiZ3R5IjoicGFzc3dvcmQiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6cGVyc29ucyIsImdldDpjYXJzIiwiZ2V0OnBlcnNvbnMiLCJwYXRjaDpwZXJzb25zIiwicG9zdDpjYXJzIiwicG9zdDpwZXJzb25zIl19.S9dUFlkWt41w1zck6RlCXYGvYA9MSE85y--vUBETp1tZ6nuKONYvaVch1wUp9n7WVcLSt_p1Ml9AVhuRzWxTAKjGWHghgsEpIg_PLg8eDyzIGfCXlnEoGs6YYsS5ufFYe43wUzGR3PQ6O26yJ322uemcfKivBakLI0q3NQCAQxdGF0bLKCwsgWt1kTT3NjNVLEov-GKNFMd7erpgbyNVHah46qKszj-iq3MXS1yxpvhNClOnQQg1h8YVida6iEWedkBVHPn0rsR3JxJN-DHiEmpCVK-RPW3Cs_XY7xsyQi2D1xkB6Ql013SStYEX7p0VcuUq5np7MWBiQTXwSJ9jIQ'

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

        self.client().post("/persons", json={
            'name': 'Yasser',
            'age': 18,
        })

        res = self.client().get("/persons")

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["persons"])

    def test_get_404_persons(self):

        # remove all rows
        Person.query.delete()

        res = self.client().get("/persons")

        self.assertEqual(res.status_code, 404)


    def test_get_cars(self):

        self.client().post("/persons", json={
            'name': 'Yasser',
            'age': 18,
        })

        self.client().post("/cars", json={
            'color': 'red',
            'release': 2021,
            'person_name': 'Yasser'
        })

        res = self.client().get("/cars")

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["cars"])


    def test_get_404_cars(self):

        # remove all rows
        Car.query.delete()

        res = self.client().get("/cars")

        self.assertEqual(res.status_code, 404)


    def test_post_car(self):

        self.client().post("/persons", json={
            'name': 'Yasser',
            'age': 18,
        })

        res = self.client().post("/cars", json={
            'color': 'red',
            'release': 2021,
            'person_name': 'Yasser'
        })

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["cars"])

    def test_post_persons(self):

        res = self.client().post("/persons", json={
            'name': 'Yasser',
            'age': 18,
        })

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["persons"])

    def test_fail_post_car(self):
        Person.query.delete()

        res = self.client().post("/cars", json={
            'color': 'red',
            'release': 2021,
            'person_name': 'Yasser'
        })

        self.assertEqual(res.status_code, 422)

    def test_fail_post_persons(self):

        res = self.client().post("/persons", json={
            'age': 18,
        })

        self.assertEqual(res.status_code, 422)

    def test_patch_person(self):
        res = self.client().post("/persons", json={
            'name': 'Sam',
            'age': 18,
        })

        old_person = json.loads(res.data)['persons'][0]

        res = self.client().patch("/persons/" + str(old_person['id']), json={
            'name': 'Sam',
            'age': 19,
        }) 

        self.assertNotEqual(old_person['age'], json.loads(res.data)['persons'][0]['age'])

    def test_patch_person(self):

        res = self.client().patch("/persons/213213", json={
            'name': 'DontExists',
            'age': 19,
        }) 

        self.assertEqual(res.status_code, 404)

    def test_delete_person(self):
        res = self.client().post("/persons", json={
            'name': 'NewPerson',
            'age': 18,
        })

        res = self.client().delete(f"/persons/" + str(json.loads(res.data)['persons'][0]['id']))
        
        self.assertEqual(res.status_code, 200)

    def test_fail_delete_person(self):
        res = self.client().delete(f"/persons/23423432")
        
        self.assertEqual(res.status_code, 404)

def manager_post_person(self):

        res = self.client().post('/persons', headers={'Authorization': MANAGER_TOKEN}, json={
            'name': 'Sam',
            'age': 18,
        })

        records = json.loads(res.data)

        self.assertEqual(res.status_code, 200)

def fail_helpdesk_post_person(self):

        res = self.client().post('/persons', headers={'Authorization': HELPDESK_TOKEN}, json={
            'name': 'Sam',
            'age': 18,
        })

        records = json.loads(res.data)

        self.assertEqual(res.status_code, 403)

def help_desk_patch_person(self):

        res = self.client().post('/persons', headers={'Authorization': HELPDESK_TOKEN}, json={
            'name': 'Sam',
            'age': 18,
        })

        records = json.loads(res.data)

        self.assertEqual(res.status_code, 200)

def manager_delete_person(self):

        res = self.client().post('/persons', headers={'Authorization': MANAGER_TOKEN}, json={
            'name': 'Sam',
            'age': 18,
        })


        res = self.client().delete('/persons/' + str(json.loads(res.data)['persons'][0]['id']), headers={'Authorization': MANAGER_TOKEN})

        records = json.loads(res.data)

        self.assertEqual(res.status_code, 200)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
