import unittest
from EducationalSystem.app import create_app


class TestUserAuth(unittest.TestCase):
    def setUp(self):
        # setUp function is run before each test function is executed
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_login_page(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_dashboard_page(self):
        response = self.client.get("/dashboard", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome', response.data)

if __name__ == '__main__':
    unittest.main()