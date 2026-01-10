"""
Test Scenario 2: Create a flight booking with invalid customer and flight details
Expected Result: Booking is not created. The Passport API returns a 'Firstname or Lastname is mismatch.' error.
"""


def test_create_booking_with_invalid_customer(api_client):
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
    assert response.status_code == 400, f"Expected 400, got {response.status_code}: {response.text}"
    
    # Verify the error message
    response_data = response.json()
    assert "detail" in response_data
    assert "Firstname or Lastname is mismatch" in response_data["detail"]
    
    # Verify the booking was NOT created
    get_response = api_client.get(f"/flights/{flight_id}/passengers")
    assert get_response.status_code == 200
    
    passengers = get_response.json()["passengers"]
    # Find our booking - should NOT exist
    our_booking = next(
        (p for p in passengers if p["passport_id"] == passport_id),
        None
    )
    assert our_booking is None, "Booking should NOT be created when names don't match"
