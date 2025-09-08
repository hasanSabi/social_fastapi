import pytest

def test_get_all_posts(authorized_client, test_posts):
    response = authorized_client.get("/posts/")
    assert response.status_code == 200
    assert len(response.json()) == len(test_posts)


def test_unauthorized_user_get_all_posts(test_client, test_posts):
    response = test_client.get("/posts/")
    assert response.status_code == 401

def test_unauthorized_user_get_one_post(test_client, test_posts):
    response = test_client.get(f"/posts/{test_posts[0].id}")
    assert response.status_code == 401

def test_get_nonexistent_post(authorized_client, test_posts):
    response = authorized_client.get("/posts/9999")
    assert response.status_code == 404

def test_get_one_post(authorized_client, test_posts):
    response = authorized_client.get(f"/posts/{test_posts[0].id}")
    assert response.status_code == 200
    post = response.json()
    assert post["Post"]["id"] == test_posts[0].id
    assert post["Post"]["title"] == test_posts[0].title
    assert post["Post"]["content"] == test_posts[0].content
    assert post["Post"]["owner_id"] == test_posts[0].owner_id
    assert post["Post"]["published"] == test_posts[0].published

@pytest.mark.parametrize("title, content, published", [
    ("New Post 1", "Content 1", True),
    ("New Post 2", "Content 2", False),
])
def test_create_post(authorized_client, setup_user, title, content, published):
    response = authorized_client.post("/posts/", json={"title": title, "content": content, "published": published})
    assert response.status_code == 201
    post = response.json()
    assert post["title"] == title
    assert post["content"] == content   
    assert post["owner_id"] == setup_user["id"]
    assert post["published"] == published


def test_unauthorized_user_create_post(test_client):
    response = test_client.post("/posts/", json={"title": "New Post", "content": "New Content"})
    assert response.status_code == 401  # Unauthorized 


def test_update_post(authorized_client, test_posts):
    post_id = test_posts[0].id
    response = authorized_client.put(f"/posts/{post_id}", json={"title": "Updated Title", "content": "Updated Content", "published": False})
    assert response.status_code == 202
    updated_post = response.json()
    assert updated_post["title"] == "Updated Title"
    assert updated_post["content"] == "Updated Content"
    assert updated_post["published"] == False

def test_unauthorized_user_update_post(test_client, test_posts):
    post_id = test_posts[0].id
    response = test_client.put(f"/posts/{post_id}", json={"title": "Updated Title", "content": "Updated Content"})
    assert response.status_code == 401  # Unauthorized

def test_update_other_user_post(authorized_client, test_posts, db_session):
    # Create a new user
    response = authorized_client.put(f"/posts/{test_posts[3].id}", json={"title": "Hacked Title", "content": "Hacked Content"})
    assert response.status_code == 403  # Forbidden

def test_delete_post(authorized_client, test_posts):
    post_id = test_posts[0].id
    response = authorized_client.delete(f"/posts/{post_id}")
    assert response.status_code == 204
    # Verify the post is deleted
    get_response = authorized_client.get(f"/posts/{post_id}")
    assert get_response.status_code == 404
    

def test_unauthorized_user_delete_post(test_client, test_posts):
    post_id = test_posts[0].id
    response = test_client.delete(f"/posts/{post_id}")
    assert response.status_code == 401  # Unauthorized


def test_delete_other_user_post(authorized_client, test_posts, db_session):
    response = authorized_client.delete(f"/posts/{test_posts[3].id}")
    assert response.status_code == 403  # Forbidden
    

def test_delete_nonexistent_post(authorized_client):
    response = authorized_client.delete("/posts/9999")
    assert response.status_code == 404


def test_update_nonexistent_post(authorized_client):
    response = authorized_client.put("/posts/9999", json={"title": "Updated Title", "content": "Updated Content"})
    assert response.status_code == 404


