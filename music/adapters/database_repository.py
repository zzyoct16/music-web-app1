from typing import List

from sqlalchemy import desc, asc
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from sqlalchemy.orm import scoped_session

from music.domainmodel.user import User
from music.domainmodel.track import Track
from music.domainmodel.album import Album
from music.domainmodel.genre import Genre
from music.domainmodel.review import Review
from music.domainmodel.artist import Artist
from music.adapters.Repository import AbstractRepository


class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        # this method can be used e.g. to allow Flask to start a new session for each http request,
        # via the 'before_request' callback
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory)

    def close_current_session(self):
        if not self.__session is None:
            self.__session.close()


class SqlAlchemyRepository(AbstractRepository):

    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()

    def add_user(self, user: User):
        with self._session_cm as scm:
            scm.session.add(user)
            scm.commit()

    def get_user(self, user_name: str) -> User:
        user = None
        try:
            user = self._session_cm.session.query(User).filter(User._User__user_name == user_name).one()
        except NoResultFound:
            # Ignore any exception and return None.
            pass

        return user

    def add_track(self, track: Track):
        with self._session_cm as scm:
            scm.session.add(track)
            scm.commit()

    def add_album(self, album: Album):
        with self._session_cm as scm:
            scm.session.add(album)
            scm.commit()

    def add_artist(self, artist: Artist):
        with self._session_cm as scm:
            scm.session.add(artist)
            scm.commit()


    def get_track(self, id: int) -> Track:
        track = None
        try:
            track = self._session_cm.session.query(Track).filter(Track._Track__track_id == id).one()
        except NoResultFound:
            # Ignore any exception and return None.
            pass

        return track

    def get_tracks(self) -> List[Track]:
        tracks = None
        try:
            tracks = self._session_cm.session.query(Track).all()
        except NoResultFound:
            # Ignore any exception and return None.
            pass

        return tracks
        

    def get_tracks_by_artist(self, target_artist: str) -> List[Track]:
        if target_artist is None:
            tracks = self._session_cm.session.query(Track).all()
            return tracks
        else:
            # Return tracks matching target_date; return an empty list if there are no matches.
            try:
                artist_id = self._session_cm.session.query(Artist).filter(Artist._Artist__full_name == target_artist.replace("_"," ")).one().artist_id
            
                tracks = self._session_cm.session.query(Track).filter(Track.artist_id == artist_id).all()
            except:
                tracks = []
            return tracks

    def get_tracks_by_album(self, target_album: Album) -> List[Track]:
        if target_album is None:
            tracks = self._session_cm.session.query(Track).all()
            return tracks
        else:
            # Return tracks matching target_date; return an empty list if there are no matches.
            try:
                album_id = self._session_cm.session.query(Album).filter(Album._Album__title == target_album.replace("_"," ")).one().album_id
            
                tracks = self._session_cm.session.query(Track).filter(Track.album_id == album_id).all()
            except:
                tracks = []
            return tracks

    def get_number_of_tracks(self):
        number_of_tracks = self._session_cm.session.query(Track).count()
        return number_of_tracks

    def get_first_track(self):
        track = self._session_cm.session.query(Track).first()
        return track

    def get_last_track(self):
        track = self._session_cm.session.query(Track).order_by(desc(Track._Track__track_id)).last()
        return track

    def get_tracks_by_id(self, id_list: List[int]):
        tracks = self._session_cm.session.query(Track).filter(Track._Track__track_id.in_(id_list)).all()
        return tracks

    def get_track_ids_for_genre(self, genre_name: str):
        track_ids = []

        # Use native SQL to retrieve track ids, since there is no mapped class for the track_tags table.
        row = self._session_cm.session.execute('SELECT genre_id FROM genres WHERE name = :name', {'name': genre_name}).fetchone()

        if row is None:
            # No tag with the name tag_name - create an empty list.
            track_ids = list()
        else:
            genre_id = row[0]
            # Retrieve track ids of tracks associated with the tag.
            track_ids = self._session_cm.session.execute(
                    'SELECT track_id FROM track_genres WHERE genre_id = :genre_id ORDER BY track_id ASC',
                    {'genre_id': genre_id}
            ).fetchall()
            track_ids = [id[0] for id in track_ids]

        return track_ids

    def get_genres(self) -> List[Genre]:
        genres = self._session_cm.session.query(Genre).all()
        return genres

    def get_artists(self) -> List[Artist]:
        artists = self._session_cm.session.query(Artist).all()
        return artists

    def get_albums(self) -> List[Album]:
        albums = self._session_cm.session.query(Album).all()
        return albums

    def add_genre(self, genre: Genre):
        with self._session_cm as scm:
            scm.session.add(genre)
            scm.commit()

    def get_reviews(self) -> List[Review]:
        reviews = self._session_cm.session.query(Review).all()
        return reviews

    def add_review(self, review: Review):
        super().add_review(review)
        with self._session_cm as scm:
            scm.session.add(review)
            scm.commit()
        