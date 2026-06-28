from fastapi.testclient import TestClient


def create_client(api_client: TestClient, email: str = "ana@example.com") -> dict:
    response = api_client.post(
        "/clients",
        json={"name": "Ana Perez", "email": email, "company": "Finanz"},
    )
    assert response.status_code == 201
    return response.json()


def test_create_client(api_client: TestClient) -> None:
    client = create_client(api_client)

    assert client["id"]
    assert client["name"] == "Ana Perez"
    assert client["email"] == "ana@example.com"
    assert client["company"] == "Finanz"
    assert client["created_at"]


def test_list_clients_ordered_by_creation(api_client: TestClient) -> None:
    first = create_client(api_client, "first@example.com")
    second = create_client(api_client, "second@example.com")

    response = api_client.get("/clients")

    assert response.status_code == 200
    assert [client["id"] for client in response.json()] == [first["id"], second["id"]]


def test_get_client_by_id(api_client: TestClient) -> None:
    created = create_client(api_client)

    response = api_client.get(f"/clients/{created['id']}")

    assert response.status_code == 200
    assert response.json()["id"] == created["id"]


def test_get_missing_client_returns_404(api_client: TestClient) -> None:
    response = api_client.get("/clients/00000000-0000-0000-0000-000000000000")

    assert response.status_code == 404
    assert response.json()["detail"] == "Client not found"
