from fastapi.testclient import TestClient
from main import app, Ticket
import pytest

client = TestClient(app)

def test_index():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Message": "Welcome to the Ticket Booking System"}

def test_get_tickets_empty():
    response = client.get("/tickets")
    assert response.status_code == 200
    assert response.json() == []

def test_add_ticket():
    ticket_data = {
        "id": 1,
        "flight_name": "AirX Flight 101",
        "flight_date": "2025-10-15",
        "flight_time": "14:30",
        "destination": "New York"
    }
    response = client.post("/ticket", json=ticket_data)
    assert response.status_code == 200
    assert response.json() == ticket_data

def test_get_tickets_after_adding():
    ticket_data = {
        "id": 2,
        "flight_name": "AirX Flight 102",
        "flight_date": "2025-10-16",
        "flight_time": "15:00",
        "destination": "London"
    }
    client.post("/ticket", json=ticket_data)
    response = client.get("/tickets")
    assert response.status_code == 200
    assert len(response.json()) > 0
    assert any(ticket["id"] == 2 for ticket in response.json())

def test_update_ticket():
    ticket_data = {
        "id": 3,
        "flight_name": "AirX Flight 103",
        "flight_date": "2025-10-17",
        "flight_time": "16:00",
        "destination": "Paris"
    }
    client.post("/ticket", json=ticket_data)
    updated_ticket = {
        "id": 3,
        "flight_name": "AirX Flight 104",
        "flight_date": "2025-10-18",
        "flight_time": "17:00",
        "destination": "Tokyo"
    }
    response = client.put("/ticket/3", json=updated_ticket)
    assert response.status_code == 200
    assert response.json() == updated_ticket

def test_update_nonexistent_ticket():
    updated_ticket = {
        "id": 999,
        "flight_name": "AirX Flight 999",
        "flight_date": "2025-10-19",
        "flight_time": "18:00",
        "destination": "Sydney"
    }
    response = client.put("/ticket/999", json=updated_ticket)
    assert response.status_code == 200
    assert response.json() == {"error": "Ticket Not Found"}

def test_delete_ticket():
    ticket_data = {
        "id": 4,
        "flight_name": "AirX Flight 105",
        "flight_date": "2025-10-20",
        "flight_time": "19:00",
        "destination": "Berlin"
    }
    client.post("/ticket", json=ticket_data)
    response = client.delete("/ticket/4")
    assert response.status_code == 200
    assert response.json() == ticket_data

def test_delete_nonexistent_ticket():
    response = client.delete("/ticket/999")
    assert response.status_code == 200
    assert response.json() == {"error": "Ticket not found, deletion failed"}