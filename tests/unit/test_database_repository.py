from typing import List

import pytest
from music.adapters.Repository import RepositoryException

from music.domainmodel.user import User
from music.domainmodel.track import Track
from music.domainmodel.genre import Genre
from music.domainmodel.review import Review
from music.utilities.services import make_review
from tests.conftest import session_factory

repo = session_factory()

def test_read_csv_files():
    assert repo.get_number_of_tracks() == 2000
    assert len(repo.get_artists()) == 263
    assert len(repo.get_albums()) == 428
    assert len(repo.get_genres()) == 60


def test_repository_can_add_a_user():
    user = User('dave', '123456789')
    repo.add_user(user)

    assert repo.get_user('dave') is user


def test_repository_can_retrieve_a_user():
    user2 = repo.get_user('dave')
    assert user2 == User('dave', '123456789')


def test_repository_does_not_retrieve_a_non_existent_user():
    user = repo.get_user('prince')
    assert user is None


def test_repository_can_retrieve_track_count():
    number_of_tracks = repo.get_number_of_tracks()
    assert number_of_tracks == 2000


def test_repository_can_add_track():
    track = Track(9869786,'heat')
    track.video_hyperlink = "random_link"
    repo.add_track(track)

    assert repo.get_track(9869786) is track


def test_repository_can_retrieve_track():
    track = repo.get_track(2)

    # Check that the track has the expected album_id.
    assert track.album.album_id == 1


def test_repository_does_not_retrieve_a_non_existent_track():
    track = repo.get_track(101)
    assert track is None


def test_repository_can_retrieve_tracks_by_artist():
    tracks = repo.get_tracks_by_artist("AWOL")
    assert len(tracks) == 4


def test_repository_does_not_retrieve_an_track_when_there_are_no_tracks_for_a_given_artist():
    tracks = repo.get_tracks_by_artist("sdgsdfgjsodfgjh")
    assert len(tracks) == 0


def test_repository_can_retrieve_genres():
    genres: List[Genre] = repo.get_genres()

    assert len(genres) == 60


def test_repository_can_get_first_genre():
    track = repo.get_first_track()
    assert track.track_id == 2


def test_repository_can_get_tracks_by_ids():
    tracks = repo.get_tracks_by_id([2, 3, 5])

    assert len(tracks) == 3
    assert tracks[0].album.album_id == 1
    assert tracks[1].album.album_id == 1
    assert tracks[2].album.album_id == 1


def test_repository_does_not_retrieve_track_for_non_existent_id():
    tracks = repo.get_tracks_by_id([2, 9])

    assert len(tracks) == 1


def test_repository_returns_an_empty_list_for_non_existent_ids():
    tracks = repo.get_tracks_by_id([0, 9])

    assert len(tracks) == 0


def test_repository_returns_an_empty_list_for_non_existent_genre():
    track_ids = repo.get_track_ids_for_genre('United States')

    assert len(track_ids) == 0


def test_repository_can_add_a_genre():
    genre = Genre(985,'Motoring')
    repo.add_genre(genre)

    assert genre in repo.get_genres()


def test_repository_can_add_a_comment():
    user = User('123','12345678')
    repo.add_user(user)
    user1 = repo.get_user('123')
    track = repo.get_track(2)
    review = make_review(track, user1, 3)

    repo.add_review(review)

    assert review in repo.get_reviews()


def test_repository_does_not_add_a_comment_without_a_user():
    track = repo.get_track(2)
    review = Review(track, None, 3)

    with pytest.raises(RepositoryException):
        repo.add_review(review)