from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

"""Models for Blogly."""

DEFAULT_IMAGE = "https://images.unsplash.com/photo-1704278921589-ac35120085dd?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxlZGl0b3JpYWwtZmVlZHwzNHx8fGVufDB8fHx8fA%3D%3D"

class User(db.Model):
    """User."""

    __tablename__ = "users"

    def __repr__(self):
        u = self
        return f"<User: {u.first_name} {u.last_name}>"

    id = db.Column (db.Integer,
                    primary_key = True,
                    autoincrement = True)
    
    first_name = db.Column (db.Text,
                            nullable = False)
    
    last_name = db.Column (db.Text,
                           nullable = False)
    
    profile_image = db.Column (db.Text,
                               nullable = False,
                               default = DEFAULT_IMAGE)
    
    def greet(self):
        return f"Logged in as {self.first_name} {self.last_name}"
    
def connect_db(app):
    """Connect to database"""
    db.app = app
    db.init_app(app)

