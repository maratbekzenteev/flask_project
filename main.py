import flask
import flask_login

from data import db_session
from flask_login import LoginManager, login_user
from data.users import User
from data.artists import Artist
from data.songs import Song
from data.genres import Genre
from data.likes import Like
from data.dislikes import Dislike
from forms import SignInForm, SignUpForm, SearchForm, SongSubmitForm, \
    ArtistSubmitForm, GenreSubmitForm, CatalogueForm

app = flask.Flask(__name__)
app.config['SECRET_KEY'] = 'beta-secret-key'

login_manager = LoginManager()
login_manager.init_app(app)

db_session.global_init("db/music.db")


@app.route('/', methods=['GET', 'POST'])
def home():
    search_form = SearchForm()
    if search_form.validate_on_submit():
        return flask.redirect(flask.url_for('search', search_title=search_form.search_title.data))
    return flask.render_template('home.html', title='Домашняя страница', search_form=search_form)


@app.route('/search/<string:search_title>', methods=['GET', 'POST'])
def search(search_title):
    search_form = SearchForm()
    if search_form.validate_on_submit():
        return flask.redirect(flask.url_for('search', search_title=search_form.search_title.data))
    session = db_session.create_session()
    songs = session.query(Song).filter(Song.title.like('%' + search_title + '%')).all()
    artists = session.query(Artist).filter(Artist.title.like('%' + search_title + '%')).all()
    return flask.render_template('search.html', title='Результаты поиска',
                                 artists=artists, songs=songs,
                                 search_title=search_title, search_form=search_form)


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    search_form = SearchForm()
    if search_form.validate_on_submit():
        return flask.redirect(flask.url_for('search', search_title=search_form.search_title.data))
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
        return flask.redirect(flask.url_for('search', search_title=search_form.search_title.data))
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


@app.route('/catalogue', methods=['GET', 'POST'])
def catalogue():
    search_form = SearchForm()
    if search_form.validate_on_submit():
        return flask.redirect(flask.url_for('search', search_title=search_form.search_title.data))
    form = CatalogueForm()
    if form.validate_on_submit():
        return flask.redirect(flask.url_for('catalogue_filter', genre=form.genre.data))
    session = db_session.create_session()
    songs = session.query(Song).all()
    return flask.render_template('catalogue.html', title='Каталог', form=form,
                                 search_form=search_form, songs=songs)


@app.route('/catalogue/<string:genre>', methods=['GET', 'POST'])
def catalogue_filter(genre):
    search_form = SearchForm()
    if search_form.validate_on_submit():
        return flask.redirect(flask.url_for('search', search_title=search_form.search_title.data))
    form = CatalogueForm()
    if form.validate_on_submit():
        return flask.redirect(flask.url_for('catalogue_filter', genre=form.genre.data))
    session = db_session.create_session()
    genre_id = session.query(Genre).filter(Genre.title == genre).first().id
    songs = session.query(Song).filter(Song.genre_id == genre_id).all()
    return flask.render_template('catalogue.html', title='Каталог', form=form,
                                 search_form=search_form, songs=songs)


@app.route('/song-submit', methods=['GET', 'POST'])
def song_submit():
    search_form = SearchForm()
    if search_form.validate_on_submit():
        return flask.redirect(flask.url_for('search', search_title=search_form.search_title.data))
    form = SongSubmitForm()
    if form.validate_on_submit():
        img_name = form.img.data.filename
        wav_name = form.wav.data.filename
        if img_name[img_name.rfind('.'):] not in ['.jpg', '.png', '.gif'] or \
                wav_name[wav_name.rfind('.'):] not in ['.mp3', '.wav', '.ogg']:
            return flask.render_template('song_submit.html', title='Загрузить песню', form=form,
                                         search_form=search_form, message='Неверный формат файлов')
        session = db_session.create_session()
        artist = session.query(Artist).filter(
            Artist.title.like('%' + form.artist.data + '%')).first()
        if not artist:
            return flask.render_template('song_submit.html', title='Загрузить песню', form=form,
                                         search_form=search_form, message='Указанного исполнителя нет в базе')
        genre = session.query(Genre).filter(Genre.title == form.genre.data).first()
        current_id = session.query(Song).order_by(-Song.id).first()
        if not current_id:
            current_id = 1
        else:
            current_id = current_id.id + 1
        form.img.data.save('static/songs_img/' + str(current_id) + img_name[img_name.rfind('.'):])
        form.wav.data.save('static/wav/' + str(current_id) + wav_name[wav_name.rfind('.'):])
        song = Song(
            title=form.title.data,
            artist_id=artist.id,
            genre_id=genre.id,
            user_id=flask_login.current_user.id,
            img_name=str(current_id) + img_name[img_name.rfind('.'):],
            wav_name=str(current_id) + wav_name[wav_name.rfind('.'):]
        )
        session.add(song)
        session.commit()
        return flask.redirect('/')
    return flask.render_template('song_submit.html', title='Загрузить песню', form=form,
                          search_form=search_form)


