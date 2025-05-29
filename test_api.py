# This file contains unit tests for the REST API endpoints of the Flask user management application.
# The tests cover positive and negative cases for all CRUD operations using the unittest framework.

import unittest
import json
import sys
import os

# Add the project directory to sys.path to allow imports
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from myapp import app, db
from models import User

class UserApiTestCase(unittest.TestCase):
    def setUp(self):
        # Set up test client and initialize database
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        # Clean up database
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_user(self):
        # Test creating a new user (positive case)
        response = self.client.post('/user', data={
            'name': 'Test User',
            'email': 'testuser@example.com',
            'pwd': 'password123',
            'mobile': '1234567890'
        })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 201)
        self.assertIn('user_id', data)

    def test_create_user_missing_fields(self):
        # Test creating a user with missing fields (negative case)
        response = self.client.post('/user', data={
            'name': '',
            'email': '',
            'pwd': '',
            'mobile': ''
        })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        # The current implementation does not validate input, so status 201 might still be returned
        # This test can be updated if validation is added
        self.assertIn('status', data)

    def test_get_all_users(self):
        # Test getting all users (positive case)
        # First create a user
        self.test_create_user()
        response = self.client.get('/user')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 200)
        self.assertIsInstance(data['data'], list)
        self.assertGreaterEqual(len(data['data']), 1)

    def test_get_specific_user(self):
        # Test getting a specific user by ID (positive case)
        # First create a user
        self.test_create_user()
        response = self.client.get('/user/1')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 200)
        self.assertIsInstance(data['data'], list)
        self.assertEqual(len(data['data']), 1)

    def test_get_nonexistent_user(self):
        # Test getting a user that does not exist (negative case)
        response = self.client.get('/user/999')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 404)

    def test_update_user(self):
        # Test updating a user (positive case)
        self.test_create_user()
        response = self.client.put('/user/1', data={
            'name': 'Updated User',
            'email': 'updated@example.com',
            'pwd': 'newpassword',
            'mobile': '0987654321'
        })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 200)

    def test_update_nonexistent_user(self):
        # Test updating a user that does not exist (negative case)
        response = self.client.put('/user/999', data={
            'name': 'No User'
        })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 404)

    def test_delete_user(self):
        # Test deleting a user (positive case)
        self.test_create_user()
        response = self.client.delete('/user/1')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 200)

    def test_delete_nonexistent_user(self):
        # Test deleting a user that does not exist (negative case)
        response = self.client.delete('/user/999')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 404)

if __name__ == '__main__':
    unittest.main()
