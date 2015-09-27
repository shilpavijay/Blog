from flask.ext.wtf import Form
from wtforms import StringField,BooleanField
from wtforms.validators import DataRequired

class MainForm(Form):
    openid = StringField('openid', validators = [DataRequired()])
   # remem = BooleanField('Remember_me',default=False)
