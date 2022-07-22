from flask import Flask, render_template, redirect, request, url_for,session,flash,g
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import desc

app = Flask(__name__)

app.secret_key = "myblog"
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://wadolglkhevojs:a59a4eff860cf0945cc66de18012d287a96a5df8b7f3978404b7a72277723333@ec2-52-49-120-150.eu-west-1.compute.amazonaws.com:5432/d415i8h43grm90'
db = SQLAlchemy(app)
class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    author = db.Column(db.String(100), nullable = False, default = 'N/A')
    content = db.Column(db.Text, nullable = False)
    date_posted = db.Column(db.DateTime, nullable = False, default = datetime.now)
    comment = db.relationship('Comment')
    def __repr__(self):
        return 'Post' + str(self.id)

class Comment(db.Model):
    com_id = db.Column(db.Integer, primary_key = True)
    nickname = db.Column(db.String(100), nullable = False, default = 'Anonymous')
    email = db.Column(db.String(20), nullable = False, default = 'N/A')
    comment = db.Column(db.Text, nullable = False)
    time = db.Column(db.DateTime, nullable = False, default = datetime.now)
    id = db.Column(db.Integer, db.ForeignKey('post.id'))

# db.create_all()
# w = Post(title = "hello", author = "busayo", content="First Post")
# db.session.add(w)
# db.session.commit()
# posts = Post.query.all()
# for new in posts:
#     db.session.delete(new)
#     db.session.commit()
# w = Comment(nickname = "hello", email = "busayo", comment="First Post", id = 1)
# db.session.add(w)
# db.session.commit()
# posts = Comment.query.filter(Comment.id == 3).all()
# print(len(posts))
# for new in posts:
#     print(new.comment)
#     db.session.delete(new)
#     db.session.commit()


login_database = {"busayo":"busayo", "tosin":"tosin"}
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/thoughts", methods= ["POST", "GET"])
def thoughts():
    all_post = Post.query.order_by(desc(Post.date_posted)).all() 
    if request.method == 'POST':
        session.pop('name', None)
        name = request.form['username']
        pwd = request.form['password']
        session['name'] = name
        session['pwd'] = pwd
        if name not in login_database:
            flash("User not found")
            session.pop('name', None)
            return render_template('thoughts.html', posts = all_post)
        else:
            if login_database[name]!= pwd:
                flash("Incorrect password")
                session.pop('name', None)
                return render_template('thoughts.html', posts = all_post)
            else:
                return redirect('/posts')
        
    else:
        if 'name' and 'pwd' in session:
            return redirect(url_for('thoughtn'))
        return render_template('thoughts.html', posts = all_post)

@app.route("/thoughtn")
def thoughtn():
    all_post = Post.query.order_by(desc(Post.date_posted)).all()
    
    if g.name:
        return render_template("thoughtn.html", posts = all_post)
    return render_template('thoughts.html', posts = all_post)
@app.before_request
def before_request():
    g.name = None
    if 'name' in session:
        g.name = session['name']
# logging out of the website
@app.route('/logout')
def logout():
    if 'name' and 'pwd' in session:
        session.pop('name', None)
        session.pop('pwd', None)

    return redirect(url_for('thoughts'))

@app.route("/education")
def education():
    return render_template("education.html")
@app.route("/skills")
def skills():
    return render_template("skills.html")
@app.route("/projects")
def projects():
    return render_template("learning.html")
@app.route("/photography")
def photography():
    return render_template("photography.html")

@app.route("/posts", methods= ['GET', 'POST'])
def posts():
    if 'name' and 'pwd' in session:
        if request.method == 'POST':
            titles = request.form['title']
            authors = request.form['author']
            contents = request.form['content']
            new_post = Post(title = titles, author = authors, content = contents)
            if Post.title:
                db.session.add(new_post)
                db.session.commit()
            return redirect('/posts')
        else:
            all_post = Post.query.order_by(desc(Post.date_posted)).all()
            # print(all_post)
        return render_template("post.html", posts=all_post)
    else:
        return redirect("/")
@app.route("/posts/delete/<int:id>")
def delete(id):
    post = Post.query.get_or_404(id)
    comments = Comment.query.filter(Comment.id== id).all()
    if comments:
        for comment in comments:
            db.session.delete(comment)
            db.session.commit()
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')
@app.route("/posts/edit/<int:id>", methods=['GET', 'POST'])
def edit(id):
    post = Post.query.get_or_404(id)
    if request.method == 'POST':
        post.title = request.form['title']
        post.author = request.form['author']
        post.content = request.form['content']
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('edit.html', posts = post)
@app.route("/posts/comment/<int:id>", methods=['GET', 'POST'])
def comment(id):
    post = Post.query.get_or_404(id)
    all_comment = Comment.query.filter(Comment.id == id).order_by(desc(Comment.time)).all()
    num = Comment.query.filter(Comment.id == id).all()
    num = len(num)
    if request.method == 'POST':
        nicknames = request.form['nickname']
        emails = request.form['email']
        comments = request.form['comment']
        new_comment = Comment(nickname= nicknames, email = emails, comment = comments, id = id)
        db.session.add(new_comment)
        db.session.commit()
        return redirect('/thoughtn')
    else:
        if g.name:
            return render_template('comments.html', comments = all_comment, posts = post, nums = num)
        return render_template('commentmain.html', comments = all_comment, posts = post, nums =num)
@app.route("/comment/delete/<int:id>")
def delete_comment(id):
    post = Comment.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')
# @app.route('/base')
# def base():
#     return render_template("base.html")
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=80)
