from music.domainmodel.track import Track
from music.domainmodel.user import User


class Review:

    def __init__(self, track: Track, user: User, rating: int):
        self.__track = None
        if isinstance(track, Track):
            self.__track = track

        self.__user = None
        if isinstance(user, User):
            self.__user = user

        if isinstance(rating, int) and 1 <= rating <= 5:
            self.__rating = rating
        else:
            raise ValueError('Invalid value for the rating.')

    @property
    def track(self) -> Track:
        return self.__track

    @property
    def user(self) -> User:
        return self.__user

    @property
    def rating(self) -> int:
        return self.__rating

    @rating.setter
    def rating(self, new_rating: int):
        if isinstance(new_rating, int) and 1 <= new_rating <= 5:
            self.__rating = new_rating
        else:
            self.__rating = None
            raise ValueError("Wrong value for the rating")

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return other.track == self.track and other.user == self.user

    def __repr__(self):
        return f'<Review of track {self.track}, rating = {self.rating}>'
