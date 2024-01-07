from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

"""Models for Blogly."""

DEFAULT_IMAGE = "https://unsplash.com/de/fotos/ein-3d-bild-eines-mannes-mit-roten-linien-auf-seinem-korper-WWQzZO6kORA"

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

