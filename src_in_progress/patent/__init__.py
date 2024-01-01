from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
import pymysql

pymysql.install_as_MySQLdb()

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = r"mysql://root:Sun135189@127.0.0.1:3306/patent_2022"
app.config['SECRET_KEY'] = 'secret_key'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manage = LoginManager(app)
login_manage.login_view = "login"
login_manage.login_message_category = "info"

from patent import routes
