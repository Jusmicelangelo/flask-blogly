"""Blogly application."""

from flask import Flask, redirect, render_template, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'ihaveasecret'

toolbar = DebugToolbarExtension(app)

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
    return render_template("/users.html", users = users)

@app.route('/users/new', methods=["GET"])
def users_new_form():
    """Form to create a new User"""

    return render_template('newUser.html')

@app.route('/users/new', methods=["POST"])
def create_user():
    """Creates a new User"""
    new_user = User (
        first_name = request.form['first_name'],
        last_name = request.form['last_name'],
        profile_image = request.form['image_url'] or None)
    
    db.session.add(new_user)
    db.session.commit()
    
    return redirect("/users")

@app.route('/users/<int:user_id>')
def user_details(user_id):
    """Details of an User"""
    user_detail = User.query.get_or_404(user_id)
    return render_template("userDetail.html", user = user_detail)


@app.route('/users/<int:user_id>/edit')
def users_edit_form(user_id):
    """Form to edit the User"""
    to_update_user = User.query.get_or_404(user_id)
    return render_template('edit.html', user = to_update_user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def update_user(user_id):
    """Updates User details"""
    update_user = User.query.get_or_404(user_id)
    update_user.first_name = request.form['first_name']
    update_user.last_name = request.form['last_name']
    update_user.profile_image = request.form['image_url']
    
    db.session.add(update_user)
    db.session.commit()
    
    return redirect("/users")


@app.route('/users/<int:user_id>/delete', methods=["POST"])
def users_delete(user_id):
    """delete a User"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")