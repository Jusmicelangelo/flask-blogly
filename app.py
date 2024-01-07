"""Blogly application."""

from flask import Flask, redirect, render_template
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'ihaveasecret'

connect_db(app)
app.app_context().push()
db.create_all()

@app.route('/')
def root():
    """Homepage redirects to list of users."""

    return redirect("/users")

@app.route('/users')
def users():
    """Shows a complete list of users"""
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template("/users", users = users)