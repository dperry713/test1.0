import unittest
from app import app, db, Sum

class TestSumAPI(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['TESTING'] = True
        self.client = app.test_client()
        with app.app_context():
            db.create_all()
    
    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_sums_by_result_success(self):
        # Create test data
        with app.app_context():
            sum1 = Sum(num1=2, num2=2, result=4)
            sum2 = Sum(num1=3, num2=1, result=4)
            sum3 = Sum(num1=1, num2=2, result=3)
            db.session.add_all([sum1, sum2, sum3])
            db.session.commit()

        # Test endpoint
        response = self.client.get('/sum/result/4')
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 2)
        self.assertTrue(all(sum_dict['result'] == 4 for sum_dict in data))

    def test_get_sums_by_result_not_found(self):
        # Test with a result that doesn't exist
        response = self.client.get('/sum/result/999')
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 0)

    def test_get_sums_by_result_invalid_input(self):
        # Test with invalid input (non-integer)
        response = self.client.get('/sum/result/invalid')
        
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
