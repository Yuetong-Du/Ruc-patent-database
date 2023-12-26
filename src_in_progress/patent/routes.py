from patent import app, db, bcrypt
from patent.forms import *
from patent.models import *
from flask import render_template, url_for, request, redirect, flash, abort
from flask_login import current_user, logout_user, login_user, login_required
from datetime import datetime


@app.route('/')
@app.route("/home") # home page
def home():
    first_ten_patents = GPatent.query.limit(10).all()
    return render_template("home.html", patents=first_ten_patents)

@app.route("/register",methods=["GET", 'POST']) # register
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if form.role.data == "1":
            role = Applicant()
            table_name = "Applicant"
            table = Applicant
        elif form.role.data == "2":
            role = Visitor()
            table_name = "Visitor"
            table = Visitor
        hashed_password = bcrypt.generate_password_hash(password=form.password.data).decode("utf-8")
        role.username = form.username.data
        role.email = form.email.data
        role.password = hashed_password
        db.session.add(role)
        db.session.commit()
        user = User()
        user.table_name = table_name
        user.table_id = table.query.filter_by(email=form.email.data).first().id
        user.username=form.username.data
        user.email=form.email.data
        db.session.add(user)
        db.session.commit()
        flash('Your account was created successfully', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login",methods=["GET",'POST']) # login
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        if form.role.data == "1":
            table = Applicant
            table_name="Applicant"
        elif form.role.data == "2":
            table = Visitor
            table_name = "Visitor"
        user = table.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            table_id = user.id
            user_user = User.query.filter_by(table_id=table_id,table_name=table_name).first()
            login_user(user_user,remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash('Login failed, please check your character name, email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout") # logout
def logout():
    logout_user()
    return redirect(url_for('home'))
