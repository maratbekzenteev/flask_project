import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Like(SqlAlchemyBase):
    __tablename__ = 'likes'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    song_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('songs.id'))

    user = sqlalchemy.orm.relation('User')
    song = sqlalchemy.orm.relation('Song')
