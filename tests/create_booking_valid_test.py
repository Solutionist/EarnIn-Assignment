"""
Test Scenario 1: Create a flight booking with valid customer and flight details
Expected Result: Booking is successfully created. Customer name is verified via Passport API.
"""
import httpx
from tests.conftest import (
    create_booking,
    get_passengers,
    find_passenger_by_passport_id,
    assert_booking_response,
    assert_passenger_fields_match
)


def test_create_booking_with_valid_customer(api_client: httpx.Client) -> None:
    """
    Test creating a booking with valid customer details.
    The Passport API should be called and return matching names.
    """
    # Use test flight from schema.sql (Test Scenario 1)
    flight_id = "AA001"
    
    # Using static mapping from create_booking_valid.json (Test Scenario 1)
    # This mapping returns: passport_id="PP001", first_name="Sarah", last_name="Johnson"
    passport_id = "PP001"
    first_name = "Sarah"
    last_name = "Johnson"
    
    # Create booking
    response_data = create_booking(api_client, flight_id, passport_id, first_name, last_name)
    
    # Assert booking response fields
    assert_booking_response(response_data, flight_id, passport_id, first_name, last_name)
    
    # Verify the booking was created by retrieving it
    passengers = get_passengers(api_client, flight_id)
    assert len(passengers) > 0, "Booking should be created and retrievable"
    
    # Find our booking
    our_booking = find_passenger_by_passport_id(passengers, passport_id)
    assert our_booking is not None, "Created booking should be in the list"
    assert_passenger_fields_match(our_booking, first_name=first_name, last_name=last_name)
