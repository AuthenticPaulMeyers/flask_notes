from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, SubmitField, SelectField
from wtforms.validators import Length, DataRequired, ValidationError, Email, EqualTo

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()], render_kw={"placeholder": "Username"})
    password = PasswordField("Password", validators=[DataRequired()], render_kw={"placeholder": "Password"})
    submit = SubmitField("Log In")

class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()], render_kw={"placeholder": "Username"})
    email = StringField("Email", validators=[DataRequired(), Email()], render_kw={"placeholder": "Email"})
    password = PasswordField("Password", validators=[DataRequired()], render_kw={"placeholder": "Create password"})
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo('password')], render_kw={"placeholder": "Confirm password"})
    submit = SubmitField("Register")


class NotesForm(FlaskForm):
    category = SelectField("Select category", choices=[('School', 'School'), ('Church', 'Church'), ('Personal','Personal'), ('Other', 'Other')], default='Other')
    title = StringField("Title", validators=[DataRequired()], render_kw={"placeholder": "Title"})
    content = TextAreaField("Content", validators=[Length(min=0, max=160)], render_kw={"placeholder": "Write notes here"})
    submit = SubmitField("Save")