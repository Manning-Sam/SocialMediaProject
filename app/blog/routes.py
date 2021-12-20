from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import current_user, login_required 

from .forms import CreatePostForm

from app.models import Post, User, Votes, Dislikes

blog = Blueprint('blog', __name__, template_folder='blog_templates')

from app.models import db

@blog.route('/feed')
def blogHome():
    posts = db.session.query(Post,User).filter(Post.user_id==User.id).filter(Post.user_id!=2).order_by(Post.date_created.desc()).all()
    likes = Votes.query.all()
    dislikes = Dislikes.query.all()
    return render_template('blog.html', posts = posts, likes = likes, dislikes = dislikes)

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
def individualPost(id):
    post = db.session.query(Post,User).filter(Post.user_id==User.id).filter(Post.id==id).first()
    likes = Votes.query.all()
    dislikes = Dislikes.query.all()
    print(post)
    if post[0] is None:
        return redirect(url_for('blogHome'))
    if post[0].child:
        child_post=db.session.query(Post,User).filter(Post.user_id==User.id).filter(Post.parent==id).all()
        print(child_post)
        return render_template('individualpost.html', post=post, child_post=child_post, likes = likes, dislikes = dislikes)
    return render_template('individualpost.html', post=post, likes = likes, dislikes = dislikes)

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
    
    post.content = "This post was removed by the user"
    post.title = "[Deleted]"
    post.user_id = 2
    post.likes = 0
    post.dislikes = 0
    post.score = 0
    db.session.commit()
    return redirect(url_for('blog.blogHome'))

@blog.route('/blog/l/<int:id>')
@login_required
def likedPost(id):
    like = Votes(current_user.id, id)
    db.session.add(like)
    return redirect(url_for('blog.individualPost', id=id))

@blog.route('/blog/d/<int:id>')
@login_required
def dlikedPost(id):
    dlike = Dislikes(current_user.id, id)
    db.session.add(dlike)
    db.session.commit()
    return redirect(url_for('blog.individualPost', id=id))

@blog.route('/blog/ul/<int:id><int:pid>')
@login_required
def unlikedPost(id):
    like = Votes.query(id=id).first()
    db.session.add(like)
    db.session.commit()
    return redirect(url_for('blog.individualPost', pid=id))    

@blog.route('/blog/ud/<int:id><int:pid>')
@login_required
def undlikedPost(id):
    dlike = Dislikes.query(id=id).first()
    db.session.delete(dlike)
    db.session.commit()
    return redirect(url_for('blog.individualPost', pid=id))    