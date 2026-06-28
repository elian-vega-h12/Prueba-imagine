from typing import Any

from fastapi.testclient import TestClient


def create_client(api_client: TestClient) -> dict[str, Any]:
    response = api_client.post(
        "/clients",
        json={"name": "Maria Diaz", "email": "maria@example.com", "company": "Acme"},
    )
    assert response.status_code == 201
    return response.json()


def create_ticket(api_client: TestClient, client_id: str) -> dict[str, Any]:
    response = api_client.post(
        "/tickets",
        headers={"X-User": "agent@example.com"},
        json={
            "client_id": client_id,
            "title": "Login issue",
            "description": "The customer cannot access the portal.",
        },
    )
    assert response.status_code == 201
    return response.json()


def test_create_ticket_for_client(api_client: TestClient, audit_writer) -> None:
    client = create_client(api_client)

    ticket = create_ticket(api_client, client["id"])

    assert ticket["id"]
    assert ticket["client_id"] == client["id"]
    assert ticket["title"] == "Login issue"
    assert ticket["status"] == "Pendiente"
    assert audit_writer.events[0]["action"] == "ticket_created"
    assert audit_writer.events[0]["user"] == "agent@example.com"
    assert audit_writer.events[0]["ticket_id"] == ticket["id"]


def test_create_ticket_for_missing_client_returns_404(api_client: TestClient) -> None:
    response = api_client.post(
        "/tickets",
        json={
            "client_id": "00000000-0000-0000-0000-000000000000",
            "title": "Login issue",
            "description": "The customer cannot access the portal.",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Client not found"


def test_list_tickets_ordered_by_creation(api_client: TestClient) -> None:
    client = create_client(api_client)
    first = create_ticket(api_client, client["id"])
    second_response = api_client.post(
        "/tickets",
        json={
            "client_id": client["id"],
            "title": "Billing issue",
            "description": "The invoice has the wrong tax ID.",
        },
    )
    assert second_response.status_code == 201
    second = second_response.json()

    response = api_client.get("/tickets")

    assert response.status_code == 200
    assert [ticket["id"] for ticket in response.json()] == [first["id"], second["id"]]


def test_update_ticket_status(api_client: TestClient, audit_writer) -> None:
    client = create_client(api_client)
    ticket = create_ticket(api_client, client["id"])

    response = api_client.patch(
        f"/tickets/{ticket['id']}/status",
        headers={"X-User": "lead@example.com"},
        json={"status": "En progreso"},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "En progreso"
    status_event = audit_writer.events[-1]
    assert status_event["action"] == "ticket_status_updated"
    assert status_event["user"] == "lead@example.com"
    assert status_event["previous_status"] == "Pendiente"
    assert status_event["new_status"] == "En progreso"


def test_update_ticket_status_defaults_audit_user(api_client: TestClient, audit_writer) -> None:
    client = create_client(api_client)
    ticket = create_ticket(api_client, client["id"])

    response = api_client.patch(f"/tickets/{ticket['id']}/status", json={"status": "Finalizado"})

    assert response.status_code == 200
    assert audit_writer.events[-1]["user"] == "system"


def test_invalid_ticket_status_returns_422(api_client: TestClient) -> None:
    client = create_client(api_client)
    ticket = create_ticket(api_client, client["id"])

    response = api_client.patch(
        f"/tickets/{ticket['id']}/status",
        json={"status": "Bloqueado"},
    )

    assert response.status_code == 422


def test_update_missing_ticket_returns_404(api_client: TestClient) -> None:
    response = api_client.patch(
        "/tickets/00000000-0000-0000-0000-000000000000/status",
        json={"status": "Finalizado"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Ticket not found"
