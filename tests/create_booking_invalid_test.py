"""
Test Scenario 2: Create a flight booking with invalid customer and flight details
Expected Result: Booking is not created. The Passport API returns a 'Firstname or Lastname is mismatch.' error.
"""
import httpx
from tests.conftest import (
    find_passenger_by_passport_id,
    get_passengers,
    assert_mismatch_error
)


def test_create_booking_with_invalid_customer(api_client: httpx.Client) -> None:
    """
    Test creating a booking with invalid customer details.
    The Passport API should be called and return a 'Firstname or Lastname is mismatch.' error.
    """
    # Use test flight from schema.sql
    flight_id = "LHR001"
    
    # Using static mapping from passport_invalid_customer_flight.json
    passport_id = "DOE12345"
    first_name = "John"
    last_name = "Doe" 
    
    # Create booking request with names that don't match the static mapping
    booking_data = {
        "passport_id": passport_id,
        "first_name": first_name,
        "last_name": last_name
    }
    
    # Make API call to create booking
    response = api_client.post(
        f"/flights/{flight_id}/passengers",
        json=booking_data,
        headers={"Content-Type": "application/json"}
    )
    
    # Assertions - should fail with 400 and mismatch error
    assert_mismatch_error(response)
    
    # Verify the booking was NOT created
    passengers = get_passengers(api_client, flight_id)
    
    # Find our booking - should NOT exist
    our_booking = find_passenger_by_passport_id(passengers, passport_id)
    assert our_booking is None, "Booking should NOT be created when names don't match"
