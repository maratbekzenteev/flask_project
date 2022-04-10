import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Song(SqlAlchemyBase):
    __tablename__ = 'songs'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String)
    artist_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("artists.id"))
    genre_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("genres.id"))
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    img_name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    wav_name = sqlalchemy.Column(sqlalchemy.String)

    artist = sqlalchemy.orm.relation('Artist', foreign_keys=[artist_id])
    genre = sqlalchemy.orm.relation('Genre', foreign_keys=[genre_id])
    user = sqlalchemy.orm.relation('User', foreign_keys=[user_id])

    likes = sqlalchemy.orm.relation('Like', back_populates='song')
    dislikes = sqlalchemy.orm.relation('Dislike', back_populates='song')
