from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import current_user, login_required 

from .forms import CreatePostForm

from app.models import Post, User

blog = Blueprint('blog', __name__, template_folder='blog_templates')

from app.models import db

@blog.route('/feed')
@login_required
def blogHome():
    posts = db.session.query(Post,User).filter(Post.user_id==User.id).all()
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

            return redirect(url_for('blog.blogHome'))
    return render_template('createpost.html', form = form)

@blog.route('/blog/<int:id>')
@login_required
def individualPost(id):
    post = db.session.query(Post,User).filter(Post.user_id==User.id).filter(Post.id==id).first()
    print(post)
    if post[0] is None:
        return redirect(url_for('blogHome'))
    if post[0].child:
        child_post=db.session.query(Post,User).filter(Post.user_id==User.id).filter(Post.parent==id).all()
        print(child_post)
        return render_template('individualpost.html', post=post, child_post=child_post)
    return render_template('individualpost.html', post=post)

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

@blog.route('/posts/delete/<int:id>', methods = ["POST"])
@login_required
def deletePost(id):
    post = Post.query.filter_by(id=id).first()
    if post.user_id != current_user.id:
        return redirect(url_for('blog.blogHome'))
    
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('blog.blogHome'))