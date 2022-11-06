from email.policy import default
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

base_dir = os.path.dirname(os.path.realpath(__file__))


# Making Flask Module Instance
app = Flask(__name__)

#Database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db= SQLAlchemy(app)

#Creating Models and Fields
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(30), nullable=False, default='Unknown')
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return str(self.title)


# db.create_all()

# making url and function for the render template
@app.route('/')
@app.route('/homepage')
def index():
    return render_template('blog/index.html')

@app.route('/create_posts', methods=['GET', 'POST'])
def createPost():
    if request.method == 'POST':
        blog_title = request.form['title']
        blog_content = request.form['content']
        blog_author = request.form['author']

        #Creating New Blog
        new_blog = BlogPost(title=blog_title, content=blog_content, author=blog_author)
        db.session.add(new_blog)
        db.session.commit()
        return redirect(url_for('postsViews'))
    else:
        return render_template('blog/create_posts.html')


@app.route('/posts/delete/<int:pk>')
def deletePost(pk):
    blog = BlogPost.query.get(pk)
    if blog:
        db.session.delete(blog)
        db.session.commit()
        return redirect(url_for('postsview'))
    else:
        return 'Blog Not Found!!!'


app.route('/post/edit/<int:pk>', methods=['GET', 'POST'])
def editPost(pk):
    blog = BlogPost.query.get(pk)
    if blog:
        if request.method == 'POST':
            blog_title = request.form['title']
            blog_content = request.form['content']
            blog_author = request.form['author']

        
            new_blog = BlogPost(title=blog_title, content=blog_content, author=blog_author)
            db.session.add(new_blog)
            db.session.commit()
            return redirect(url_for('postsViews'))
        else:
            return render_template('blog/update.html', content=blog)

    else:
        return 'Blog Not Found!!!'

# with app.app_context():
#     db.session.commit()


@app.route('/posts')
def postsViews():
    return render_template('blog/posts.html')






if __name__ == '__main__':
    app.run(debug=True)