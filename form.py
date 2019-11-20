from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email

csrf = CSRFProtect()

class ContactForm(FlaskForm):
    name = StringField('Meno', validators=[DataRequired('Napíš tvoje meno')])
    email = StringField('E-mail', validators=[DataRequired('E-mail kam chceč, aby sme ti odpovedali'),Email('E-mail musí mať platný formát.')])
    subject = StringField('Predmet', validators=[DataRequired('Predmet')])
    message = TextAreaField('Text správy', validators=[DataRequired('Text správy, ktorú nám chceš poslať.')])
    submit = SubmitField("Poslat")