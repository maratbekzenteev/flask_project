from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, SelectField
from wtforms.validators import DataRequired
from data import db_session
from data.genres import Genre

db_session.global_init("db/music.db")


# форма поисковой строки в topnav
class SearchForm(FlaskForm):
    search_title = StringField('', validators=[DataRequired()])
    submit = SubmitField('>')


# форма авторизации
class SignInForm(FlaskForm):
    title = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')


# форма регистрации
class SignUpForm(FlaskForm):
    title = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_2 = PasswordField('Повторите пароль', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')


# форма загрузки песни
class SongSubmitForm(FlaskForm):
    title = StringField('Название песни', validators=[DataRequired()])
    artist = StringField('Исполнитель', validators=[DataRequired()])
    session = db_session.create_session()
    genres = session.query(Genre).all()
    genre = SelectField('Жанр', choices=[i.title for i in genres], validators=[DataRequired()])
    img = FileField('Обложка песни', validators=[DataRequired()])
    wav = FileField('Аудиодорожка', validators=[DataRequired()])
    submit = SubmitField('Загрузить')


# форма добавления исполнителя
class ArtistSubmitForm(FlaskForm):
    title = StringField('Название исполнителя', validators=[DataRequired()])
    img = FileField('Фото исполнителя', validators=[DataRequired()])
    submit = SubmitField('Добавить')


# форма добавления жанра
class GenreSubmitForm(FlaskForm):
    title = StringField('Название жанра', validators=[DataRequired()])
    submit = SubmitField('Добавить')


# форма для фильтрации песен по жанру в каталоге
class CatalogueForm(FlaskForm):
    session = db_session.create_session()
    genres = session.query(Genre).all()
    genre = SelectField('Жанр', choices=([''] + [i.title for i in genres]), validators=[DataRequired()])
    submit = SubmitField('Обновить')
