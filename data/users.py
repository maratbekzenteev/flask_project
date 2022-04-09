import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, unique=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.Integer, unique=True)
    playlist = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    songs = sqlalchemy.orm.relation('Song', back_populates='user')
    likes = sqlalchemy.orm.relation('Like', back_populates='user')
    dislikes = sqlalchemy.orm.relation('Dislike', back_populates='user')
