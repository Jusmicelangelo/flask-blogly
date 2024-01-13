from flask_sqlalchemy import SQLAlchemy
import datetime

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
    
    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")
    
    def greet(self):
        return f"Logged in as {self.first_name} {self.last_name}"
    

    
class Post(db.Model):
    """Posts"""

    __tablename__ = "posts"

    def __repr__(self):
        p = self
        return f"<Post: {p.title} {p.content} {p.user_id}>"

    id = db.Column (db.Integer,
                    primary_key = True,
                    autoincrement = True)
    
    title = db.Column (db.Text,
                       nullable = False)
    
    content = db.Column (db.Text,
                         nullable = False)
    
    created_at = db.Column (db.DateTime,
                            nullable = False,
                            default = datetime.datetime.now)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)

    category = db.relationship('PostTag', backref = 'tags')

    @property
    def friendly_date(self):
        """friendly formatted date."""

        return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")


class Tag(db.Model):
    """Tags"""

    __tablename__ = "tags"

    def __repr__(self):
        t = self
        return f"<Tag: {t.name}>"

    id = db.Column (db.Integer, 
                    primary_key= True, 
                    autoincrement = True)

    name = db.Column (db.Text,
                      nullable = False,
                      unique = True)
    
    posts = db.relationship('Post', secondary= 'posts_tags', backref= 'tags', 
                            cascade = "all,delete")
    
class PostTag(db.Model):
    """Tags a post """

    __tablename__ = "posts_tags"

    post_id = db.Column (db.Integer,
                         db.ForeignKey('posts.id'),
                         nullable = False,
                         primary_key = True)
    
    tag_id = db.Column (db.Integer,
                        db.ForeignKey('tags.id'),
                        nullable = False,
                        primary_key = True)
    
def connect_db(app):
    """Connect to database"""
    db.app = app
    db.init_app(app)

