import flask
from forms import SignInForm
from data import db_session
from data.users import User
from flask_login import login_user, LoginManager

blueprint = flask.Blueprint('pages', __name__, template_folder='templates')


@blueprint.route('/', methods=['GET', 'POST'])
def home():
    if flask.request.method == 'GET':
        return flask.render_template('home.html', title='Домашняя страница')
    elif flask.request.method == 'POST':
        return flask.redirect(location=flask.url_for('pages.search',
                                                     search_title=flask.request.form['search_title']))


@blueprint.route('/search/<string:search_title>')
def search(search_title):
    return flask.render_template('search.html', title='Результаты поиска',
                                 artists=[{'name': 'Beatles'}, {'name': 'AC/DC'}],
                                 songs=[{'title': 'Hey Jude'}, {'title': 'Welcome to the jungle'}],
                                 search_title=search_title)


@blueprint.route('/signin', methods=['GET', 'POST'])
def signin():
    form = SignInForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.title == form.title.data)
        if user and user.check_password(form.password.data):
            login_user(user, remember=True)
            return flask.redirect(location='/')
        return flask.render_template('signin.html', title='Войти',
                                     form=form, message='Неверное имя пользователя или пароль')
    return flask.render_template('signin.html', title='Войти', form=form)
