from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import current_user, login_required 

from .forms import CreatePostForm

from app.models import Post

blog=Blueprint('blog', __name__,template_folder='blog_template')

from app.models import db

@blog.route('/')
def blogHome():
    posts = Post.query.all()
    return render_template('blog.html', posts = posts)

@blog.route('/posts/create/<int:id>', methods = ["GET","POST"])
@login_required
def createPost(id):
    form = CreatePostForm()
    if request.method == "POST":
        if form.validate():
            
            title = form.title.data
            content = form.content.data

            
            post = Post(title, content, current_user.id)

            if id:
                post.parent=id
                parent=Post.query.filter_by(id=id).first()
                parent.child=True 

            
            db.session.add(post)
            
            db.session.commit()

            return redirect(url_for('home'))
    return render_template('createpost.html', form = form)

@blog.route('/blog/<int:id>')
def individualPost(id):
    post = Post.query.filter_by(id=id).first()
    if post is None:
        return redirect(url_for('blogHome'))
    if post.child is not None:
        child_post=Post.query.filter_by(parent=id)
    return render_template('post.html', post=post, child_post=child_post)

@blog.route('/blog/update/<int:id>', methods = ["GET","POST"])
@login_required
def updatePost(id):
    post = Post.query.filter_by(id=id).first()
    if post.user_id != current_user.id:
        return redirect(url_for('blog.blogHome'))


    form = CreatePostForm()
    if request.method == "POST":
        if form.validate():
            
            title = form.title.data
            content = form.content.data

            if not title:
                title = post.title
            if not content:
                content = post.content

        
            post.title = title
            post.content = content

    
            db.session.commit()

            return redirect(url_for('blog.individualPost', id=id))
    return render_template('updatepost.html', form = form)