@app.route('/artist-submit', methods=['GET', 'POST'])
def artist_submit():
    search_form = SearchForm()
    if search_form.validate_on_submit():
        return flask.redirect(flask.url_for('search', search_title=search_form.search_title.data))
    form = ArtistSubmitForm()
    if form.validate_on_submit():
        img_name = form.img.data.filename
        if img_name[img_name.rfind('.'):] not in ['.jpg', '.png', '.gif']:
            return flask.render_template("artist_submit.html", title='Добавить исполнителя',
                                         form=form, search_form=search_form,
                                         message='Неверный формат файла')
        session = db_session.create_session()
        artist = session.query(Artist).filter(Artist.title == form.title.data).first()
        if artist:
            return flask.render_template("artist_submit.html", title='Добавить исполнителя',
                                         form=form, search_form=search_form,
                                         message='Такой исполнитель уже есть в базе')
        current_id = session.query(Artist).order_by(-Artist.id).first()
        if not current_id:
            current_id = 1
        else:
            current_id = current_id.id + 1
        form.img.data.save('static/artists_img/' + str(current_id) + img_name[img_name.rfind('.'):])
        artist = Artist(
            title=form.title.data,
            img_name=str(current_id) + img_name[img_name.rfind('.'):]
        )
        session.add(artist)
        session.commit()
        return flask.redirect('/')
    return flask.render_template("artist_submit.html", title='Добавить исполнителя',
                                 form=form, search_form=search_form)


@app.route('/genre-submit', methods=['GET', 'POST'])
def genre_submit():
    search_form = SearchForm()
    if search_form.validate_on_submit():
        return flask.redirect(flask.url_for('search', search_title=search_form.search_title.data))
    form = GenreSubmitForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        genre = session.query(Genre).filter(Genre.title == form.title.data.lower()).first()
        if genre:
            return flask.render_template("genre_submit.html", title='Добавить жанр',
                                         form=form, search_form=search_form,
                                         message='Такой жанр уже есть')
        genre = Genre(title=form.title.data.lower())
        session.add(genre)
        session.commit()
        return flask.redirect('/')
    return flask.render_template("genre_submit.html", title='Добавить жанр',
                                 form=form, search_form=search_form)


@app.route('/song/<int:song_id>')
def song_page(song_id):
    search_form = SearchForm()
    if search_form.validate_on_submit():
        return flask.redirect(flask.url_for('search', search_title=search_form.search_title.data))
    session = db_session.create_session()
    song = session.query(Song).filter(Song.id == song_id).first()
    my_like = len(session.query(Like).filter(
        Like.song_id == song_id, Like.user_id == flask_login.current_user.id).all())
    my_dislike = len(session.query(Dislike).filter(
        Dislike.song_id == song_id, Dislike.user_id == flask_login.current_user.id).all())
    likes = len(session.query(Like).filter(Like.song_id == song_id).all())
    dislikes = len(session.query(Dislike).filter(Dislike.song_id == song_id).all())
    img_url = flask.url_for('static', filename='songs_img/' + song.img_name)
    wav_url = flask.url_for('static', filename='wav/' + song.wav_name)
    return flask.render_template("song_page.html", title=song.artist.title + ' - ' + song.title, img_url=img_url,
                                 wav_url=wav_url, song=song, likes=likes, dislikes=dislikes,
                                 search_form=search_form, my_like=my_like, my_dislike=my_dislike)


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


app.run(host='127.0.0.1')
