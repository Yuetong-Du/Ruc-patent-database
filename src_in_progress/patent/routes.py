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
    return render_template("home.html", patents=first_ten_patents, title = "Home")

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
        elif form.role.data == "3":
            role = Inspector()
            table_name = "Visitor"
            table = Inspector
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
        elif form.role.data == "3":
            table = Inspector
            table_name = "Inspector"
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

@app.route("/<string:patent_id>/detail") # 展示专利详细信息
def patent_detail(patent_id):
    patent_info = GPatent.query.filter_by(patent_number = patent_id).first()
    patent_detail = GInventorGeneral.query.filter_by(patent_number = patent_id).first()
    patent_super_detail = GInventorDetailed.query.filter_by(patent_number = patent_id).first()
    return render_template('patent_detail.html', title='Patent_detail', patent_info = patent_info, patent_detail = patent_detail, super_detail = patent_super_detail)

@app.route("/applicant/<string:username>/account") # asking applicants to fill in detailed info
@login_required
def applicant_account(username):
    if current_user.table_name != "Applicant":
        abort(403)
    Applicant1 = Applicant.query.filter_by(id=current_user.table_id).first()
    if Applicant1.affliated_organization == "null" or Applicant1.address == "null" or Applicant1.telephone == "null":
        flash("Please complete your personal information as soon as possible","warning")
        return redirect(url_for("applicant_detail_manage"))
    return render_template("applicant_account.html", username=username)

@app.route("/visitor/<string:username>/account") # asking visitors to update their detailed info
@login_required
def visitor_account(username):
    if current_user.table_name != "Visitor":
        abort(403)
    visitor1 = Visitor.query.filter_by(id=current_user.table_id).first() # looking for visitor info and set it into an object
    if visitor1.telephone == "null": # if any of the info is not submitted
        flash("Please complete your personal information as soon as possible","warning")
        return redirect(url_for("visitor_detail_manage"))
    return render_template("visitor_account.html", username=username)

@app.route("/inspector/<string:username>/account") # asking visitors to update their detailed info
@login_required
def inspector_account(username):
    if current_user.table_name != "Inspector":
        abort(403)
    insepctor1 = Inspector.query.filter_by(id=current_user.table_id).first() # looking for visitor info and set it into an object
    if insepctor1.telephone == "null": # if any of the info is not submitted
        flash("Please complete your personal information as soon as possible","warning")
        return redirect(url_for("inspector_detail_manage"))
    return render_template("visitor_account.html", username=username)

@app.route("/update/info",methods=["GET","POST"])
@login_required
def update_info():
    if current_user.table_name == "Applicant":
        table = Applicant
    elif current_user.table_name == "Visitor":
        table = Visitor
    elif current_user.table_name == "Inspector":
        table = Inspector
    form = UpdateInfo()
    role = table.query.filter_by(id=current_user.table_id).first()
    if form.validate_on_submit():
        role.username = form.username.data
        role.email = form.email.data
        db.session.add(role)
        db.session.commit()
        user = User.query.filter_by(id=current_user.id).first()
        user.username = form.username.data
        user.email = form.email.data
        db.session.add(user)
        db.session.commit()
        flash('Profile updated successfully', 'success')
        return redirect(url_for("home"))
    if request.method == "GET":
        form.username.data = role.username
        form.email.data = role.email
    return render_template("update_info.html", form=form)

@app.route("/update/password",methods=["GET","POST"])
@login_required
def update_password():
    if current_user.table_name == "Applicant":
        table = Applicant
    elif current_user.table_name == "Visitor":
        table = Visitor
    elif current_user.table_name == "Inspector":
        table = Inspector
    form = UpdatePasswordForm()
    role = table.query.filter_by(id=current_user.table_id).first()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(password=form.password.data).decode("utf-8")
        role.password = hashed_password
        role.confirm_password = form.confirm_password.data
        db.session.add(role)
        db.session.commit()
        flash('Your password has been updated', 'success')
        return redirect(url_for("home"))
    return render_template("update_password.html", form=form)
    

@app.route("/applicant/detail", methods=["POST","GET"])
@login_required
def applicant_detail_manage():
    if current_user.table_name != "Applicant":
        abort(403)
    address = Applicant.query.filter_by(id=current_user.table_id).first()
    form = UpdateApplicantForm()
    if form.validate_on_submit():
        address.affliated_organization = form.affliated_organization.data
        address.address = form.address.data
        address.telephone = form.telephone.data
        db.session.commit()
        flash("Shipping address updated successfully!","success")
    elif request.method =="GET":
        form.affliated_organization.data = address.affliated_organization
        form.address.data = address.address
        form.telephone.data = address.telephone
    return render_template("update_applicant.html",form=form)

@app.route("/visitor/detail",methods=["GET","POST"])
@login_required
def visitor_detail_manage(): # supplier_shipper_manage
    if current_user.table_name != "Visitor":
        abort(403)
    form = UpdateVisitorForm()
    visitor1 = Visitor.query.filter_by(id=current_user.table_id).first() # look for visitor info
    if form.validate_on_submit():
        visitor1.telephone = form.telephone.data
        db.session.add(visitor1)
        db.session.commit()
        flash("Profile updated successfully","success")
    elif request.method == "GET":
        form.telephone.data = visitor1.telephone
    return render_template("update_visitor.html", form=form)

@app.route("/inspector/detail",methods=["GET","POST"])
@login_required
def inspector_detail_manage():
    if current_user.table_name != "Inspector":
        abort(403)
    form = UpdateVisitorForm()
    inspector1 = Inspector.query.filter_by(id=current_user.table_id).first() # look for visitor info
    if form.validate_on_submit():
        inspector1.telephone = form.telephone.data
        db.session.add(inspector1)
        db.session.commit()
        flash("Profile updated successfully","success")
    elif request.method == "GET":
        form.telephone.data = inspector1.telephone
    return render_template("update_visitor.html", form=form)
