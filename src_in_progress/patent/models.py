from datetime import datetime
from patent import db, login_manage
from flask_login import UserMixin


@login_manage.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model,UserMixin):
    __tablename__="User"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=False, nullable=False,default="私密")
    email = db.Column(db.String(120), unique=True, nullable=False)
    table_name = db.Column(db.String(20), unique=False, nullable=False)
    table_id = db.Column(db.Integer,nullable=False)


class Applicant(db.Model,UserMixin):
    __tablename__ = "Applicant"
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20),unique=False,nullable=False)
    email = db.Column(db.String(120),unique=True,nullable=False)
    password = db.Column(db.String(60),nullable=False)
    affliated_organization = db.Column(db.String(20),nullable=False,default="null")
    address = db.Column(db.String(40),nullable=False,default="null")
    telephone = db.Column(db.String(20),nullable=False,default="null")
    # orders = db.relationship("Order",backref="Applicant",lazy=True)


class Visitor(db.Model,UserMixin):
    __tablename__ = "Visitor"
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20),unique=False,nullable=False)
    email = db.Column(db.String(120),unique=True,nullable=False)
    password = db.Column(db.String(60),nullable=False)
    telephone = db.Column(db.String(20),nullable=False,default="null")
    # products = db.relationship("Product",backref="supplier",lazy=True)

class Inspector(db.Model,UserMixin):
    __tablename__ = "Inspector"
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20),unique=False,nullable=False)
    email = db.Column(db.String(120),unique=True,nullable=False)
    password = db.Column(db.String(60),nullable=False)
    telephone = db.Column(db.String(20),nullable=False,default="null")
    # products = db.relationship("Product",backref="supplier",lazy=True)


class GPatent(db.Model):
    __tablename__ = "g_patent"
    patent_number = db.Column(db.String(20), primary_key=True)
    d_ipc = db.Column(db.Integer, db.CheckConstraint('d_ipc = 0 or d_ipc = 1'))
    ipc_section = db.Column(db.String(32))
    application_number = db.Column(db.String(36))
    patent_type = db.Column(db.String(10), db.CheckConstraint("patent_type IN ('utility', 'design', 'plant', 'reissue')"))
    patent_date = db.Column(db.DateTime)
    patent_title = db.Column(db.Text)
    patent_abstract = db.Column(db.Text)
    wipo_kind = db.Column(db.String(3))
    num_claims = db.Column(db.Integer)

class GInventorGeneral(db.Model):
    __tablename__ = "g_inventor_general"
    patent_number = db.Column(db.String(20), primary_key=True)
    team_size = db.Column(db.Integer)
    inventors = db.Column(db.Integer)
    men_inventors = db.Column(db.Integer)
    women_inventors = db.Column(db.Integer)
    d_inventor = db.Column(db.Integer, db.CheckConstraint('inventors = men_inventors + women_inventors and team_size >= inventors', name='inventor_num'))

class GInventorDetailed(db.Model):
    __tablename__ = "g_inventor_detailed"
    patent_number = db.Column(db.String(20), primary_key=True)
    inventor_id1 = db.Column(db.String(128))
    male_flag1 = db.Column(db.Integer)
    inventor_name1 = db.Column(db.String(128))
    inventor_id2 = db.Column(db.String(128))
    male_flag2 = db.Column(db.Integer)
    inventor_name2 = db.Column(db.String(128))
    inventor_id3 = db.Column(db.String(128))
    male_flag3 = db.Column(db.Integer)
    inventor_name3 = db.Column(db.String(128))
    inventor_id4 = db.Column(db.String(128))
    male_flag4 = db.Column(db.Integer)
    inventor_name4 = db.Column(db.String(128))
    inventor_id5 = db.Column(db.String(128))
    male_flag5 = db.Column(db.Integer)
    inventor_name5 = db.Column(db.String(128))
    inventor_id6 = db.Column(db.String(128))
    male_flag6 = db.Column(db.Integer)
    inventor_name6 = db.Column(db.String(128))
    inventor_id7 = db.Column(db.String(128))
    male_flag7 = db.Column(db.Integer)
    inventor_name7 = db.Column(db.String(128))
    inventor_id8 = db.Column(db.String(128))
    male_flag8 = db.Column(db.Integer)
    inventor_name8 = db.Column(db.String(128))
    inventor_id9 = db.Column(db.String(128))
    male_flag9 = db.Column(db.Integer)
    inventor_name9 = db.Column(db.String(128))

