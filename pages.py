import flask

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
