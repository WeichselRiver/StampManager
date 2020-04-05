from flask import render_template, flash, redirect, url_for, request
from stamp_manager import app, db, bcrypt
from stamp_manager.forms import RegistrationForm, LoginForm
from stamp_manager.models import User, Post
from stamp_manager.data import Articles
from flask_login import login_user, current_user, logout_user, login_required


Articles = Articles()


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title="Home")


@app.route('/about')
def about():
    return render_template('about.html', title="About")


@app.route('/articles')
def articles():
    return render_template('articles.html', articles=Articles, title="Sammelgebiete")


@app.route('/article/<string:title>/')
def article(title):
    return render_template('article.html', title=title)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('Succesfully logged in!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash(f'Login not successful!', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account")
@login_required
def account():
    image_file = url_for('static', filename="pics/" + current_user.image_file)
    return render_template('account.html', title='Account', image_file = image_file)
