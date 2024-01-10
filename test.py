from unittest import TestCase

from app import app
from models import db, User, Post

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
        """Clean up any existing post and users and define 1st user"""
        Post.query.delete()
        User.query.delete()
        
        """Setting up a start user for every test"""
        user = User(first_name="John", last_name="Lennon", profile_image = "homepage")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id
        self.user = user    

    def tearDown(self):
        """Clean up any fouled transaction"""
        db.session.rollback()

    def test_users(self):
        """Test show up of User"""
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("John", html)

    def test_user_details(self):
        """Test show up of details of User"""
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("John", html)
            self.assertIn(self.user.last_name, html)

    def test_users_delete(self):
        """Test for deleting a User"""
        with app.test_client() as client:
            resp = client.post(f"/users/{self.user_id}/delete", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIsNot("John", html)


    def test_update_user(self):
        """Test for updating user information"""
        with app.test_client() as client:
               
            resp = client.post(f'/users/{self.user_id}/edit', 
				data={'first_name': 'Gustav', 'last_name': 'Wiesl', 'image_url': 'www.photos.com'},
                follow_redirects=True)
            html= resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Gustav Wiesl", html)  


class PostModelTestCase(TestCase):
    """Test for Post Model"""

    def setUp(self):
        """Clean up any existing users and define 1st user"""
        Post.query.delete()
        User.query.delete()

        """Setting up a start user for every test"""
        user = User(first_name="John", last_name="Lennon", profile_image = "homepage")
        db.session.add(user)
        db.session.commit()

        """Setting up a start post for every test"""
        post = Post(title="HarryPotter", content="greatbook", user_id=user.id)
        db.session.add(post)
        db.session.commit()

        self.post_id = post.id
        self.user_id = user.id
        self.post = post

    def tearDown(self):
        """Clean up any fouled transaction"""
        db.session.rollback()

    def test_post_details(self):
        """Test show up of post details"""
        with app.test_client() as client:
            resp = client.get(f"/posts/{self.post_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("HarryPotter", html)
            self.assertIn(self.post.content, html)

    def test_update_post(self):
        """Test for updating a post"""
        with app.test_client() as client:
               
            resp = client.post(f'/posts/{self.post_id}/edit', 
				data={'title': 'Update', 'content': 'updated content'},
                follow_redirects=True)
            html= resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Update", html)  

    def test_create_post(self):
        """Test for creating a post"""
        with app.test_client() as client:
               
            resp = client.post(f'/users/{self.user_id}/posts/new', 
				data={'title': 'CreatePost', 'content': 'new created content'},
                follow_redirects=True)
            html= resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("CreatePost", html)  

    def test_post_delete(self):
        """Test for deleting a post"""
        with app.test_client() as client:
            resp = client.post(f"/posts/{self.post_id}/delete", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIsNot("HarryPotter", html)

