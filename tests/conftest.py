import pytest
import httpx
import os
from typing import Dict, List, Optional, Any
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Test configuration
AIRLINE_API_URL = os.getenv("AIRLINE_API_URL", "http://localhost:8000")
WIREMOCK_URL = os.getenv("WIREMOCK_URL", "http://localhost:8081")
WIREMOCK_ADMIN_URL = f"{WIREMOCK_URL}/__admin"
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/airline")


@pytest.fixture(autouse=True)
def reset_database():
    """
    Reset database state before each test.
    Cleans up passengers and customers, but keeps flights intact.
    This ensures each test starts with a fresh state.
    """
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        session.execute(text("DELETE FROM passengers"))
        session.execute(text("DELETE FROM customers"))
        session.execute(text("ALTER SEQUENCE customers_id_seq RESTART WITH 1"))
        session.commit()
    except Exception as e:
        session.rollback()
        pass
    finally:
        session.close()
    
    yield


@pytest.fixture
def api_client():
    """HTTP client for making requests to the airline API"""
    with httpx.Client(base_url=AIRLINE_API_URL, timeout=30.0) as client:
        yield client


@pytest.fixture
def wiremock_client():
    """HTTP client for Wiremock admin API"""
    with httpx.Client(base_url=WIREMOCK_ADMIN_URL, timeout=10.0) as client:
        yield client


# Helper functions for test utilities
def find_passenger_by_passport_id(
    passengers: List[Dict[str, Any]], 
    passport_id: str
) -> Optional[Dict[str, Any]]:
    """
    Find a passenger in a list by passport_id.
    """
    for passenger in passengers:
        if passenger["passport_id"] == passport_id:
            return passenger
    return None


def find_passenger_by_customer_id(
    passengers: List[Dict[str, Any]], 
    customer_id: int
) -> Optional[Dict[str, Any]]:
    """
    Find a passenger in a list by customer_id.
    """
    for passenger in passengers:
        if passenger["customer_id"] == customer_id:
            return passenger
    return None


def create_booking(api_client: httpx.Client, flight_id: str, passport_id: str,
    first_name: str, last_name: str) -> Dict[str, str]:
    """
    Create a booking and return the response data.
    """
    booking_data: Dict[str, str] = {
        "passport_id": passport_id,
        "first_name": first_name,
        "last_name": last_name
    }
    
    response: httpx.Response = api_client.post(
        f"/flights/{flight_id}/passengers",
        json=booking_data,
        headers={"Content-Type": "application/json"}
    )
    
    assert response.status_code == 200, \
        f"Booking creation should succeed: {response.status_code}: {response.text}"
    
    return response.json()


def get_passengers(api_client: httpx.Client, flight_id: str) -> List[Dict[str, Any]]:
    """
    Get the list of passengers for a flight.
    """
    response: httpx.Response = api_client.get(f"/flights/{flight_id}/passengers")
    assert response.status_code == 200, \
        f"Expected 200, got {response.status_code}: {response.text}"
    
    return response.json()["passengers"]


def assert_booking_response(booking_data: Dict[str, Any],flight_id: str,passport_id: str,
    first_name: str, last_name: str) -> None:
    """
    Assert that a booking response contains the expected fields and values.
    """
    assert booking_data["flight_id"] == flight_id
    assert booking_data["passport_id"] == passport_id
    assert booking_data["first_name"] == first_name
    assert booking_data["last_name"] == last_name
    assert "customer_id" in booking_data
    assert isinstance(booking_data["customer_id"], int)


def assert_mismatch_error(response: httpx.Response, expected_status_code: int = 400) -> None:
    """
    Assert that a response contains a mismatch error.
    """
    assert response.status_code == expected_status_code, \
        f"Expected {expected_status_code}, got {response.status_code}: {response.text}"
    
    response_data: Dict[str, Any] = response.json()
    assert "detail" in response_data
    assert "Firstname or Lastname is mismatch" in response_data["detail"]


def find_flight_by_id(flights: List[Dict[str, Any]], flight_id: str) -> Optional[Dict[str, Any]]:
    """
    Find a flight in a list by flight ID.
    """
    for flight in flights:
        if flight["id"] == flight_id:
            return flight
    return None


def assert_passenger_fields_match(passenger: Dict[str, Any], flight_id: Optional[str] = None,
    customer_id: Optional[int] = None, passport_id: Optional[str] = None,
    first_name: Optional[str] = None, last_name: Optional[str] = None) -> None:
    """
    Assert that passenger fields match expected values.
    Only checks fields that are provided (not None).
    """
    expected_fields: Dict[str, Any] = {
        "flight_id": flight_id,
        "customer_id": customer_id,
        "passport_id": passport_id,
        "first_name": first_name,
        "last_name": last_name
    }
    
    for field_name, expected_value in expected_fields.items():
        if expected_value is not None:
            assert passenger[field_name] == expected_value, \
                f"{field_name} should be {expected_value}, got {passenger[field_name]}"