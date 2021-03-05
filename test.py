from unittest import TestCase

from app import app
from models import db, User

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flaskbloglytest'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class UserProfilesTestCase(TestCase):

    def setUp(self):

        User.query.delete()

        user = User(first_name="Pinky",last_name="Buggy")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

    def tearDown(self):

        db.session.rollback()

    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code,200)
            self.assertIn('Pinky Buggy',html)

    def test_show_user(self):
         with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<p>Pinky Buggy</p>', html)

    def test_add_user(self):
        with app.test_client() as client:
            d = {"first_name":"Pinky","last_name":"Buggy"}
            resp = client.post("/users/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)
          

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<p>Pinky Buggy</p>',html)



    def test_show_Edit_user(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<p>Pinky Buggy</p>',html)
