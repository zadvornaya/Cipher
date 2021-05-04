from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length


class PostCreateForm(FlaskForm):
    id = HiddenField('ID')
    name = StringField('Название', validators=[DataRequired(), Length(min=1, max=64)])
    text = TextAreaField('Текст', validators=[DataRequired(), Length(min=1, max=1024)])
    level = BooleanField('Только для преподавателей')  # Создание записи с уровнем секретности 1 (для преподавателей)
    submit = SubmitField('Добавить')


class PostEditForm(FlaskForm):
    id = HiddenField('ID')
    name = StringField('Название', validators=[DataRequired(), Length(min=1, max=64)])
    text = TextAreaField('Текст', validators=[DataRequired(), Length(min=1, max=1024)])
    submit = SubmitField('Изменить')
