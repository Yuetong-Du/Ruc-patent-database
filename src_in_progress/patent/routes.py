from patent import app, db, bcrypt
from patent.forms import *
from patent.models import *
from flask import render_template, url_for, request, redirect, flash, abort
from flask_login import current_user, logout_user, login_user, login_required
from datetime import datetime
from sqlalchemy import or_, and_
from flask import session
from sqlalchemy import func
from flask_paginate import get_page_parameter, Pagination


@app.route('/')
@app.route("/home")  # home page
def home():
    patents = GPatent.query.all()

    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = 20
    pagination = Pagination(page=page, per_page=per_page, total=len(patents), css_framework='bootstrap4')

    start = (page - 1) * per_page
    end = start + per_page
    patents = patents[start:end]

    return render_template("home.html", patents=patents, pagination=pagination, title="Home")


@app.route("/dashboard")
def dashboard():
    results = (db.session.query(GLocation.country, func.count(GLocation.patent_number).label('number'))
               .group_by(GLocation.country)
               .order_by(func.count(GLocation.patent_number).desc())
               .limit(8).all())
    return render_template("dashboard.html", result_left1=results, title="Dashboard")


@app.route("/register", methods=["GET", 'POST'])  # register
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
            table_name = "Inspector"
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
        user.username = form.username.data
        user.email = form.email.data
        db.session.add(user)
        db.session.commit()
        flash('Your account was created successfully', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=["GET", 'POST'])  # login
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        if form.role.data == "1":
            table = Applicant
            table_name = "Applicant"
        elif form.role.data == "2":
            table = Visitor
            table_name = "Visitor"
        elif form.role.data == "3":
            table = Inspector
            table_name = "Inspector"
        user = table.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            table_id = user.id
            user_user = User.query.filter_by(table_id=table_id, table_name=table_name).first()
            login_user(user_user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash('Login failed, please check your character name, email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")  # logout
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/<string:patent_id>/detail")  # 展示专利详细信息
def patent_detail(patent_id):
    patent_info = GPatent.query.filter_by(patent_number=patent_id).first()
    patent_detail = GInventorGeneral.query.filter_by(patent_number=patent_id).first()
    patent_super_detail = GInventorDetailed.query.filter_by(patent_number=patent_id).first()
    return render_template('patent_detail.html', title='Patent_detail', patent_info=patent_info,
                           patent_detail=patent_detail, super_detail=patent_super_detail)


@app.route("/applicant/<string:username>/account")  # asking applicants to fill in detailed info
@login_required
def applicant_account(username):
    if current_user.table_name != "Applicant":
        abort(403)
    Applicant1 = Applicant.query.filter_by(id=current_user.table_id).first()
    if Applicant1.affliated_organization == "null" or Applicant1.address == "null" or Applicant1.telephone == "null":
        flash("Please complete your personal information as soon as possible", "warning")
        return redirect(url_for("applicant_detail_manage"))
    return render_template("applicant_account.html", username=username)


@app.route("/visitor/<string:username>/account")  # asking visitors to update their detailed info
@login_required
def visitor_account(username):
    if current_user.table_name != "Visitor":
        abort(403)
    visitor1 = Visitor.query.filter_by(id=current_user.table_id).first()
    # looking for visitor info and set it into an object

    if visitor1.telephone == "null":  # if any of the info is not submitted
        flash("Please complete your personal information as soon as possible", "warning")
        return redirect(url_for("visitor_detail_manage"))
    return render_template("visitor_account.html", username=username)


@app.route("/inspector/<string:username>/account")  # asking visitors to update their detailed info
@login_required
def inspector_account(username):
    if current_user.table_name != "Inspector":
        abort(403)
    insepctor1 = Inspector.query.filter_by(id=current_user.table_id).first()
    # looking for visitor info and set it into an object

    if insepctor1.telephone == "null":  # if any of the info is not submitted
        flash("Please complete your personal information as soon as possible", "warning")
        return redirect(url_for("inspector_detail_manage"))
    return render_template("inspector_account.html", username=username)


@app.route("/update/info", methods=["GET", "POST"])
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


@app.route("/update/password", methods=["GET", "POST"])
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
    

@app.route("/applicant/detail", methods=["POST", "GET"])
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
        flash("Shipping address updated successfully!", "success")
    elif request.method == "GET":
        form.affliated_organization.data = address.affliated_organization
        form.address.data = address.address
        form.telephone.data = address.telephone
    return render_template("update_applicant.html", form=form)


@app.route("/visitor/detail", methods=["GET", "POST"])
@login_required
def visitor_detail_manage():  # supplier_shipper_manage
    if current_user.table_name != "Visitor":
        abort(403)
    form = UpdateVisitorForm()
    visitor1 = Visitor.query.filter_by(id=current_user.table_id).first()  # look for visitor info
    if form.validate_on_submit():
        visitor1.telephone = form.telephone.data
        db.session.add(visitor1)
        db.session.commit()
        flash("Profile updated successfully", "success")
    elif request.method == "GET":
        form.telephone.data = visitor1.telephone
    return render_template("update_visitor.html", form=form)


@app.route("/inspector/detail", methods=["GET", "POST"])
@login_required
def inspector_detail_manage():
    if current_user.table_name != "Inspector":
        abort(403)
    form = UpdateInspectorForm()
    inspector1 = Inspector.query.filter_by(id=current_user.table_id).first()  # look for visitor info
    if form.validate_on_submit():
        inspector1.telephone = form.telephone.data
        db.session.add(inspector1)
        db.session.commit()
        flash("Profile updated successfully", "success")
    elif request.method == "GET":
        form.telephone.data = inspector1.telephone
    return render_template("update_inspector.html", form=form)


@app.route("/applicant/apply", methods=["GET", "POST"])
@login_required
def applicant_apply():
    if current_user.table_name != "Applicant":
        abort(403)
    inventor_count = sum(1 for key in request.form.keys() if key.startswith('inventor_name'))
    form = GApplicationInProgress()
    form.add_inventor_fields(inventor_count)
    if form.validate_on_submit():
        patent_application = GApplication(applicant_id=current_user.table_id)
        patent_application.d_ipc = form.d_ipc.data
        patent_application.ipc_section = form.ipc_section.data
        patent_application.patent_title = form.patent_title.data
        patent_application.patent_abstract = form.patent_abstract.data
        patent_application.wipo_kind = form.wipo_kind.data
        patent_application.patent_application_date = datetime.now()
        patent_application.patent_type = form.patent_type.data
        patent_application.status = 1
        inventor_count = sum(1 for key in request.form.keys() if key.startswith('inventor_name'))

        for i in range(1, inventor_count + 1):  # 从 1 开始，直到 inventor_count
            inventor_name = request.form.get(f'inventor_name{i}')
            inventor_gender = request.form.get(f'male_flag{i}')
            if inventor_name:
                setattr(patent_application, f'inventor_name{i}', inventor_name)
                setattr(patent_application, f'male_flag{i}', int(inventor_gender))

        db.session.add(patent_application)
        try:
            db.session.commit()
            flash("Application submitted successfully", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred: {e}", "danger")

        # flash("Application submitted successfully","success")
        return redirect(url_for('home'))
    return render_template("applicant_apply.html", form=form)


@app.route("/applicant/application_manage")
@login_required
def applicant_application_manage():  # customer_order_manage
    if current_user.table_name != "Applicant":
        abort(403)
    pending_patents = GApplication.query.filter_by(applicant_id=current_user.table_id, status=1).all()
    rejected_patents = GApplication.query.filter_by(applicant_id=current_user.table_id, status=2).all()
    approved_patents = GApplication.query.filter_by(applicant_id=current_user.table_id, status=3).all()
    return render_template("applicant_patent_in_progress_manage.html", pending=pending_patents,
                           rejected=rejected_patents, approved=approved_patents)


@app.route("/applicant/application_detail/<int:application_table_id>")
@login_required
def application_detail(application_table_id):
    if current_user.table_name != "Applicant":
        abort(403)
    application_info = GApplication.query.filter_by(table_number=application_table_id).first()
    return render_template('application_detail.html', title='Application_detail', info=application_info)


@app.route("/search", methods=["GET", "POST"])
@login_required
def patent_search():
    form = GPatentSearch()  # 假设您已经创建了这个表单类
    if form.validate_on_submit():
        # 存储搜索参数到会话中
        session['search_params'] = {
            'patent_keyword': form.patent_keyword.data,
            'patent_abstract_keyword': form.patent_abstract_keyword.data,
            'ipc_section': form.ipc_section.data,
            'patent_type': form.patent_type.data,
            'd_ipc': form.d_ipc.data,
            'wipo_kind': form.wipo_kind.data,
            'inventor': form.inventor.data,
            'per_page': form.per_page.data
        }

        # 重定向到结果显示视图
        return redirect(url_for('search_results'))

    return render_template('search_page.html', title='Search', form=form)


@app.route("/search_result", methods=["GET", "POST"])
@login_required
def search_results():
    search_params = session.get('search_params', {})
    query = GPatent.query
    conditions = []

    # 构建基于用户输入的搜索条件
    if search_params.get('patent_keyword'):
        conditions.append(GPatent.patent_title.like(f'%{search_params["patent_keyword"]}%'))
    if search_params.get('patent_abstract_keyword'):
        conditions.append(GPatent.patent_abstract.like(f'%{search_params["patent_abstract_keyword"]}%'))
    if search_params.get('ipc_section'):
        conditions.append(GPatent.ipc_section.like(f'%{search_params["ipc_section"]}%'))
    if search_params.get('patent_type') and search_params['patent_type'] != "NA":
        conditions.append(GPatent.patent_type == search_params['patent_type'])
    if search_params.get('d_ipc') and search_params['d_ipc'] != "NA":
        conditions.append(GPatent.d_ipc == search_params['d_ipc'])
    if search_params.get('wipo_kind'):
        conditions.append(GPatent.wipo_kind == search_params['wipo_kind'])

    # 应用普通搜索条件
    if conditions:
        query = query.filter(and_(*conditions))
        # query.patent_title = query.patent_title.replace(keyword, Fore.RED + keyword)

    # 构建发明家搜索条件并应用
    inventor_conditions = []
    if search_params.get('inventor'):
        inventor_conditions.extend([
            GInventorDetailed.inventor_name1.like(f'%{search_params["inventor"]}%'),
            GInventorDetailed.inventor_name2.like(f'%{search_params["inventor"]}%'),
            GInventorDetailed.inventor_name3.like(f'%{search_params["inventor"]}%'),
            GInventorDetailed.inventor_name4.like(f'%{search_params["inventor"]}%'),
            GInventorDetailed.inventor_name5.like(f'%{search_params["inventor"]}%'),
            GInventorDetailed.inventor_name6.like(f'%{search_params["inventor"]}%'),
            GInventorDetailed.inventor_name7.like(f'%{search_params["inventor"]}%'),
            GInventorDetailed.inventor_name8.like(f'%{search_params["inventor"]}%'),
            GInventorDetailed.inventor_name9.like(f'%{search_params["inventor"]}%')
        ])
        if inventor_conditions:
            query = query.join(GInventorDetailed, GPatent.patent_number == GInventorDetailed.patent_number)
            query = query.filter(or_(*inventor_conditions))

    results = query.all()
    num = len(results)
    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = search_params.get('per_page')
    per_page = int(per_page)
    pagination = Pagination(page=page, per_page=per_page, total=len(results), css_framework='bootstrap4')

    start = (page - 1) * per_page
    end = start + per_page
    results = results[start:end]
    return render_template('search_result.html', title='Search Result', number=num, pagination=pagination,
                           result=results, keyword=search_params["patent_keyword"])


@app.route("/cite/<id>")
@login_required
def cite():
    patent = GPatent.query.filter_by(patent_number=id).first()
    if patent:
        patent.num_claims = patent.num_claims + 1 if patent.num_claims else 1
        db.session.add(patent)
        db.session.commit()
        flash("Claimed Successfully!", "success")
    else:
        flash("Patent not found.", "danger")

    return redirect(url_for("home"))


@app.route("/cite/<id>")
@login_required
def inspector_process_applications():

    return redirect(url_for("home"))