class GApplication(db.Model):
    __tablename__ = "g_application"
    application_number = db.Column(db.String(20), primary_key=True)
    application_year = db.Column(db.Integer)
    patent_number = db.Column(db.String(36), db.ForeignKey('g_patent.patent_number'), nullable=False)
    grant_year = db.Column(db.Integer)
    d_application = db.Column(db.Integer, db.CheckConstraint('d_application = 0 or d_application = 1'))

class GAssignee(db.Model):
    __tablename__ = "g_assignee"
    patent_number = db.Column(db.String(20), primary_key=True)
    d_assignee = db.Column(db.Integer)
    assignee = db.Column(db.String(160))
    assignee_sequence = db.Column(db.Integer)
    assignee_ind = db.Column(db.Integer)

class GLocation(db.Model):
    __tablename__ = "g_location"
    patent_number = db.Column(db.String(20), primary_key=True)
    country = db.Column(db.String(36))
    city = db.Column(db.String(100))
    state = db.Column(db.String(36))
    county = db.Column(db.String(72))
    d_location = db.Column(db.Integer, db.CheckConstraint('d_location = 0 or d_location = 1'))

class InventorAlert(db.Model):
    __tablename__ = "inventor_alert"
    patent_number = db.Column(db.String(20), primary_key=True)
    inventors = db.Column(db.Integer)
    men_inventors = db.Column(db.Integer)
    women_inventors = db.Column(db.Integer)

class AppliDelay(db.Model):
    __tablename__ = "appli_delay"
    application_number = db.Column(db.String(20), primary_key=True)
    patent_number = db.Column(db.String(36), db.ForeignKey('g_patent.patent_number'), nullable=False)
    application_year = db.Column(db.Integer)
    grant_year = db.Column(db.Integer)

class BeyondInventor(db.Model):
    __tablename__ = "beyond_inventor"
    patent_number = db.Column(db.String(20), primary_key=True)
    not_inventors = db.Column(db.Integer)
    inventors = db.Column(db.Integer)


import json
class GApplication(db.Model):
    __tablename__ = "g_application_in_progress"
    applicant_id = db.Column(db.Integer)
    table_number = db.Column(db.Integer,primary_key=True, autoincrement=True)
    d_ipc = db.Column(db.Integer, db.CheckConstraint('d_ipc = 0 or d_ipc = 1'))
    ipc_section = db.Column(db.String(32))
    patent_type = db.Column(db.String(10), db.CheckConstraint("patent_type IN ('utility', 'design', 'plant', 'reissue')"))
    patent_application_date = db.Column(db.DateTime)
    patent_title = db.Column(db.Text)
    patent_abstract = db.Column(db.Text)
    wipo_kind = db.Column(db.String(3))
    status = db.Column(db.Integer)
    male_flag1 = db.Column(db.Integer)
    inventor_name1 = db.Column(db.String(128))
    male_flag2 = db.Column(db.Integer)
    inventor_name2 = db.Column(db.String(128))
    male_flag3 = db.Column(db.Integer)
    inventor_name3 = db.Column(db.String(128))
    male_flag4 = db.Column(db.Integer)
    inventor_name4 = db.Column(db.String(128))
    male_flag5 = db.Column(db.Integer)
    inventor_name5 = db.Column(db.String(128))
    male_flag6 = db.Column(db.Integer)
    inventor_name6 = db.Column(db.String(128))
    male_flag7 = db.Column(db.Integer)
    inventor_name7 = db.Column(db.String(128))
    male_flag8 = db.Column(db.Integer)
    inventor_name8 = db.Column(db.String(128))
    male_flag9 = db.Column(db.Integer)
    inventor_name9 = db.Column(db.String(128))