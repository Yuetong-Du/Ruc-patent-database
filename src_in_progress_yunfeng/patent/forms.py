from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, \
    SelectField, TextAreaField, FloatField, IntegerField
from wtforms.validators import DataRequired, EqualTo, ValidationError, Email, InputRequired, Length
from patent.models import Applicant, Visitor, Inspector


class RegistrationForm(FlaskForm):
    role = SelectField("Select role", coerce=str, choices=[("1", "Applicant"), ("2", "Visitor"), ("3", "Inspector")])
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=20)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        if self.role.data == "1":
            table = Applicant
        elif self.role.data == "2":
            table = Visitor
        elif self.role.data == "3":
            table = Inspector
        if table.query.filter_by(email=email.data).first():
            raise ValidationError("Duplicate email")


class LoginForm(FlaskForm):
    role = SelectField("Select role", coerce=str, choices=[("1", "Applicant"), ("2", "Visitor"), ("3", "Inspector")])
    email = StringField('Mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField("Remember me")
    submit = SubmitField('Sign in')


class UpdateInfo(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Mail', validators=[DataRequired(), Email()])
    submit = SubmitField('Update')

    def validate_email(self, email):
        if current_user.table_name == "Applicant":
            table = Applicant
        elif current_user.table_name == "Visitor":
            table = Visitor
        user = table.query.filter_by(email=email.data).first()
        if user and user.username != current_user.username:
            raise ValidationError("Duplicate email")


class UpdatePasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=20)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Update')


class UpdateApplicantForm(FlaskForm):
    affliated_organization = StringField("affliated_organization", validators=[InputRequired(), Length(min=2, max=20)])
    address = StringField("Address", validators=[InputRequired(), Length(min=10, max=40)])
    telephone = StringField("Telephone", validators=[InputRequired(), Length(max=20, min=9)])
    submit = SubmitField("Update")


class UpdateVisitorForm(FlaskForm):
    # address = StringField('address',validators=[InputRequired(),Length(min=5, max=40)])
    telephone = StringField("Telephone", validators=[InputRequired(), Length(max=20, min=9)])
    submit = SubmitField('Update')


class UpdateInspectorForm(FlaskForm):
    # address = StringField('address',validators=[InputRequired(),Length(min=5, max=40)])
    telephone = StringField("Telephone", validators=[InputRequired(), Length(max=20, min=9)])
    submit = SubmitField('Update')


class ProductForm(FlaskForm):
    name = StringField('Product name', validators=[DataRequired(), Length(min=2, max=40)])
    price = FloatField("Product price", validators=[DataRequired()])
    count = IntegerField("Product count", validators=[DataRequired()])
    confirm = IntegerField("Confirm Product count", validators=[DataRequired(), EqualTo("count")])
    submit = SubmitField("Add")


class UpdateProductForm(FlaskForm):
    name = StringField('Product name', validators=[InputRequired(), Length(min=2, max=40)])
    price = FloatField("Product price", validators=[InputRequired()])
    count = IntegerField("Product count", validators=[InputRequired()])
    confirm = IntegerField("Confirm Product count", validators=[InputRequired(), EqualTo("count")])
    submit = SubmitField("Update")


class GApplicationInProgress(FlaskForm):

    d_ipc = SelectField(
        'D-IPC',
        choices=[(0, 0), (1, 1)],
        validators=[DataRequired()]
    )
    ipc_section = StringField(
        'IPC Section (Maximum Length = 32)', 
        validators=[DataRequired(), Length(max=32)]
    )
    patent_type = SelectField(
        'Patent Type', 
        choices=[('utility', 'Utility'), ('design', 'Design'), ('plant', 'Plant'), ('reissue', 'Reissue')],
        validators=[DataRequired()]
    )
    patent_title = TextAreaField(
        'Patent Title', 
        validators=[DataRequired()]
    )
    patent_abstract = TextAreaField(
        'Patent Abstract', 
        validators=[DataRequired()]
    )
    wipo_kind = StringField(
        'WIPO Kind (Maximum Length = 3)', 
        validators=[DataRequired(), Length(max=3)]
    )

    def add_inventor_fields(self, number_of_inventors):
        for i in range(1, number_of_inventors + 1):
            setattr(self, f'inventor_name{i}', StringField(f'Inventor Name {i}'))
            setattr(self, f'male_flag{i}',
                    SelectField(f'Inventor Gender {i}', choices=[('1', 'Male'), ('0', 'Female')]))

    submit = SubmitField("Submit")


class GPatentSearch(FlaskForm):

    d_ipc = SelectField(
        'D-IPC',
        choices=[('NA', 'Both'), (0, 0), (1, 1)],
        validators=[]
    )
    ipc_section = StringField(
        'IPC Section (Maximum Length = 32)', 
        validators=[Length(max=32)]
    )
    patent_type = SelectField(
        'Patent Type', 
        choices=[('NA', 'Any will be fine!'), ('utility', 'utility'), ('design', 'design'),
                 ('plant', 'plant'), ('reissue', 'reissue')],
        validators=[]
    )
    patent_keyword = TextAreaField(
        'Patent Keyword', 
        validators=[]
    )
    patent_abstract_keyword = TextAreaField(
        'Patent Abstract', 
        validators=[]
    )
    wipo_kind = StringField(
        'WIPO Kind (Maximum Length = 3)', 
        validators=[Length(max=3)]
    )
    inventor = StringField(
        'Inventor Name', 
        validators=[Length(max=32)]
    )

    assignee = StringField(
        'Assignee',
        validators=[Length(max=50)]
    )

    country = StringField(
        'Country',
        validators=[Length(max=50)]
    )
    city = StringField(
        'City',
        validators=[Length(max=50)]
    )
    state = StringField(
        'state',
        validators=[Length(max=50)]
    )
    county = StringField(
        'state',
        validators=[Length(max=50)]
    )

    per_page = SelectField(
        'per_page (Default 10)',
        choices=[(10, 10), (20, 20), (30, 30), (50, 50), (100, 100)],
        validators=[]
    )

    submit = SubmitField("Search")