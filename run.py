from app import app, db
from app.models import User, Post, Votes, Dislikes

@app.shell_context_processor
def shell_context():
    return {'db': db,'User': User, 'Post': Post, 'Votes': Votes, 'Dislikes': Dislikes}


if __name__ == '__main__':
    app.run()