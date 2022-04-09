import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Artist(SqlAlchemyBase):
    __tablename__ = 'artists'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String)
    img_name = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    songs = sqlalchemy.orm.relation('Song', back_populates='artist')
