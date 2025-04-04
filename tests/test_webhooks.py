import unittest
from app import create_app, db

class WebhookTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('test')
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_receive_message(self):
        response = self.client.post('/webhook', data={
            'From': 'whatsapp:+1234567890',
            'Body': 'Hello'
        })
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()