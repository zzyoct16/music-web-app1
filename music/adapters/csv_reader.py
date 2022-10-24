import csv
from pathlib import Path
import os
import ast
from music.adapters.Repository import AbstractRepository
from music.domainmodel.user import User
from music.domainmodel.review import Review
from music.domainmodel.artist import Artist
from music.domainmodel.album import Album
from music.domainmodel.track import Track
from music.domainmodel.genre import Genre
from music.utilities.services import get_random_video


def create_track_object(track_row):
    track = Track(int(track_row['track_id']), track_row['track_title'])
    track.track_url = track_row['track_url']
    track_duration = round(float(
        track_row['track_duration'])) if track_row['track_duration'] is not None else None
    if type(track_duration) is int:
        track.track_duration = track_duration
    return track

def extract_genres(track_row: dict):
    # List of dictionaries inside the string.
    track_genres_raw = track_row['track_genres']
    # Populate genres. track_genres can be empty (None)
    if track_genres_raw:
        try:
            genre_dicts = ast.literal_eval(
                track_genres_raw) if track_genres_raw != "" else []
            return genre_dicts
        except Exception as e:
            print(track_genres_raw)
            print(f'Exception occurred while parsing genres: {e}')

    
def read_tracks_file(data_path: Path):
    track_file = str(Path(data_path) / "raw_tracks_excerpt.csv")
    if not os.path.exists(track_file):
        print(f"path {track_file} does not exist!")
        return

    track_rows = []
    # encoding of unicode_escape is required to decode successfully
    with open(track_file, encoding='unicode_escape') as track_csv:
        reader = csv.DictReader(track_csv)
        for track_row in reader:
            track_rows.append(track_row)
    return track_rows

def read_csv_files(data_path: Path, repo: AbstractRepository):
    genres = {}
    artists = {}
    albums = {}
    # list of track csv rows, not track objects
    track_rows: list = read_tracks_file(data_path)

    # Make sure re-initialize to empty list, so that calling this function multiple times does not create
    # duplicated dataset.
    for track_row in track_rows:
        track = create_track_object(track_row)
        track.video_hyperlink = get_random_video()
        repo.add_track(track)
        # Extract track_genres attributes and assign genres to the track.
        genre_dicts = extract_genres(track_row)
        try:
            for genre_dict in genre_dicts:
                if genre_dict['genre_title'] not in list(genres.keys()):
                    genres[genre_dict['genre_title']] = []
                    genres[genre_dict['genre_title']].append(genre_dict['genre_id'])
                genres[genre_dict['genre_title']].append(track.track_id)
        except:
            pass

        if track_row['artist_name'] not in artists.keys():
            artists[track_row['artist_name']] = []
            artists[track_row['artist_name']].append(track_row['artist_id'])
        artists[track_row['artist_name']].append(track.track_id)

        if track_row['album_title'] not in albums.keys():
            albums[track_row['album_title']] = []
            albums[track_row['album_title']].append(track_row['album_id'])
        albums[track_row['album_title']].append(track.track_id)

    for artist_name in artists.keys():
        try:
            artist = Artist(int(artists[artist_name][0]), artist_name)
        
            for track_id in artists[artist_name][1:]:
                track = repo.get_track(int(track_id))
                track.artist = artist
            repo.add_artist(artist)
        except:
            pass
       
    for album_name in albums.keys():
        try:
            album = Album(int(albums[album_name][0]), album_name)
        
            for track_id in albums[album_name][1:]:
                track = repo.get_track(int(track_id))
                track.album = album
            repo.add_album(album)
        except:
            pass

    for genre_name in genres.keys():
        try:
            genre = Genre(
                int(genres[genre_name][0]), genre_name)
            for track_id in genres[genre_name][1:]:
                track = repo.get_track(int(track_id))
                track.add_genre(genre)
            repo.add_genre(genre)
        except:
            continue

        
def populate(data_path: Path, repo: AbstractRepository):
    # Load tracks and genres into the repository.
    read_csv_files(data_path, repo)