from sqlalchemy import (
    Table, MetaData, Column, Integer, String, ForeignKey
)
from sqlalchemy.orm import mapper, relationship, synonym

from music.domainmodel.user import User
from music.domainmodel.review import Review
from music.domainmodel.artist import Artist
from music.domainmodel.album import Album
from music.domainmodel.track import Track
from music.domainmodel.genre import Genre

metadata = MetaData()

users_table = Table(
    'users', metadata,
    Column('user_name', String(255), unique=True, primary_key=True, nullable=False),
    Column('password', String(255), nullable=False)
)

reviews_table = Table(
    'reviews', metadata,
    Column('user_name', ForeignKey('users.user_name'), primary_key=True),
    Column('track_id', ForeignKey('tracks.track_id'), primary_key=True),
    Column('rating', Integer, nullable=False),
)

tracks_table = Table(
    'tracks', metadata,
    Column('track_id', Integer, primary_key=True),
    Column('title', String(255), nullable=False),
    Column('video_hyperlink', String(255), nullable=False),
    Column('artist_id', ForeignKey('artists.artist_id')),
    Column('album_id', ForeignKey('albums.album_id')),
)

genres_table = Table(
    'genres', metadata,
    Column('genre_id', Integer, primary_key=True),
    Column('name', String(64), nullable=False)
)

artists_table = Table(
    'artists', metadata,
    Column('artist_id', Integer, primary_key=True),
    Column('full_name', String(64), nullable=False),
)

albums_table = Table(
    'albums', metadata,
    Column('album_id', Integer, primary_key=True),
    Column('title', String(64), nullable=False),
)

track_genres_table = Table(
    'track_genres', metadata,
    Column('id', Integer, primary_key=True),
    Column('track_id', ForeignKey('tracks.track_id')),
    Column('genre_id', ForeignKey('genres.genre_id'))
)

def map_model_to_tables():
    mapper(User, users_table, properties={
        '_User__user_name': users_table.c.user_name,
        '_User__password': users_table.c.password,
        '_User__reviews': relationship(Review, backref='_Review__user')
    })
    mapper(Review, reviews_table, properties={
        '_Review__rating': reviews_table.c.rating,
    })
    mapper(Track, tracks_table, properties={
        '_Track__track_id': tracks_table.c.track_id,
        '_Track__title': tracks_table.c.title,
        '_Track__video_hyperlink': tracks_table.c.video_hyperlink,
        '_Track__reviews': relationship(Review, backref='_Review__track'),
        '_Track__artist': relationship(Artist),
        '_Track__album': relationship(Album),
        '_Track__genres': relationship(Genre, secondary=track_genres_table),
    })
    mapper(Genre, genres_table, properties={
        '_Genre__genre_id': genres_table.c.genre_id,
        '_Genre__name': genres_table.c.name
    })
    mapper(Artist, artists_table, properties={
        '_Artist__artist_id': artists_table.c.artist_id,
        '_Artist__full_name': artists_table.c.full_name,
    })
    mapper(Album, albums_table, properties={
        '_Album__album_id': albums_table.c.album_id,
        '_Album__title': albums_table.c.title,
    })