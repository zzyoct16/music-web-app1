from datetime import date

import pytest

import music.utilities.services as services
import music.adapters.Repository as repo
from tests.conftest import session_factory
from flask import url_for

repo = session_factory()

def test_can_add_user():
    new_user_name = 'jz'
    new_password = 'abcd1A23'

    services.add_user(new_user_name, new_password, repo)

    user_as_dict = services.get_user(new_user_name, repo)
    assert user_as_dict['user_name'] == new_user_name

    # Check that password has been encrypted.
    assert user_as_dict['password'].startswith('pbkdf2:sha256:')


def test_authentication_with_valid_credentials():
    new_user_name = 'pmccartney'
    new_password = 'abcd1A23'

    services.add_user(new_user_name, new_password, repo)

    try:
        services.authenticate_user(new_user_name, new_password, repo)
    except services.AuthenticationException:
        assert False


def test_authentication_with_invalid_credentials():
    new_user_name = 'pmccartney'
    new_password = 'abcd1A23'

    with pytest.raises(services.AuthenticationException):
        services.authenticate_user(new_user_name, '0987654321', repo)


def test_cannot_add_comment_by_unknown_user():
    track_id = 2
    rating = 3
    user_name = 'gmichael'

    # Call the service layer to attempt to add the comment.
    with pytest.raises(services.UnknownUserException):
        services.add_review(track_id, rating, user_name, repo)


def test_can_get_tracks():
    tracks_as_dict = services.get_all_tracks(repo)
    assert len(tracks_as_dict) == 2000


def test_get_tracks_for_artist():
    artist = 'AWOL'
    tracks = services.get_tracks_for_artist(artist, repo)
    assert len(tracks) == 4

def test_get_tracks_for_album():
    album = 'Au'
    tracks = services.get_tracks_for_album(album, repo)
    assert len(tracks) == 1

def test_get_tracks_by_id():
    id_list = [2,3,5]
    tracks = services.get_tracks_by_id(id_list, repo)
    assert len(tracks) == 3
