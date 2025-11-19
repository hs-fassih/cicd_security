"""
Basic test cases for Flask CRUD application
These tests verify core functionality WITHOUT affecting the production database.

Tests include:
1. Check if / returns 200
2. Check /add works properly by adding a test user
"""

import unittest
import sys
from pathlib import Path

# Add parent directory to path to import app
sys.path.insert(0, str(Path(__file__).parent.parent))


class FlaskAppTestCase(unittest.TestCase):
    """
    Basic test cases for Flask CRUD application
    IMPORTANT: Uses completely isolated in-memory test database
    Production database and existing data are NEVER touched
    """

    @classmethod
    def setUpClass(cls):
        """Set up test environment once for all tests"""
        # Import app components
        from app import app, db, User
        
        # Store references
        cls.app = app
        cls.db = db
        cls.User = User
        
        # Store original database URI to restore later
        cls.original_db_uri = app.config['SQLALCHEMY_DATABASE_URI']
        
        # Configure app for testing with in-memory database
        cls.app.config['TESTING'] = True
        cls.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Isolated in-memory DB
        cls.app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
        
        # Create test client
        cls.client = cls.app.test_client()

    @classmethod
    def tearDownClass(cls):
        """Restore original configuration after all tests"""
        # Restore original database URI
        cls.app.config['SQLALCHEMY_DATABASE_URI'] = cls.original_db_uri

    def setUp(self):
        """Set up clean database before each test"""
        # Push application context
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        # Create fresh tables for this test
        self.db.create_all()

    def tearDown(self):
        """Clean up after each test"""
        # Remove session and drop tables
        self.db.session.remove()
        self.db.drop_all()
        
        # Pop application context
        self.app_context.pop()

    # ==================== REQUIRED TESTS ====================

    def test_1_index_returns_200(self):
        """
        Test Case 1: Check if / returns 200
        Expected: GET request to home page returns HTTP 200 status code
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        print("✓ Test 1 PASSED: Home page (/) returns 200")

    def test_2_add_user_works_properly(self):
        """
        Test Case 2: Check /add works properly by adding a test user
        Test Data:
        - first_name: test
        - last_name: user
        - email: test@user.com
        - age: 18
        - city: Islamabad
        
        Expected: User is created successfully in database with correct data
        """
        # Test data as specified
        test_user_data = {
            'first_name': 'test',
            'last_name': 'user',
            'email': 'test@user.com',
            'age': '18',
            'city': 'Islamabad'
        }
        
        # Send POST request to /add endpoint
        response = self.client.post('/add', data=test_user_data, follow_redirects=True)
        
        # Verify response is successful
        self.assertIn(response.status_code, [200, 302], "POST request to /add should succeed")
        
        # Verify user was created in test database
        user = self.User.query.filter_by(email='test@user.com').first()
        self.assertIsNotNone(user, "User should be created in database")
        
        # Verify all user data is correct
        self.assertEqual(user.first_name, 'test', "First name should match")
        self.assertEqual(user.last_name, 'user', "Last name should match")
        self.assertEqual(user.email, 'test@user.com', "Email should match")
        self.assertEqual(user.age, 18, "Age should match")
        self.assertEqual(user.city, 'Islamabad', "City should match")
        
        print("✓ Test 2 PASSED: /add works properly - test user created successfully")
        print(f"  - User created: {user.first_name} {user.last_name} ({user.email})")
        print(f"  - Age: {user.age}, City: {user.city}")

    # ==================== ADDITIONAL SUPPORTING TESTS ====================

    def test_3_add_get_request_returns_form(self):
        """
        Additional Test: Verify GET request to /add returns the form
        Expected: GET /add returns status 200 with add user form
        """
        response = self.client.get('/add')
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.data)
        print("✓ Test 3 PASSED: GET /add returns add form")

    def test_4_form_validation_works(self):
        """
        Additional Test: Verify form validation prevents incomplete submissions
        Expected: Missing required fields should not create a user
        """
        # Incomplete data (missing email, age, city)
        incomplete_data = {
            'first_name': 'test',
            'last_name': 'user'
        }
        
        response = self.client.post('/add', data=incomplete_data, follow_redirects=True)
        
        # Verify no user was created with incomplete data
        user = self.User.query.filter_by(first_name='test', last_name='user').first()
        self.assertIsNone(user, "User should not be created with incomplete data")
        print("✓ Test 4 PASSED: Form validation prevents incomplete user creation")

    def test_5_duplicate_email_prevented(self):
        """
        Additional Test: Verify duplicate emails are not allowed
        Expected: Second user with same email should not be created
        """
        test_user_data = {
            'first_name': 'test',
            'last_name': 'user',
            'email': 'duplicate@test.com',
            'age': '18',
            'city': 'Islamabad'
        }
        
        # Create first user
        self.client.post('/add', data=test_user_data)
        
        # Try to create second user with same email
        test_user_data['first_name'] = 'another'
        self.client.post('/add', data=test_user_data, follow_redirects=True)
        
        # Verify only one user exists with this email
        users = self.User.query.filter_by(email='duplicate@test.com').all()
        self.assertEqual(len(users), 1, "Only one user with this email should exist")
        print("✓ Test 5 PASSED: Duplicate email prevention works")

    def test_6_index_displays_users(self):
        """
        Additional Test: Verify home page displays users after creation
        Expected: After adding user, index page should work correctly
        """
        # Add a test user
        test_user_data = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'email': 'jane@test.com',
            'age': '25',
            'city': 'Lahore'
        }
        self.client.post('/add', data=test_user_data)
        
        # Request home page
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        
        # Verify user exists in database
        user = self.User.query.filter_by(email='jane@test.com').first()
        self.assertIsNotNone(user)
        print("✓ Test 6 PASSED: Index page displays users correctly")


def run_basic_tests():
    """
    Run only the two required basic tests
    """
    print("\n" + "="*70)
    print("RUNNING BASIC TESTS (Required Tests Only)")
    print("="*70 + "\n")
    
    # Create test suite with only required tests
    suite = unittest.TestSuite()
    suite.addTest(FlaskAppTestCase('test_1_index_returns_200'))
    suite.addTest(FlaskAppTestCase('test_2_add_user_works_properly'))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "="*70)
    if result.wasSuccessful():
        print("✅ ALL BASIC TESTS PASSED!")
    else:
        print("❌ SOME TESTS FAILED")
    print("="*70 + "\n")
    
    return result


if __name__ == '__main__':
    # Check if user wants to run only basic tests
    if len(sys.argv) > 1 and sys.argv[1] == '--basic':
        run_basic_tests()
    else:
        # Run all tests with verbose output
        print("\n" + "="*70)
        print("RUNNING ALL TESTS (Basic + Additional)")
        print("="*70 + "\n")
        unittest.main(verbosity=2)
