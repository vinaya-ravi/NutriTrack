from django.test import TestCase
from rest_framework.test import APIClient

class APITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_meal_endpoint_valid_input(self):
        response = self.client.post('/api/meal/', {"meal": "1 apple"}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn("foods", response.json())

    def test_meal_endpoint_invalid_input(self):
        response = self.client.post('/api/meal/', {"meal": ""}, format='json')
        self.assertEqual(response.status_code, 400)

    def test_nutrition_endpoint(self):
        response = self.client.get('/api/nutrition/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Nutrition summary endpoint"})

    def test_suggestions_endpoint(self):
        response = self.client.get('/api/suggestions/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Suggestions endpoint"})
