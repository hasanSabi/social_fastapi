# test_comments.py
# Unit tests for comments functionality in the FastAPI application.
from http import client
import pytest
from app import models


@pytest.fixture
def test_comments(db_session, test_posts, setup_user):
    comments = [
        models.Comment(content="Comment 1", post_id=test_posts[0].id, user_id=setup_user["id"]),
        models.Comment(content="Comment 2", post_id=test_posts[0].id, user_id=setup_user["id"]),
        models.Comment(content="Comment 3", post_id=test_posts[1].id, user_id=setup_user["id"]),
    ]
    db_session.add_all(comments)
    db_session.commit()
    return comments


def test_create_comment(authorized_client, db_session, test_posts, setup_user):
    comment_data = {
        "content": "This is a test comment",
        "post_id": test_posts[0].id
    }
    response = authorized_client.post("/comment", json=comment_data)
    print(response.json())
    assert response.status_code == 201
    assert response.json()["content"] == comment_data["content"]
    assert response.json()["post_id"] == comment_data["post_id"]


def test_create_comment_post_not_found(authorized_client, db_session, setup_user):
    comment_data = {
        "content": "This is a test comment",
        "post_id": 9999  # Assuming this post ID does not exist
    }
    response = authorized_client.post("/comment", json=comment_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "Post with id 9999 not found"


def test_get_comments_for_post(authorized_client, db_session, test_posts, setup_user, test_comments):
    response = authorized_client.get(f"/comment/{test_posts[0].id}")
    assert response.status_code == 200
    assert len(response.json()) == 2  # There are 2 comments for post 0
    assert response.json()[0]["content"] == "Comment 1"
    assert response.json()[1]["content"] == "Comment 2"

def test_get_comments_for_post_no_comments(authorized_client, db_session, test_posts, setup_user):
    response = authorized_client.get(f"/comment/{test_posts[2].id}")  # Assuming post 2 has no comments
    assert response.status_code == 404
    assert response.json()["detail"] == f"No comments found for post with id: {test_posts[2].id}"

def test_get_comments_for_post_not_found(authorized_client, db_session, setup_user):
    response = authorized_client.get("/comment/9999")  # Assuming this post ID does not exist
    assert response.status_code == 404
    assert response.json()["detail"] == "No comments found for post with id: 9999"

    
 