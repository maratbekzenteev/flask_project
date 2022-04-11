import flask
from data import db_session
from flask_login import LoginManager, login_user
from data.users import User
from forms import SignInForm, SignUpForm, SearchForm

app = flask.Flask(__name__)
app.config['SECRET_KEY'] = 'beta-secret-key'

login_manager = LoginManager()
login_manager.init_app(app)

db_session.global_init("db/music.db")


@app.route('/', methods=['GET', 'POST'])
def home():
    search_form = SearchForm()
    if search_form.validate_on_submit():
        return flask.redirect(location=flask.url_for('search',
                                                     search_title=search_form.search_title.data,
                                                     search_form=search_form))
    return flask.render_template('home.html', title='Домашняя страница', search_form=search_form)


@app.route('/search/<string:search_title>', methods=['GET', 'POST'])
def search(search_title):
    search_form = SearchForm()
    if search_form.validate_on_submit():
        return flask.redirect(location=flask.url_for('search',
                                                     search_title=search_form.search_title.data,
                                                     search_form=search_form))
    return flask.render_template('search.html', title='Результаты поиска',
                                 artists=[{'name': 'Beatles'}, {'name': 'AC/DC'}],
                                 songs=[{'title': 'Hey Jude'}, {'title': 'Welcome to the jungle'}],
                                 search_title=search_title, search_form=search_form)


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    search_form = SearchForm()
    if search_form.validate_on_submit():
        return flask.redirect(location=flask.url_for('search',
                                                     search_title=search_form.search_title.data,
                                                     search_form=search_form))
    form = SignInForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.title == form.title.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=True)
            return flask.redirect(location='/')
        return flask.render_template('signin.html', title='Войти',
                                     form=form, message='Неверное имя пользователя или пароль',
                                     search_form=search_form)
    return flask.render_template('signin.html', title='Войти', form=form, search_form=search_form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    search_form = SearchForm()
    if search_form.validate_on_submit():
        return flask.redirect(location=flask.url_for('search',
                                                     search_title=search_form.search_title.data,
                                                     search_form=search_form))
    form = SignUpForm()
    if form.validate_on_submit():
        if form.password.data != form.password_2.data:
            return flask.render_template('signup.html', title='Зарегистрироваться',
                                   form=form,
                                   message="Пароли не совпадают",
                                         search_form=search_form)
        session = db_session.create_session()
        if session.query(User).filter(User.title == form.title.data).first():
            return flask.render_template('signup.html', title='Зарегистрироваться',
                                   form=form,
                                   message="Это имя пользователя уже занято",
                                         search_form=search_form)
        user = User(title=form.title.data)
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return flask.redirect('/signin')
    return flask.render_template('signup.html', title='Зарегистрироваться', form=form,
                                 search_form=search_form)


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


app.run(host='127.0.0.1')
