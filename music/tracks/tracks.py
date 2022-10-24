from flask import Blueprint
from flask import request, render_template, url_for, session
import json

import music.adapters.Repository as repo
import music.utilities.utilities as utilities
import music.utilities.services as services

tracks_blueprint = Blueprint('tracks_bp', __name__)

@tracks_blueprint.route('/all', methods=['GET'])
def view_all_tracks():
    try:
        page_num = int(request.args.get('page_num'))
    except:
        page_num = 0
    return render_template(
        'tracks/tracks.html',
        selected_tracks=utilities.get_all_tracks(page_num),
        genres=utilities.get_genres_and_urls(),
        artists=utilities.get_artists_and_urls(),
        albums=utilities.get_albums_and_urls()
    )

@tracks_blueprint.route('/tracks_by_genre', methods=['GET'])
def tracks_by_genre():
    try:
        page_num = int(request.args.get('page_num'))
        genre_name = request.args.get('genre')
    except:
        page_num = 0
        genre_name = 'African'
    track_ids = services.get_track_ids_for_genre(genre_name, repo.repo_instance)
    tracks = services.get_tracks_by_id(track_ids, repo.repo_instance)
    try:
        if page_num > len(tracks)-1:
            page_num = len(tracks)-1
        response = {
            "track_data": tracks[page_num],
            "pagination": {},
        }
        if len(tracks)-1 == 0:
            response['pagination']['next'] = f"{url_for('tracks_bp.tracks_by_genre')}?genre={genre_name}&page_num={page_num}"
            response['pagination']['previous'] = f"{url_for('tracks_bp.tracks_by_genre')}?genre={genre_name}&page_num={page_num}"
        elif page_num >= len(tracks)-1:
            response['pagination']['next'] = f"{url_for('tracks_bp.tracks_by_genre')}?genre={genre_name}&page_num={page_num}"
            response['pagination']['previous'] = f"{url_for('tracks_bp.tracks_by_genre')}?genre={genre_name}&page_num={page_num-1}"
        else:
            if page_num > 0:
                response['pagination']['next'] = f"{url_for('tracks_bp.tracks_by_genre')}?genre={genre_name}&page_num={page_num+1}"
                response['pagination']['previous'] = f"{url_for('tracks_bp.tracks_by_genre')}?genre={genre_name}&page_num={page_num-1}"
            else:
                response['pagination']['next'] = f"{url_for('tracks_bp.tracks_by_genre')}?genre={genre_name}&page_num={page_num+1}"
                response['pagination']['previous'] = f"{url_for('tracks_bp.tracks_by_genre')}?genre={genre_name}&page_num={page_num}"
    except:
        response = {
            "message": f'Genre: {genre_name} has no tracks.',
            "pagination": {},
        }
    
    return render_template(
        'tracks/tracks.html',
        selected_tracks=response,
        genres=utilities.get_genres_and_urls(),
        artists=utilities.get_artists_and_urls(),
        albums=utilities.get_albums_and_urls()
    )

@tracks_blueprint.route('/tracks_by_artist', methods=['GET'])
def tracks_by_artist():
    try:
        page_num = int(request.args.get('page_num'))
        artist_name = request.args.get('artist')
    except:
        page_num = 0
        artist_name = 'AWOL'
    tracks = services.get_tracks_for_artist(artist_name, repo.repo_instance)
    try:
        if page_num > len(tracks)-1:
            page_num = len(tracks)-1
        response = {
            "track_data": tracks[page_num],
            "pagination": {},
        }
        if len(tracks)-1 == 0:
            response['pagination']['next'] = f"{url_for('tracks_bp.tracks_by_artist')}?artist={artist_name}&page_num={page_num}"
            response['pagination']['next'] = f"{url_for('tracks_bp.tracks_by_artist')}?artist={artist_name}&page_num={page_num}"
        elif page_num >= len(tracks)-1:
            response['pagination']['next'] = f"{url_for('tracks_bp.tracks_by_artist')}?artist={artist_name}&page_num={page_num}"
            response['pagination']['previous'] = f"{url_for('tracks_bp.tracks_by_artist')}?artist={artist_name}&page_num={page_num-1}"
        else:
            if page_num > 0:
                response['pagination']['next'] = f"{url_for('tracks_bp.tracks_by_artist')}?artist={artist_name}&page_num={page_num+1}"
                response['pagination']['previous'] = f"{url_for('tracks_bp.tracks_by_artist')}?artist={artist_name}&page_num={page_num-1}"
            else:
                response['pagination']['next'] = f"{url_for('tracks_bp.tracks_by_artist')}?artist={artist_name}&page_num={page_num+1}"
                response['pagination']['previous'] = f"{url_for('tracks_bp.tracks_by_artist')}?artist={artist_name}&page_num={page_num}"
    except:
        response = {
            "message": f'Artist: {artist_name} has no tracks.',
            "pagination": {},
        }
    
    return render_template(
        'tracks/tracks.html',
        selected_tracks=response,
        genres=utilities.get_genres_and_urls(),
        artists=utilities.get_artists_and_urls(),
        albums=utilities.get_albums_and_urls()
    )

@tracks_blueprint.route('/tracks_by_album', methods=['GET'])
def tracks_by_album():
    try:
        page_num = int(request.args.get('page_num'))
        album_name = request.args.get('album')
    except:
        page_num = 0
        album_name = 'Au'
    tracks = services.get_tracks_for_album(album_name, repo.repo_instance)
    try:
        if page_num > len(tracks)-1:
            page_num = len(tracks)-1
        response = {
            "track_data": tracks[page_num],
            "pagination": {},
        }
        if len(tracks)-1 == 0:
            response['pagination']['next'] = f"{url_for('tracks_bp.tracks_by_album')}?album={album_name}&page_num={page_num}"
            response['pagination']['previous'] = f"{url_for('tracks_bp.tracks_by_album')}?album={album_name}&page_num={page_num}"
        elif page_num >= len(tracks)-1:
            response['pagination']['next'] = f"{url_for('tracks_bp.tracks_by_album')}?album={album_name}&page_num={page_num}"
            response['pagination']['previous'] = f"{url_for('tracks_bp.tracks_by_album')}?album={album_name}&page_num={page_num-1}"
        else:
            if page_num > 0:
                response['pagination']['next'] = f"{url_for('tracks_bp.tracks_by_album')}?album={album_name}&page_num={page_num+1}"
                response['pagination']['previous'] = f"{url_for('tracks_bp.tracks_by_album')}?album={album_name}&page_num={page_num-1}"
            else:
                response['pagination']['next'] = f"{url_for('tracks_bp.tracks_by_album')}?album={album_name}&page_num={page_num+1}"
                response['pagination']['previous'] = f"{url_for('tracks_bp.tracks_by_album')}?album={album_name}&page_num={page_num}"
    except:
        response = {
            "message": f'Album: {album_name} has no tracks.',
            "pagination": {},
        }
    
    return render_template(
        'tracks/tracks.html',
        selected_tracks=response,
        genres=utilities.get_genres_and_urls(),
        artists=utilities.get_artists_and_urls(),
        albums=utilities.get_albums_and_urls()
    )

@tracks_blueprint.route('/review', methods=['POST'])
def review_track():
    if 'user_name' not in session:
        return json.dumps({"message": url_for('authentication_bp.login')})
    user_name = session['user_name']
    # Obtain the user name of the currently logged in user.
    data = request.get_json(force=True)
    services.add_review(int(data['track_id']),int(data['value']),user_name, repo.repo_instance)
    return json.dumps({"message":"success"})
    
    

    


