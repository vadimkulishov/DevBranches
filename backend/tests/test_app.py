import unittest
from backend.app import app


class SimpleAppTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_home_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Welcome', response.get_data(as_text=True))


if __name__ == '__main__':
    unittest.main()
