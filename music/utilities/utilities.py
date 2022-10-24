from flask import Blueprint, url_for

import music.adapters.Repository as repo
import music.utilities.services as services


# Configure Blueprint.
utilities_blueprint = Blueprint(
    'utilities_bp', __name__)


def get_genres_and_urls():
    genres = services.get_genre_names_and_urls(repo.repo_instance)
    return genres

def get_artists_and_urls():
    artists = services.get_artist_names_and_urls(repo.repo_instance)
    return artists

def get_albums_and_urls():
    albums = services.get_album_names_and_urls(repo.repo_instance)
    return albums

def get_all_tracks(page_num):
    tracks = services.get_all_tracks(repo.repo_instance)
    try:
        response = {
            "track_data": tracks[page_num],
            "pagination": {},
        }
    except:
        response = {
            "track_data": tracks[len(tracks)-1],
            "pagination": {},
        }
    if page_num >= len(tracks)-1:
        response['pagination']['next'] = f"{url_for('tracks_bp.view_all_tracks')}?page_num={page_num}"
        response['pagination']['previous'] = f"{url_for('tracks_bp.view_all_tracks')}?page_num={page_num-1}"
    else:
        if page_num > 0:
            response['pagination']['next'] = f"{url_for('tracks_bp.view_all_tracks')}?page_num={page_num+1}"
            response['pagination']['previous'] = f"{url_for('tracks_bp.view_all_tracks')}?page_num={page_num-1}"
        else:
            response['pagination']['next'] = f"{url_for('tracks_bp.view_all_tracks')}?page_num={page_num+1}"
            response['pagination']['previous'] = f"{url_for('tracks_bp.view_all_tracks')}?page_num={page_num}"
    return response

    

