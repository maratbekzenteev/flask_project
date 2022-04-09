import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Genre(SqlAlchemyBase):
    __tablename__ = 'genres'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String)

    songs = sqlalchemy.orm.relation('Song', back_populates='genre')
