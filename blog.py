import os
from flask import Flask,render_template, redirect,url_for, request, session, flash
from functools import wraps
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import Integer,Text,DateTime, create_engine
from time import gmtime, strftime
# from sqlalchemy.sql.schema import Column
# from sqlalchemy.orm import scoped_session,sessionmaker
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy_utils import database_exists, create_database
from flask.ext.wtf import Form
from wtforms import StringField,BooleanField, TextField, PasswordField, validators
from wtforms.validators import DataRequired
import datetime
# import sqlite3

app = Flask(__name__)
app.debug = True

app.secret_key = 'I dont know'

# class Register(Form):
#     username = TextField('username', [validators.Length(min=4, max=25)])
#     email = TextField('email', [validators.Length(min=6, max=35)])
#     password = PasswordField('password', [validators.Length(min=6, max=35)])

# class PostForm(Form):
# 	title = TextField('title', [validators.Required()])
# 	body = TextField('body', [validators.Required()])

# class Blog(Form):
# 	__tablename__='blog_main'
# 	blog_id = Column(Integer,primary_key=True,autoincrement=True)
# 	title = Column(Text, nullable=False)
# 	body = Column(Text, nullable=False)
# 	date = Column(DateTime, default=datetime.datetime.utcnow())

# class MainForm(Form):
#     openid = StringField('openid', validators = [DataRequired()])
#    # remem = BooleanField('Remember_me',default=False)    

#login required decorator
def login_required(f):
    @wraps(f)
    def wrap(*args,**kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first...')
            return redirect(url_for('login'))
    return wrap


@app.route('/Main', methods=['GET','POST'])
def Main():
    form = MainForm()
    return render_template('frontpg.html',
                            title='main',
                            form=form)
#use decorator to link the function to the url.

@app.route('/', methods=['GET','POST'])
def home():
    query = 'select title,body from post;'    
    cur = engine.execute(query)
    content = [dict(title=row[0],body=row[1]) for row in cur.fetchall()][::-1]
    #r = [list((res.description[idx][0])for idx in enumerate(row)) for row in res.fetchall()]
    return render_template('frontpg.html', content=content,
                            time=strftime("%Y-%m-%d",gmtime()))


@app.route('/admin', methods=['GET','POST'])
def admin():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('Main'))
    return render_template('admin.html', 
                            error = error)
    
@app.route('/post',methods = ['GET','POST'])
def post():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        engine.execute("INSERT INTO post VALUES('{}','{}')".format(title,body))
    return render_template('post.html')

@app.route('/logout')
@login_required  
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('home'))

# @app.route('/register',methods=['GET','POST']) 
# def Register_page():
#     error = None
#     if request.method == 'POST':
#         print "in if loop"
#         db_session.add(Register(username=request.form['username'],email=request.form['email'], password=request.form['password']))
#         db_session.commit()
#         print "executed db commit"
#         flash('Thanks for registering')
#         return redirect(url_for('login'))
#     return render_template('register.html',form=Register(request.form),error=error)

if __name__ == '__main__':
	#DB configuration
    conn_str = 'sqlite:///blog.db'
    engine = create_engine(conn_str)
    # query = 'insert into post values("first post","abcdefgh");'
    # engine.execute(query)
    app.run()
    # engine.close(conn_str)