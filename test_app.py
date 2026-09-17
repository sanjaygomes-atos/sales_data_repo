
import unittest
from app import app

class SalesDataTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_total_revenue(self):
        response = self.app.get('/total_revenue')
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('total_revenue', data)

    def test_highest_region(self):
        response = self.app.get('/highest_region')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('region', data)
        self.assertIn('total_sales', data)

if __name__ == '__main__':
    unittest.main()

