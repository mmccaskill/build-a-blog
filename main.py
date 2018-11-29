from flask import Flask, request, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:Edwin!99@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] =True

db = SQLAlchemy(app)

app.secret_key = '9RT2xc3gH6FD1v23'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(120))
    content = db.Column(db.String(255))


    def __init__(self, title, content):
        self.title = title
        self.content = content

@app.route("/")
def index():
    return redirect('/blog')

@app.route('/blog', methods=['POST','GET'])
def blog():

    blogs = Blog.query.all()
    id = request.query_string
    if request.method == 'GET':
        if not id:
            return render_template('blog.html', blogs = blogs)
        else:
            b = int(request.args.get('b'))
            blog = Blog.query.get(b)
            return render_template('post.html', blog = blog)


       # return render_template('post.html', title=title, content=content, title_error=title_error, body_error=body_error)

#@app.route("/blog", methods=['GET'])
#def post():
 #   title = request.form.get('title')
  #  content = request.form.get('content')
   # return render_template('post.html', title=title, content=content)


@app.route('/newpost', methods = ['GET'])
def newpost():

    return render_template('newpost.html')


@app.route('/newpost', methods=['POST'])
def add_post():

    title = request.form['title']
    content = request.form['content']

    if not title and not content:
        return render_template('newpost.html', title_error="🚨You Must Include A Title", content_error="🚨You Must Include Blog Content")

    elif not title:
        return render_template('newpost.html', title_error="🚨You Must Include A Title", content=content)

    elif not content:
        return render_template('newpost.html', title=title, content_error="🚨You Must Include Blog Content")

        return render_template('/blog?id={0}'.format(Blog))
#case 2 issue
    else:
        new_post = Blog(title, content)
        db.session.add(new_post)
        db.session.commit()
        blog = new_post

    return render_template('new_entry.html', blog = blog)


if __name__ == '__main__':
    app.run()