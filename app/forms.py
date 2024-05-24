from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FileField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
  username = StringField('Username', validators=[DataRequired()])
  password = PasswordField('Password', validators=[DataRequired()])
  # remember_me = BooleanField('Remember Me')
  # submit = SubmitField('Sign In')

class RegisterForm(FlaskForm):
  username = StringField('username', validators=[DataRequired()])
  password1 = PasswordField('password1', validators=[DataRequired()])
  password2 = PasswordField('password2', validators=[DataRequired()])
  docpicker = FileField('docpicker')
  # remember_me = BooleanField('Remember Me')
  # submit = SubmitField('Sign up')


class SettingsForm(FlaskForm):
  username = StringField('username')
  docpicker = FileField('docpicker')
