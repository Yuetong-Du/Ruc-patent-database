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
    if current_user.is_authenticated:
        statement = current_user.username
    else:
        statement = "please sign in first"
    return render_template("home.html", statement=statement, user_num=len(User.query.all()),
                           patent_num=178233, title="Home")


@app.route("/dashboard")
def dashboard():
    result_left1 = (db.session.query(GLocation.country, func.count(GLocation.patent_number).label('number'))
                .filter(GLocation.country != '')  # 过滤掉国家名称为空的记录
                .group_by(GLocation.country)
                .order_by(func.count(GLocation.patent_number).desc())
                .limit(8)
                .all())

    
    result_left2 = (db.session.query(GPatent.ipc_section, func.count(GPatent.ipc_section).label('number'))
                    .filter(GPatent.ipc_section != '')
                    .group_by(GPatent.ipc_section)
                    .order_by(func.count(GPatent.ipc_section).desc())
                    .limit(8).all())
    
    result_middle1 = (db.session.query(func.count(GPatent.patent_number).label('Patent_num')))

    result_middle1a =(db.session.query(func.count(Applicant.id).label('Aid')))

    result_middle1b =(db.session.query(func.count(User.id).label('Uid')))

    result_middle1c =(db.session.query(func.count(Visitor.id).label('Vid')))

    result_middle1d =(db.session.query(func.count(Inspector.id).label('Iid')))

    result_middle1e =(db.session.query(func.count(GApplicationInProgress.table_number).label('Appid')))

    result_middle2 = (db.session.query(GApplication.application_year,func.count(GApplication.application_year).label('number'))
                .group_by(GApplication.application_year)
                .order_by(GApplication.application_year.asc())
                .all())
    
    result_right1 = (db.session.query(InventorAlert.inventors,func.count(InventorAlert.inventors).label('number'))
                     .group_by(InventorAlert.inventors)
                     .order_by(InventorAlert.inventors).all())
    
    result_right2 = (db.session.query(GPatent.num_claims,func.count(GPatent.num_claims).label('number'))
                     .group_by(GPatent.num_claims)
                     .order_by(GPatent.num_claims.asc())
                     .all())
    
    return render_template("dashboard.html", 
                           result_left1=result_left1,
                           result_left2 =result_left2,
                           result_middle1=result_middle1,
                           result_middle1a=result_middle1a,
                           result_middle1b=result_middle1b,
                           result_middle1c=result_middle1c,
                           result_middle2=result_middle2,
                           result_right1=result_right1,
                           result_right2=result_right2, 
                           result_middle1d = result_middle1d,
                           result_middle1e= result_middle1e,
                           title="Dashboard")




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
    form = GApplicationInProgress_form()
    form.add_inventor_fields(inventor_count)
    if form.validate_on_submit():
        patent_application = GApplicationInProgress(applicant_id=current_user.table_id)
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
    pending_patents = GApplicationInProgress.query.filter_by(applicant_id=current_user.table_id, status=1).all()
    rejected_patents = GApplicationInProgress.query.filter_by(applicant_id=current_user.table_id, status=2).all()
    approved_patents = GApplicationInProgress.query.filter_by(applicant_id=current_user.table_id, status=3).all()
    return render_template("applicant_patent_in_progress_manage.html", pending=pending_patents,
                           rejected=rejected_patents, approved=approved_patents)


@app.route("/applicant/application_detail/<int:application_table_id>")
@login_required
def application_detail(application_table_id):
    if current_user.table_name != "Applicant" and current_user.table_name != "Inspector":
        abort(403)
    application_info = GApplicationInProgress.query.filter_by(table_number=application_table_id).first()
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
    if search_params.get('claims_least'):
        conditions.append(GPatent.num_claims >= search_params['claims_least'])


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

    # 构建assignee搜索条件并应用
    assignee_conditions = []
    if search_params.get('assignee'):
        assignee_conditions.extend([
            GAssignee.assignee.like(f'%{search_params["assignee"]}%')
        ])
        if assignee_conditions:
            query = query.join(GAssignee, GPatent.patent_number == GAssignee.patent_number)
            query = query.filter(and_(*assignee_conditions))

    location = []
    if search_params.get('country'):
        location.extend([
            GLocation.country.like(f'%{search_params["country"]}%')
        ])
    if search_params.get('state'):
        location.extend([
            GLocation.state.like(f'%{search_params["state"]}%')
        ])
    if search_params.get('city'):
        location.extend([
            GLocation.city.like(f'%{search_params["city"]}%')
    ])
    if search_params.get('county'):
        location.extend([
            GLocation.county.like(f'%{search_params["county"]}%')
    ])
    if location:
        query = query.join(GLocation, GPatent.patent_number == GLocation.patent_number)
        query = query.filter(and_(*location))

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
def cite(id):
    patent = GPatent.query.filter_by(patent_number=id).first()
    if patent:
        patent.num_claims = patent.num_claims + 1 if patent.num_claims else 1
        db.session.add(patent)
        db.session.commit()
        flash("Claimed Successfully!", "success")
    else:
        flash("Patent not found.", "danger")

    return redirect(url_for("home"))


