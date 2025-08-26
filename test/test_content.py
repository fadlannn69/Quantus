import pytest
from fastapi.testclient import TestClient
from apk.main import app  

from apk.core.wrapper import ProtectEndpoint

# override dependency untuk bypass auth
def fake_all_access():
    return {"id": "test-content", "username": "tester"}

app.dependency_overrides[ProtectEndpoint().allAccess] = fake_all_access

client = TestClient(app)



# TEST ADD CONTENT

def test_add_content():
    response = client.post(
        "/content/AddContent",
        data={
            "title": "Testing Journal",
            "category": "OTHER",   
            "status": "DRAFT",     
            "content": "Ini adalah konten testing"
        },
    )
    print("DEBUG RESPONSE:", response.status_code, response.text) 
    assert response.status_code in [200, 201]
    data = response.json()
    assert "title" in data
    assert data["title"] == "Testing Journal"



# TEST GET ALL CONTENT

def test_get_all_content():
    response = client.get("/content/GetAllContent?limit=5&offset=0")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


# TEST GET ONE CONTENT

def test_get_one_content():
    response = client.get("/content/GetAllContent")
    content_list = response.json()
    if content_list:
        content_id = content_list[0]["id"]
        r = client.get(f"/content/GetOneContent/{content_id}")
        assert r.status_code == 200
        data = r.json()
        assert "id" in data
    else:
        pytest.skip("Tidak ada content untuk dites")

# TEST UPDATE CONTENT
def test_update_content():
    response = client.get("/content/GetAllContent")
    content_list = response.json()
    if content_list:
        content_id = content_list[0]["id"]
        r = client.put(
            f"/content/UpdateContent/{content_id}",
            data={
                "title": "Updated Journal",
                "category": "OTHER",
                "status": "DRAFT",
                "content": "Updated content"
            }
        )
        assert r.status_code == 200
        data = r.json()
        assert data["title"] == "Updated Journal"
    else:
        pytest.skip("Tidak ada content untuk dites update")

# TEST DELETE CONTENT

def test_delete_content():
    response = client.get("/content/GetAllContent")
    content_list = response.json()
    if content_list:
        content_id = content_list[-1]["id"]
        r = client.delete(f"/content/DeleteContent/{content_id}")
        assert r.status_code == 200
    else:
        pytest.skip("Tidak ada content untuk dites hapus")
