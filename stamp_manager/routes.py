from flask import render_template, flash, redirect, url_for, request
from stamp_manager import app, db, bcrypt
from stamp_manager.forms import RegistrationForm, LoginForm, UpdateAccountForm
from stamp_manager.models import User, Post
from stamp_manager.data import Articles
from flask_login import login_user, current_user, logout_user, login_required
import secrets
import os
from PIL import Image


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

# funtion to save updated picture and return filename as random hex
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename) # get extension from orig file
    picture_fn = random_hex + f_ext # build new filename
    picture_path = os.path.join(app.root_path, 'static/pics', picture_fn) # build new filepath
    output_size=(125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data) # call function above
            current_user.image_file = picture_file # update picture
        current_user.username = form.username.data # update username
        current_user.email = form.email.data # update email
        db.session.commit()
        flash('Account updated', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for('static', filename="pics/" + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)
