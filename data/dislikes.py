import sqlalchemy
from sqlalchemy import orm
from db_session import SqlAlchemyBase


class Dislike(SqlAlchemyBase):
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer)
    song_id = sqlalchemy.Column(sqlalchemy.Integer)

    user = sqlalchemy.orm.relation('User')
    song = sqlalchemy.orm.relation('Song')
