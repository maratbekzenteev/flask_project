import flask
from pages import blueprint
from data import db_session
from flask_login import LoginManager, login_user
from data.users import User
from forms import SignInForm

app = flask.Flask(__name__)
app.config['SECRET_KEY'] = 'beta-secret-key'

login_manager = LoginManager()
login_manager.init_app(app)

db_session.global_init("db/music.db")


@app.route('/', methods=['GET', 'POST'])
def home():
    if flask.request.method == 'GET':
        return flask.render_template('home.html', title='Домашняя страница')
    elif flask.request.method == 'POST':
        return flask.redirect(location=flask.url_for('search',
                                                     search_title=flask.request.form['search_title']))


@app.route('/search/<string:search_title>')
def search(search_title):
    return flask.render_template('search.html', title='Результаты поиска',
                                 artists=[{'name': 'Beatles'}, {'name': 'AC/DC'}],
                                 songs=[{'title': 'Hey Jude'}, {'title': 'Welcome to the jungle'}],
                                 search_title=search_title)


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    form = SignInForm()
    if form.validate_on_submit():
        print('valid')
        session = db_session.create_session()
        user = session.query(User).filter(User.title == form.title.data)
        if user and user.check_password(form.password.data):
            login_user(user, remember=True)
            return flask.redirect(location='/')
        return flask.render_template('signin.html', title='Войти',
                                     form=form, message='Неверное имя пользователя или пароль')
    return flask.render_template('signin.html', title='Войти', form=form)


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


app.run(host='127.0.0.1')
