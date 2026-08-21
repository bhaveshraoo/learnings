import unittest
import json
from app import app

class TestMentalHealthPredictor(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Mental Health Score Predictor', response.data)

    def test_prediction_endpoint(self):
        payload = {
            'Study_Hours': 4.0,
            'Age': 21,
            'Avg_Daily_Usage_Hours': 3.5,
            'Daily_Unlocks': 120,
            'Physical_Activity_Hours': 1.5,
            'Sleep_Hours_Per_Night': 7.5,
            'Stress_Level': 'Medium',
            'Gender': 'Female',
            'Academic_Level': 'Undergraduate',
            'Most_Used_Platform': 'Instagram',
            'Purpose_Of_Use': 'Entertainment',
            'Country': 'India'
        }
        response = self.client.post('/predict', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])
        self.assertIsInstance(data['score'], float)
        self.assertGreaterEqual(data['score'], 0.0)
        self.assertLessEqual(data['score'], 10.0)
        self.assertIn('status', data)
        self.assertIn('tips', data)

    def test_unknown_country_fallback(self):
        payload = {
            'Study_Hours': 2.0,
            'Age': 22,
            'Avg_Daily_Usage_Hours': 6.0,
            'Daily_Unlocks': 200,
            'Physical_Activity_Hours': 0.5,
            'Sleep_Hours_Per_Night': 5.0,
            'Stress_Level': 'High',
            'Gender': 'Male',
            'Academic_Level': 'Graduate',
            'Most_Used_Platform': 'TikTok',
            'Purpose_Of_Use': 'News',
            'Country': 'Japan' # Not in top 10, maps to 'Other'
        }
        response = self.client.post('/predict', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])
        self.assertIsInstance(data['score'], float)

if __name__ == '__main__':
    unittest.main()
