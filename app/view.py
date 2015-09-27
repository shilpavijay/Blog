from app import app
from flask import render_template, redirect,url_for, request, session, flash
from .forms import MainForm
from functools import wraps

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
@app.route('/')
@login_required
def home():
    return render_template('welcome.html')

@app.route('/tech', methods=['GET','POST'])
def tech():
    form = MainForm()
    return render_template('tech.html',
                            title='tech',
                            form = form)

@app.route('/login', methods=['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('Main'))
    return render_template('login.html', 
                            error = error)
@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('home'))
