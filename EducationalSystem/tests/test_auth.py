import unittest
from EducationalSystem.app import create_app
from EducationalSystem.app.models import user_model
import bcrypt

class TestAuth(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()


        hashed_password = bcrypt.hashpw("123".encode(), bcrypt.gensalt()).decode('utf-8')
        self.test_user = user_model.create_user("test_user", hashed_password, "teacher")



    def tearDown(self):
        self.app_context.pop()


    def test_login_success(self):
        response = self.client.post('/', data={
            "username": "test_user",
            "password": "123",
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("/dashboard", response.data.decode())



if __name__ == '__main__':
    unittest.main()


