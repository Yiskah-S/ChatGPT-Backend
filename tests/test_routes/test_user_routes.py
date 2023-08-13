# import json
# from app import create_app, db
# import pytest
# from app.models.user import User


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


# def test_create_user(client):
#     response = client.post('/users', json={
#         "username": "testuser",
#         "email": "short@example.com",
#         "password": "password123"
#     })

#     assert response.status_code == 201
#     user_data = json.loads(response.data)
#     assert user_data['username'] == "testuser"
#     assert user_data['email'] == "short@example.com"


# def test_create_user_missing_data(client):
#     response = client.post('/users', json={
#         "username": "testuser"
#     })

#     assert response.status_code == 400
#     error_data = json.loads(response.data)
#     assert error_data['error'] == "Incomplete user data."


# def test_create_user_existing_username(client):
#     client.post('/users', json={
#         "username": "testuser",
#         "email": "short@example.com",
#         "password": "password123"
#     })

#     response = client.post('/users', json={
#         "username": "testuser",
#         "email": "short1@example.com",
#         "password": "password123"
#     })

#     assert response.status_code == 409
#     error_data = json.loads(response.data)
#     assert error_data['error'] == "User with this username already exists."

# @pytest.mark.skip(reason="Need to implement")
# def test_password_hashing():
#     user = User(username="testuser", email="short@example.com", password="password123")
#     db.session.add(user)
#     db.session.commit()

#     saved_user = User.query.filter_by(username="testuser").first()
#     assert saved_user.password != "password123"
#     assert saved_user.verify_password("password123")
#     assert not saved_user.verify_password("wrongpassword")

# @pytest.mark.skip(reason="Need to implement")
# def test_user_deactivation():
#     user = User(username="testuser", email="short@example.com", password="password123")
#     db.session.add(user)
#     db.session.commit()
    
#     user.active = False
#     db.session.commit()

#     assert not User.query.filter_by(username="testuser").first().active

# def test_username_length_constraint():
#     with pytest.raises(Exception):
#         user = User(username="a", email="short@example.com", password="password123")
#         db.session.add(user)
#         db.session.commit()

# def test_email_validation():
#     with pytest.raises(Exception):
#         user = User(username="testuser", email="invalid-email", password="password123")
#         db.session.add(user)
#         db.session.commit()

# def test_user_to_dict():
#     user = User(username="testuser", email="short@example.com", password="password123")
#     db.session.add(user)
#     db.session.commit()

#     user_dict = user.to_dict()
#     assert user_dict['username'] == "testuser"
#     assert user_dict['email'] == "short@example.com"
#     assert user_dict['id'] == 1

# def test_user_from_dict():
#     user_dict = {
#         "username": "testuser",
#         "email": "short@example.com",
#         "password": "password123"
#     }
#     user = User.from_dict(user_dict)
#     db.session.add(user)
#     db.session.commit()

#     saved_user = User.query.filter_by(username="testuser").first()
#     assert saved_user.username == "testuser"
#     assert saved_user.email == "short@example.com"
#     assert saved_user.password != "password123"
#     assert saved_user.verify_password("password123")
#     assert not saved_user.verify_password("wrongpassword")

# def test_duplicate_email(client):
#     client.post('/users', json={
#         "username": "testuser1",
#         "email": "duplicate@example.com",
#         "password": "password123"
#     })

#     response = client.post('/users', json={
#         "username": "testuser2",
#         "email": "duplicate@example.com",
#         "password": "password123"
#     })

#     assert response.status_code == 409

# def test_duplicate_username(client):
#     client.post('/users', json={
#         "username": "duplicate",
#         "email": "short@example.com",
#         "password": "password123"
#     })

#     response = client.post('/users', json={
#         "username": "duplicate",
#         "email": "short@example.com",
#         "password": "password123",
#     })

#     assert response.status_code == 409

# def test_updating_user(client):
#     client.post('/users', json={
#         "username": "testuser",
#         "email": "testuser@example.com",
#         "password": "password123"
#     })

#     response = client.put('/users/testuser', json={
#         "email": "newemail@example.com",
#     })

#     assert response.status_code == 200
#     assert User.query.filter_by(username="testuser").first().email == "newemail@example.com"

# def test_updating_user_invalid_data(client):
#     client.post('/users', json={
#         "username": "testuser",
#         "email": "short@example.com",
#         "password": "password123"
#     })

#     response = client.put('/users/testuser', json={
#         "email": "invalid-email",
#     })  

#     assert response.status_code == 400

# def test_get_user(client):
#     client.post('/users', json={
#         "username": "testuser",
#         "email": "short@example.com",
#         "password": "password123"
#     })

#     response = client.get('/users/testuser')

#     assert response.status_code == 200
#     user_data = json.loads(response.data)
#     assert user_data['username'] == "testuser"
#     assert user_data['email'] == "short@example.com"

# def test_get_user_not_found(client):
#     response = client.get('/users/testuser')

#     assert response.status_code == 404

# def test_delete_user(client):
#     client.post('/users', json={
#         "username": "testuser",
#         "email": "short@example.com"
#     })  

#     response = client.delete('/users/testuser')

#     assert response.status_code == 200
#     assert not User.query.filter_by(username="testuser").first()

    


