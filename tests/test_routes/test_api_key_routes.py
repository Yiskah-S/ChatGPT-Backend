# import json
# import pytest
# from app import create_app, db
# from app.models.api_key import APIKey

# @pytest.fixture
# def client():
#     app = create_app()
#     app.config['TESTING'] = True
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

#     with app.test_client() as client:
#         with app.app_context():
#             db.create_all()
#         yield client

#         with app.app_context():
#             db.drop_all()

# def test_create_api_key(client):
#     response = client.post('/api_keys', json={
#         "api_type": "Test Type",
#         "api_key": "123456",
#         "user_id": 1
#     })
#     assert response.status_code == 201

# def test_create_api_key_without_type(client):
#     response = client.post('/api_keys', json={
#         "api_key": "123456",
#         "user_id": 1
#     })
#     assert response.status_code == 400

# def test_create_api_key_without_key(client):
#     response = client.post('/api_keys', json={
#         "api_type": "Test Type",
#         "user_id": 1
#     })
#     assert response.status_code == 400

# def test_create_api_key_without_user_id(client):
#     response = client.post('/api_keys', json={
#         "api_type": "Test Type",
#         "api_key": "123456"
#     })
#     assert response.status_code == 400

# def test_retrieve_api_key(client):
#     response = client.get('/api_keys/1')
#     assert response.status_code == 200

# def test_retrieve_non_existent_api_key(client):
#     response = client.get('/api_keys/9999')
#     assert response.status_code == 404

# def test_update_api_key(client):
#     client.put('/api_keys/1', json={"api_type": "Updated Type"})
#     response = client.get('/api_keys/1')
#     assert response.json["api_type"] == "Updated Type"

# def test_delete_api_key(client):
#     response = client.delete('/api_keys/1')
#     assert response.status_code == 204

# def test_delete_non_existent_api_key(client):
#     response = client.delete('/api_keys/9999')
#     assert response.status_code == 404

# def test_list_api_keys(client):
#     response = client.get('/api_keys')
#     assert response.status_code == 200
#     assert len(response.json) > 0

# def test_filter_api_keys_by_user(client):
#     response = client.get('/api_keys?user_id=1')
#     assert response.status_code == 200
#     assert all(api_key["user_id"] == 1 for api_key in response.json)

# def test_update_api_key_with_invalid_data(client):
#     response = client.put('/api_keys/1', json={"api_type": ""})
#     assert response.status_code == 400

# def test_api_key_length_validation(client):
#     response = client.post('/api_keys', json={
#         "api_type": "Test Type",
#         "api_key": "1" * 121,
#         "user_id": 1
#     })
#     assert response.status_code == 400

# def test_update_api_key_user_id(client):
#     client.put('/api_keys/1', json={"user_id": 2})
#     response = client.get('/api_keys/1')
#     assert response.json["user_id"] == 2

# def test_pagination_of_api_keys(client):
#     response = client.get('/api_keys?page=1&per_page=10')
#     assert response.status_code == 200
#     assert len(response.json) <= 10

# def test_sorting_api_keys_by_type(client):
#     response = client.get('/api_keys?sort=api_type')
#     assert response.status_code == 200
#     assert sorted(response.json, key=lambda x: x["api_type"]) == response.json

# def test_create_api_key_with_existing_key(client):
#     client.post('/api_keys', json={
#         "api_type": "Test Type",
#         "api_key": "123456",
#         "user_id": 1
#     })

#     response = client.post('/api_keys', json={
#         "api_type": "Test Type",
#         "api_key": "123456",
#         "user_id": 1
#     })

#     assert response.status_code == 409

# def test_retrieve_api_key_with_user(client):
#     response = client.get('/api_keys/1')
#     assert response.status_code == 200
#     assert "user_id" in response.json

# def test_update_api_key_key(client):
#     client.put('/api_keys/1', json={"api_key": "654321"})
#     response = client.get('/api_keys/1')
#     assert response.json["api_key"] == "654321"
