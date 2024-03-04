from django.test import TestCase
from rest_framework.test import APIClient

# Create your tests here.

class MyAPITestCase(TestCase):

    def test_teacher_signup(self):
        client = APIClient()
        data = {
            "user" :{
                'username': 'john',
                'email': 'john@example.com',
                'first_name': 'john',
                'last_name': 'adam'
                },
            'password': '1234',
            'password2': '1234'
            }
        response = client.post('/teachers/signup/', data=data, format='json')
        self.assertEqual(response.status_code, 201)