@app.route("/inspector/process")
@login_required
def inspector_process_applications():
    if current_user.table_name != "Inspector":
        abort(403)
    pending_patents = GApplication.query.filter_by(status=1).all()
    return render_template("applicant_patent_in_progress_manage.html", pending=pending_patents)



@app.route("/inspector/process/approve/<application_id>")
@login_required
def inspector_approve(application_id):
    if current_user.table_name != "Inspector":
        abort(403)
        # 获取当前年份
    current_year = datetime.now().year
    current_time = datetime.now()
    formatted_date = current_time.date().strftime("%Y-%m-%d")

    pending_patents =GApplicationInProgress.query.filter_by(table_number = application_id).first()
    pending_patents.status = 3
    db.session.add(pending_patents)
    db.session.commit()
    approved_patent = GPatent()
    approved_patent.patent_number = f"{formatted_date}/{pending_patents.table_number}"
    approved_patent.d_ipc = pending_patents.d_ipc
    approved_patent.ipc_section = pending_patents.ipc_section
    # 设置application_number为当前年份和table_id的组合
    approved_patent.application_number = f"{current_year}/{pending_patents.table_number}"
    approved_patent.patent_type = pending_patents.patent_type
    approved_patent.patent_date = formatted_date
    approved_patent.patent_title = pending_patents.patent_title
    approved_patent.patent_abstract = pending_patents.patent_abstract
    approved_patent.wipo_kind = pending_patents.wipo_kind
    approved_patent.num_claims = 0
    db.session.add(approved_patent)
    db.session.commit()

    inventor = GInventorGeneral()
    inventor_names = [pending_patents.inventor_name1, pending_patents.inventor_name2, pending_patents.inventor_name3, 
                      pending_patents.inventor_name4, pending_patents.inventor_name5, pending_patents.inventor_name6, 
                      pending_patents.inventor_name7, pending_patents.inventor_name8, pending_patents.inventor_name9]
    teamsize = sum(1 for name in inventor_names if name)
    inventor.patent_number = f"{formatted_date}/{pending_patents.table_number}"
    inventor.team_size = teamsize
    genders = [pending_patents.male_flag1, pending_patents.male_flag2, pending_patents.male_flag3, 
            pending_patents.male_flag4, pending_patents.male_flag5, pending_patents.male_flag6, 
            pending_patents.male_flag7, pending_patents.male_flag8, pending_patents.male_flag9]
   
    men_inventors = sum(1 for gender in genders if gender!=0)
    women_inventors = teamsize-men_inventors
    inventor.inventors = teamsize
    inventor.men_inventors = men_inventors
    inventor.women_inventors = women_inventors
    db.session.add(inventor)
    db.session.commit()

    inventordetail = GInventorDetailed()
    inventordetail.patent_number = f"{formatted_date}/{pending_patents.table_number}"
    inventordetail.inventor_name1 = pending_patents.inventor_name1
    inventordetail.inventor_name2 = pending_patents.inventor_name2
    inventordetail.inventor_name3 = pending_patents.inventor_name3
    inventordetail.inventor_name4 = pending_patents.inventor_name4
    inventordetail.inventor_name5 = pending_patents.inventor_name5
    inventordetail.inventor_name6 = pending_patents.inventor_name6
    inventordetail.inventor_name7 = pending_patents.inventor_name7
    inventordetail.inventor_name8 = pending_patents.inventor_name8
    inventordetail.inventor_name9 = pending_patents.inventor_name9
    inventordetail.male_flag1 = pending_patents.male_flag1
    inventordetail.male_flag2 = pending_patents.male_flag2
    inventordetail.male_flag3 = pending_patents.male_flag3
    inventordetail.male_flag4 = pending_patents.male_flag4
    inventordetail.male_flag5 = pending_patents.male_flag5
    inventordetail.male_flag6 = pending_patents.male_flag6
    inventordetail.male_flag7 = pending_patents.male_flag7
    inventordetail.male_flag8 = pending_patents.male_flag8
    inventordetail.male_flag9 = pending_patents.male_flag9
    db.session.add(inventordetail)
    db.session.commit()

    pending_patents = GApplicationInProgress.query.filter_by(status=1).all()
    return render_template("applicant_patent_in_progress_manage.html", pending=pending_patents)

@app.route("/inspector/process/reject/<application_id>")
def inspector_reject(application_id):
    pending_patents = GApplicationInProgress.query.filter_by(table_number = application_id).first()
    pending_patents.status = 2
    db.session.add(pending_patents)
    db.session.commit()

    pending_patents = GApplicationInProgress.query.filter_by(status=1).all()
    return render_template("applicant_patent_in_progress_manage.html", pending=pending_patents)

