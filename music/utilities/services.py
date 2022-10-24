from typing import Iterable
from werkzeug.security import generate_password_hash, check_password_hash
import random
from music.adapters.Repository import AbstractRepository
from music.domainmodel.review import Review
from music.domainmodel.track import Track
from music.domainmodel.user import User
from flask import url_for

class NameNotUniqueException(Exception):
    pass


class UnknownUserException(Exception):
    pass


class AuthenticationException(Exception):
    pass


class NonExistentTrackException(Exception):
    pass


def add_user(user_name: str, password: str, repo: AbstractRepository):
    # Check that the given user name is available.
    user = repo.get_user(user_name)
    if user is not None:
        raise NameNotUniqueException
    # Encrypt password so that the database doesn't store passwords 'in the clear'.
    password_hash = generate_password_hash(password)
    # Create and store the new User, with password encrypted.
    user = User(user_name, password_hash)
    repo.add_user(user)


def get_user(user_name: str, repo: AbstractRepository):
    user = repo.get_user(user_name)
    if user is None:
        raise UnknownUserException

    return user_to_dict(user)


def authenticate_user(user_name: str, password: str, repo: AbstractRepository):
    authenticated = False

    user = repo.get_user(user_name)
    if user is not None:
        authenticated = check_password_hash(user.password, password)
    if not authenticated:
        raise AuthenticationException

def get_genre_names_and_urls(repo: AbstractRepository):
    genres = repo.get_genres()
    genre_names = [genre.name.replace(" ","-") for genre in genres]
    genre_names.sort()
    genres_dict = {}
    for genre in genre_names:
        genres_dict.update({genre:f"{url_for('tracks_bp.tracks_by_genre')}?genre={genre}&page_num=0"})

    return genres_dict

def get_artist_names_and_urls(repo: AbstractRepository):
    artists = repo.get_artists()
    artist_names = [artist.full_name.replace(" ","_") for artist in artists]
    artist_names.sort()
    artists_dict = {}
    for artist in artist_names:
        artists_dict.update({artist:f"{url_for('tracks_bp.tracks_by_artist')}?artist={artist}&page_num=0"})

    return artists_dict

def get_album_names_and_urls(repo: AbstractRepository):
    albums = repo.get_albums()
    album_titles = [album.title.replace(" ","_") for album in albums]
    album_titles.sort()
    albums_dict = {}
    for album in album_titles:
        albums_dict.update({album:f"{url_for('tracks_bp.tracks_by_album')}?album={album}&page_num=0"})

    return albums_dict

def get_all_tracks(repo: AbstractRepository):
    tracks = repo.get_tracks()
    return tracks_to_dict(tracks)

def get_track_ids_for_genre(genre_name, repo: AbstractRepository):
    track_ids = repo.get_track_ids_for_genre(genre_name)
    return track_ids

def get_tracks_for_artist(artist_name, repo: AbstractRepository):
    tracks = repo.get_tracks_by_artist(artist_name)
    return tracks_to_dict(tracks)

def get_tracks_for_album(album_name, repo: AbstractRepository):
    tracks = repo.get_tracks_by_album(album_name)
    return tracks_to_dict(tracks)

def get_tracks_by_id(id_list, repo: AbstractRepository):
    tracks = repo.get_tracks_by_id(id_list)
    tracks_dict = tracks_to_dict(tracks)
    return tracks_dict

def add_review(track_id, rating, user_name, repo: AbstractRepository):
    track = repo.get_track(track_id)
    if track is None:
        raise NonExistentTrackException
    user = repo.get_user(user_name)
    if user is None:
        raise UnknownUserException
    try:
        review = make_review(track, user, rating)
        repo.add_review(review)
    except:
        pass


# ============================================
# Functions to convert dicts to model entities
# ============================================

def user_to_dict(user: User):
    user_dict = {
        'user_name': user.user_name,
        'password': user.password
    }
    return user_dict

def track_to_dict(track: Track):
    track_dict = {
        'track_id': track.track_id,
        'title': track.title,
        'artist': track.artist,
        'album': track.album,
        'genres': track.genres,
        'rating':int(sum([review.rating for review in track.reviews])/len(track.reviews)) if len(track.reviews) > 0 else 0,
        'video': track.video_hyperlink
    }
    return track_dict


def tracks_to_dict(tracks: Iterable[Track]):
    return [track_to_dict(track) for track in tracks]

def make_review(track, user, rating):
    review = Review(track, user, rating)
    user.add_review(review)
    track.add_review(review)
    return review

def get_random_video():
    videos = [
        "-zV-AxfysJA",
        "nDdZfAAvcC8",
        "t20wYezWfDw",
        "lvY8T9y6JPk",
        "yGNkjDvsHDU",
        "P96OSLHNPUY",
        "3u43yUcB8uY",
        "dxMP7U_DrtE",
        "U0YhKshmj9s",
        "TsAidqXIfos"
    ]
    return random.choice(videos)