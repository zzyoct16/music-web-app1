from typing import List
from bisect import bisect, bisect_left, insort_left
from music.adapters.Repository import AbstractRepository, RepositoryException
from music.domainmodel.user import User
from music.domainmodel.review import Review
from music.domainmodel.artist import Artist
from music.domainmodel.album import Album
from music.domainmodel.track import Track
from music.domainmodel.genre import Genre


class MemoryRepository(AbstractRepository):
    # tracks ordered by date, not id. id is assumed unique.

    def __init__(self):
        self.__tracks = list()
        self.__tracks_index = dict()
        self.__albums = dict()
        self.__artists = list()
        self.__genres = list()
        self.__users = list()
        self.__reviews = list()

    def add_user(self, user: User):
        self.__users.append(user)

    def get_user(self, user_name) -> User:
        return next((user for user in self.__users if user.user_name == user_name), None)

    def add_track(self, track: Track):
        insort_left(self.__tracks, track)
        self.__tracks_index[track.track_id] = track

    def add_album(self, album: Album):
        if album != None:
            self.__albums[album.album_id] = album

    def add_artist(self, artist: Artist):
        if artist not in self.__artists and artist != None:
            self.__artists.append(artist)

    def get_track(self, id: int) -> Track:
        track = None

        try:
            track = self.__tracks_index[id]
        except KeyError:
            pass  # Ignore exception and return None.

        return track

    def get_tracks(self) -> List[Track]:
        return self.__tracks

    def get_tracks_by_artist(self, target_artist: str) -> List[Track]:
        
        matching_tracks = list()

        try:
            for track in self.__tracks:
                
                if track.artist.full_name == target_artist.replace("_"," "):
                    matching_tracks.append(track)
        except ValueError:
            # No tracks for specified date. Simply return an empty list.
            pass

        return matching_tracks

    def get_tracks_by_album(self, target_album: Album) -> List[Track]:
        
        matching_tracks = list()

        try:
            for track in self.__tracks:
                if track.album != None and track.album.title == target_album.replace("_"," "):
                    matching_tracks.append(track)
        except ValueError:
            # No tracks for specified date. Simply return an empty list.
            pass

        return matching_tracks


    def get_number_of_tracks(self):
        return len(self.__tracks)

    def get_first_track(self):
        track = None

        if len(self.__tracks) > 0:
            track = self.__tracks[0]
        return track

    def get_last_track(self):
        track = None

        if len(self.__tracks) > 0:
            track = self.__tracks[-1]
        return track

    def get_tracks_by_id(self, id_list):
        # Strip out any ids in id_list that don't represent track ids in the repository.
        existing_ids = [id for id in id_list if id in self.__tracks_index]

        # Fetch the tracks.
        tracks = [self.__tracks_index[id] for id in existing_ids]
        return tracks

    def get_track_ids_for_genre(self, genre_name: str):
        # Linear search, to find the first occurrence of a Tag with the name tag_name.
        genre = next((genre for genre in self.__genres if genre.name == genre_name), None)

        # Retrieve the ids of tracks associated with the Tag.
        if genre is not None:
            track_ids = []
            for track in self.__tracks:
                if genre in track.genres:
                    track_ids.append(track.track_id)
        else:
            # No Tag with name tag_name, so return an empty list.
            track_ids = list()

        return track_ids

    def add_genre(self, genre: Genre):
        if genre not in self.__genres and genre != None:
            self.__genres.append(genre)

    def get_genres(self) -> List[Genre]:
        return self.__genres

    def get_artists(self) -> List[Artist]:
        return self.__artists

    def get_albums(self):
        return self.__albums

    def add_review(self, review: Review):
        # call parent class first, add_review relies on implementation of code common to all derived classes
        super().add_review(review)
        self.__reviews.append(review)

    def get_reviews(self):
        return self.__reviews

    # Helper method to return track index.
    def track_index(self, track: Track):
        index = bisect_left(self.__tracks, track)
        if index != len(self.__tracks) and self.__tracks[index].track_id == track.track_id:
            return index
        raise ValueError