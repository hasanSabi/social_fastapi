import pytest
from app import models

@pytest.fixture
def test_vote(setup_user, db_session, test_posts):
    vote = models.Vote(post_id=test_posts[0].id, user_id=setup_user["id"])
    db_session.add(vote)
    db_session.commit()
    yield vote
    db_session.delete(vote)
    db_session.commit()


def test_vote_post(authorized_client, test_posts):
    response = authorized_client.post(f"/vote", json={'post_id': test_posts[0].id, 'dir': 1})
    assert response.status_code == 201

def test_vote_twice_post(authorized_client, test_posts, test_vote):
    response = authorized_client.post(f"/vote/", json={'post_id': test_posts[0].id, 'dir': 1})
    assert response.status_code == 409

def test_delete_vote(authorized_client, test_posts, test_vote):
    response = authorized_client.post(f"/vote/", json={'post_id': test_posts[0].id, 'dir': 0})
    assert response.status_code == 204


def test_delete_vote_nonexistent(authorized_client, test_posts):
    response = authorized_client.post(f"/vote/", json={'post_id': test_posts[0].id, 'dir': 0})
    assert response.status_code == 404

def test_vote_post_nonexistent(authorized_client, test_posts):
    response = authorized_client.post(f"/vote/", json={'post_id': 9999, 'dir': 1})
    assert response.status_code == 404  # Post not found

def test_unauthorized_vote(test_client, test_posts):
    response = test_client.post(f"/vote/", json={'post_id': test_posts[0].id, 'dir': 1})
    assert response.status_code == 401  # Unauthorized  