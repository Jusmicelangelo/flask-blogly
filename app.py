"""Blogly application."""

from flask import Flask, redirect, render_template, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'ihaveasecret'

toolbar = DebugToolbarExtension(app)

connect_db(app)
app.app_context().push()
db.create_all()

#User routes#
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
    return render_template('user_edit.html', user = to_update_user)

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

#Post routes#
@app.route('/users/<int:user_id>/posts/new', methods=["GET"])
def post_new_form(user_id):
    """Form to create a new Post for a specific User"""

    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()

    return render_template('newPost.html', user = user, tags=tags)

@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def create_post(user_id):
    """Creates a new Post for a specific User"""

    user = User.query.get_or_404(user_id)
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    new_post = Post (
        title = request.form['title'],
        content = request.form['content'],
        user=user,
        tags=tags)
   
    db.session.add(new_post)
    db.session.commit()
    
    return redirect(f"/users/{user_id}")

@app.route('/posts/<int:post_id>')
def post_details(post_id):
    """Details of an Post"""
    post_detail = Post.query.get_or_404(post_id)

    return render_template("postDetail.html", post = post_detail)

@app.route('/posts/<int:post_id>/edit')
def edit_post(post_id):
    '''Editing a post'''
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()

    return render_template('post_edit.html', post=post, tags = tags)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def update_post(post_id):
    """Updates Post details"""
    update_post = Post.query.get_or_404(post_id)
    update_post.title = request.form['title']
    update_post.content = request.form['content']

    tag_ids = [int(num) for num in request.form.getlist("tags")]
    update_post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    
    db.session.add(update_post)
    db.session.commit()
    
    return redirect(f'/posts/{post_id}')  

@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def post_delete(post_id):
    """delete a Post"""

    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()

    return redirect(f"/users/{post.user_id}")  

#tag routes#
@app.route('/tags')
def list_tags():
    """Shows a list of tags"""
    tags = Tag.query.all()
    return render_template('tags.html', tags = tags)

@app.route('/tags/<int:tag_id>')
def tag_details(tag_id):
    """Shows the posts related to a tag"""
    tag = Tag.query.get_or_404(tag_id)
    return render_template('tagDetail.html', tag = tag)

@app.route('/tags/new', methods=["GET"])
def new_tag():
    """Form to create a new Tag"""

    return render_template('newTag.html')


@app.route('/tags/new', methods=["POST"])
def create_tag():
    """Create a new Tag"""

    new_tag = Tag (name = request.form['name'])

    db.session.add(new_tag)
    db.session.commit()

    return redirect('/tags')

@app.route('/tags/<int:tag_id>/edit', methods=["GET"])
def edit_tag(tag_id):
    """Form to edit a Tag"""

    tag = Tag.query.get_or_404(tag_id)

    return render_template('tag_edit.html', tag=tag)

@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def update_tag(tag_id):
    """Update a Tag name"""

    to_update_tag = Tag.query.get_or_404(tag_id)
    to_update_tag.name = request.form['name']

    db.session.add(to_update_tag)
    db.session.commit()
    
    return redirect ('/tags')

@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def delete_tag(tag_id):
    """Deleta a Tag"""

    to_delete_tag = Tag.query.get_or_404(tag_id)

    db.session.delete(to_delete_tag)
    db.session.commit()

    return redirect ('/tags')