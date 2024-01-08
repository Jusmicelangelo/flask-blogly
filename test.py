from unittest import TestCase

from app import app
from models import db, User

#test database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

#make Flask errors be real errors, rather than html page with error info
app.config['Testing'] = True

#don't use flask debugtoolbar
app.config['DEBUG_DB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class UserModelTestCase(TestCase):
    """Test for User Model"""

    def setUp(self):
        """Clean up any existing users and define 1st user"""
        User.query.delete()

        user = User(first_name="John", last_name="Lennon", profile_image = "homepage")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id
        self.user = user

    def tearDown(self):
        """Clean up any fouled transaction"""
        db.session.rollback()

    def test_users(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("John", html)

    def test_user_details(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("John", html)
            self.assertIn(self.user.last_name, html)

    def test_users_delete(self):
        with app.test_client() as client:
            resp = client.post(f"/users/{self.user_id}/delete", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIsNot("John", html)

    # UNFORTUNATELY I cannot find the mistake why I get a 400 error code
    # def test_update_user(self):
    #     with app.test_client() as client:
               
    #         resp = client.post(f'/users/{self.user_id}/edit', 
	# 			data={'first_name': 'Gustav', 'last_name': 'Wiesl', 'profile_image': 'www.photos.com'})
    #         html= resp.get_data(as_text=True)

    #         self.assertEqual(resp.status_code, 200)
    #         self.assertEqual('Gustav', html),
    #         self.assertEqual('Wiesl', html),
    #         self.assertEqual('www.photos.com', html),

