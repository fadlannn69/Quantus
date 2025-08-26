from sqlmodel import select
from apk.model.model_user import User
from apk.database.session import engine
from apk.core.auth import AuthHandler

auth_handler = AuthHandler()

# Helper Functions
def get_user_by_name(username: str):
    from sqlmodel import Session
    with Session(engine) as session:
        return session.exec(select(User).where(User.nama == username)).first()

def register_user(client, username="testuser", password="Testpass1!", role="user"):
    response = client.post("/user/Register", json={
        "nama": username,
        "password": password,
        "roles": role
    })
    assert response.status_code in [200, 201]
    user = get_user_by_name(username)
    assert user is not None
    return {"id": user.id, "nama": user.nama, "roles": user.roles}

def login_user(client, username="testuser", password="Testpass1!"):
    response = client.post("/user/Login", data={
        "username": username,
        "password": password
    })
    assert response.status_code == 200
    return response.json()["access_token"]

# User Tests
def test_register_login_user(client):
    user = register_user(client)
    token = login_user(client)
    assert isinstance(token, str)

def test_get_user(client):
    user = get_user_by_name("testuser")
    token = login_user(client, "Admin", "QuantusTelematika")
    response = client.get(
        f"/user/GetOneUser/{user.id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    
def test_update_user(client):
    user = register_user(client, "updateuser", "Update123!")
    token = login_user(client, "updateuser", "Update123!")
    response = client.put(
        f"/user/UpdateUser/{user['id']}",
        data={"nama": "updateduser", "password": "Newpass123!"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["nama"] == "updateduser"

    new_token = login_user(client, "updateduser", "Newpass123!")
    assert isinstance(new_token, str)

def test_delete_user(client):
    user = register_user(client, "deleteuser", "Delete123!")
    token = login_user(client, "deleteuser", "Delete123!")
    response = client.delete(
        f"/user/DeleteUser/{user['id']}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200

# ==========================
# Edge Cases
def test_invalid_login(client):
    response = client.post(
        "/user/Login",
        data={"username": "wrong", "password": "wrong"}
    )
    assert response.status_code == 401  # Unauthorized  

def test_invalid_jwt(client):
    user = register_user(client, "jwtuser", "Jwtpass1!")
    response = client.get(
        f"/user/GetOneUser/{user['id']}",
        headers={"Authorization": "Bearer wrongtoken"}
    )
    assert response.status_code == 401  # JWT invalid = 401
