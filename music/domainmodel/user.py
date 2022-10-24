from music.domainmodel.track import Track


class User:

    def __init__(self, user_name: str, password: str):

        if type(user_name) is str:
            self.__user_name = user_name.lower().strip()
        else:
            self.__user_name = None

        if isinstance(password, str) and len(password) >= 7:
            self.__password = password
        else:
            self.__password = None                                                                                                                      

        self.__reviews = []
        self.__liked_tracks: list[Track] = []

    @property
    def user_name(self) -> str:
        return self.__user_name

    @property
    def password(self) -> str:
        return self.__password

    @property
    def reviews(self) -> list:
        return self.__reviews

    def add_review(self, new_review):
        if new_review in self.__reviews:
            return
        self.__reviews.append(new_review)

    def remove_review(self, review):
        if review not in self.__reviews:
            return
        self.__reviews.remove(review)

    @property
    def liked_tracks(self) -> list:
        return self.__liked_tracks

    def add_liked_track(self, track: Track):
        if not isinstance(track, Track) or track in self.__liked_tracks:
            return
        self.__liked_tracks.append(track)

    def remove_liked_track(self, track: Track):
        if not isinstance(track, Track) or track not in self.__liked_tracks:
            return
        self.__liked_tracks.remove(track)

    def __repr__(self):
        return f'<User {self.user_name}>'

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.user_name == other.user_name

    def __lt__(self, other):
        if not isinstance(other, self.__class__):
            return True
        return self.user_name < other.user_name

    def __hash__(self):
        return hash(self.user_name)
