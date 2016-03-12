import os
from flask import Flask,render_template, redirect,url_for, request, session, flash
from functools import wraps
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import Integer,Text,DateTime, create_engine
from time import gmtime, strftime
from flask.ext.wtf import Form
from wtforms import StringField,BooleanField, TextField, PasswordField, validators
from wtforms.validators import DataRequired
import datetime

app = Flask(__name__)
app.debug = True

app.secret_key = 'I dont know'



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

if __name__ == '__main__':
	#DB configuration
    conn_str = 'sqlite:///blog.db'
    engine = create_engine(conn_str)
    app.run()
