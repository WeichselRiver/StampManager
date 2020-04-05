from flask import render_template, flash, redirect, url_for
from stamp_manager import app
from stamp_manager.forms import RegistrationForm, LoginForm
from stamp_manager.models import User, Post
from stamp_manager.data import Articles


Articles = Articles()


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/articles')
def articles():
    return render_template('articles.html', articles=Articles)


@app.route('/article/<string:title>/')
def article(title):
    return render_template('article.html', title=title)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'c.weichsel@gmx.de' and form.password.data == 'password':
            flash(f'You have logged in !', 'success')
            return redirect(url_for('home'))
        else:
            flash(f'Login not successful!', 'danger')
    return render_template('login.html', title='Login', form=form)
