import sqlalchemy
from sqlalchemy import orm
from db_session import SqlAlchemyBase


class Song(SqlAlchemyBase):
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String)
    artist_id = sqlalchemy.Column(sqlalchemy.Integer)
    genre_id = sqlalchemy.Column(sqlalchemy.Integer)
    user_id = sqlalchemy.Column(sqlalchemy.Integer)
    img_name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    wav_name = sqlalchemy.Column(sqlalchemy.String)

    artist = sqlalchemy.orm.relation('Artist')
    genre = sqlalchemy.orm.relation('Genre')
    user = sqlalchemy.orm.relation('User')
    likes = sqlalchemy.orm.relation('Like', back_populates='song')
    dislikes = sqlalchemy.orm.relation('Dislike', back_populates='song')
