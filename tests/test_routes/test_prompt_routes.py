# import json
# from app import create_app, db
# import pytest
# from app.models.prompt import Prompt

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

# def test_create_prompt(client):
#     response = client.post('/prompts', json={
#         "title": "Test Prompt",
#         "category": "Test Category",
#         "prompt": "This is a test prompt."
#     })

#     assert response.status_code == 201
# def test_create_prompt_without_title(client):
#     response = client.post('/prompts', json={
#         "category": "Test Category",
#         "prompt": "This is a test prompt."
#     })

#     assert response.status_code == 400
# def test_create_prompt_without_category(client):
#     response = client.post('/prompts', json={
#         "title": "Test Prompt",
#         "prompt": "This is a test prompt."
#     })

#     assert response.status_code == 400
# def test_create_prompt_without_prompt_text(client):
#     response = client.post('/prompts', json={
#         "title": "Test Prompt",
#         "category": "Test Category"
#     })

#     assert response.status_code == 400
# def test_retrieving_prompt(client):
#     response = client.get('/prompts/1')
#     assert response.status_code == 200
# def test_retrieving_non_existent_prompt(client):
#     response = client.get('/prompts/9999')
#     assert response.status_code == 404
# def test_updating_prompt_title(client):
#     client.put('/prompts/1', json={"title": "Updated Title"})
#     response = client.get('/prompts/1')
#     assert response.json["title"] == "Updated Title"
# def test_deleting_prompt(client):
#     response = client.delete('/prompts/1')
#     assert response.status_code == 204
# def test_deleting_non_existent_prompt(client):
#     response = client.delete('/prompts/9999')
#     assert response.status_code == 404
# def test_listing_prompts(client):
#     response = client.get('/prompts')
#     assert response.status_code == 200
#     assert len(response.json) > 0
# def test_filtering_prompts_by_category(client):
#     response = client.get('/prompts?category=Test Category')
#     assert response.status_code == 200
#     assert all(prompt["category"] == "Test Category" for prompt in response.json)
# def test_updating_prompt_with_invalid_data(client):
#     response = client.put('/prompts/1', json={"title": ""})
#     assert response.status_code == 400
# def test_prompt_response_relation(client):
#     response = client.get('/prompts/1')
#     assert response.status_code == 200
#     assert "responses" in response.json
# def test_create_prompt_with_long_text(client):
#     response = client.post('/prompts', json={
#         "title": "Test Prompt",
#         "category": "Test Category",
#         "prompt": "A" * 5001
#     })

#     assert response.status_code == 400
# def test_updating_prompt_category(client):
#     client.put('/prompts/1', json={"category": "Updated Category"})
#     response = client.get('/prompts/1')
#     assert response.json["category"] == "Updated Category"
# def test_pagination_of_prompts(client):
#     response = client.get('/prompts?page=1&per_page=10')
#     assert response.status_code == 200
#     assert len(response.json) <= 10
# def test_sorting_prompts_by_title(client):
#     response = client.get('/prompts?sort=title')
#     assert response.status_code == 200
#     assert sorted(response.json, key=lambda x: x["title"]) == response.json
# def test_create_prompt_without_user_id(client):
#     response = client.post('/prompts', json={
#         "title": "Test Prompt",
#         "category": "Test Category",
#         "prompt": "This is a test prompt."
#     })

#     assert response.status_code == 400
# def test_retrieving_prompt_with_responses(client):
#     response = client.get('/prompts/1')
#     assert response.status_code == 200
#     assert "responses" in response.json
# def test_create_prompt_with_existing_title(client):
#     client.post('/prompts', json={
#         "title": "Test Prompt",
#         "category": "Test Category",
#         "prompt": "This is a test prompt."
#     })

#     response = client.post('/prompts', json={
#         "title": "Test Prompt",
#         "category": "Test Category",
#         "prompt": "This is another test prompt."
#     })

#     assert response.status_code == 409
