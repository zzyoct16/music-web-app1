import abc
from typing import List
from datetime import date

from music.domainmodel.user import User
from music.domainmodel.track import Track
from music.domainmodel.album import Album
from music.domainmodel.genre import Genre
from music.domainmodel.review import Review
from music.domainmodel.artist import Artist


repo_instance = None
                

class RepositoryException(Exception):

    def __init__(self, message=None):
        pass


class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def add_user(self, user: User):
        """" Adds a User to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, user_name) -> User:
        """ Returns the User named user_name from the repository.
        If there is no User with the given user_name, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_track(self, track: Track):
        """ Adds an Article to the repository. """
        raise NotImplementedError
    
    @abc.abstractmethod
    def add_album(self, album: Album):
        """ Adds an Article to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def add_artist(self, artist: Artist):
        """ Adds an Article to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_track(self, id: int) -> Track:
        """ Returns Article with id from the repository.
        If there is no Article with the given id, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_tracks(self) -> List[Track]:
        """ Returns Article with id from the repository.
        If there is no Article with the given id, this method returns None.
        """
        raise NotImplementedError
        
    @abc.abstractmethod
    def get_tracks_by_artist(self, target_artist: Artist) -> List[Track]:
        """ Returns a list of Articles that were published on target_date.
        If there are no Articles on the given date, this method returns an empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_tracks_by_album(self, target_album: Album) -> List[Track]:
        """ Returns a list of Articles that were published on target_date.
        If there are no Articles on the given date, this method returns an empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_tracks(self) -> int:
        """ Returns the number of Articles in the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_first_track(self) -> Track:
        """ Returns the first Article, ordered by date, from the repository.
        Returns None if the repository is empty.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_last_track(self) -> Track:
        """ Returns the last Article, ordered by date, from the repository.
        Returns None if the repository is empty.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_tracks_by_id(self, id_list):
        """ Returns a list of Articles, whose ids match those in id_list, from the repository.
        If there are no matches, this method returns an empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_track_ids_for_genre(self, genre_name: str):
        """ Returns a list of ids representing Articles that are tagged by tag_name.
        If there are Articles that are tagged by tag_name, this method returns an empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_genre(self, genre: Genre):
        """ Adds a Tag to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_genres(self) -> List[Genre]:
        """ Returns the Tags stored in the repository. """
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_artists(self) -> List[Artist]:
        """ Returns the Tags stored in the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_albums(self):
        """ Returns the Tags stored in the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def add_review(self, review: Review):
        """ Adds a Comment to the repository.
        If the Comment doesn't have bidirectional links with an Article and a User, this method raises a
        RepositoryException and doesn't update the repository.
        """
        if review.user is None or review not in review.user.reviews:
            raise RepositoryException('Review not correctly attached to a User')
        if review.track is None or review not in review.track.reviews:
            raise RepositoryException('Review not correctly attached to an Track')

    @abc.abstractmethod
    def get_reviews(self):
        """ Returns the Comments stored in the repository. """
        raise NotImplementedError