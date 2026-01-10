"""
Test Scenario 1: Create a flight booking with valid customer and flight details
Expected Result: Booking is successfully created. Customer name is verified via Passport API.
"""


def test_create_booking_with_valid_customer(api_client):
    """
    Test creating a booking with valid customer details.
    The Passport API should be called and return matching names.
    """
    # Use test flight from schema.sql
    flight_id = "LHR001"
    
    # Using static mapping from passport_match.json
    # This mapping returns: passport_id="BC1500", first_name="Shauna", last_name="Davila"
    passport_id = "BC1500"
    first_name = "Shauna"
    last_name = "Davila"
    
    # Create booking request
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
    
    # Assertions
    assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
    
    response_data = response.json()
    assert response_data["flight_id"] == flight_id
    assert response_data["passport_id"] == passport_id
    assert response_data["first_name"] == first_name
    assert response_data["last_name"] == last_name
    assert "customer_id" in response_data
    assert isinstance(response_data["customer_id"], int)
    
    # Verify the booking was created by retrieving it
    get_response = api_client.get(f"/flights/{flight_id}/passengers")
    assert get_response.status_code == 200
    
    passengers = get_response.json()["passengers"]
    assert len(passengers) > 0, "Booking should be created and retrievable"
    
    # Find our booking
    our_booking = next(
        (p for p in passengers if p["passport_id"] == passport_id),
        None
    )
    assert our_booking is not None, "Created booking should be in the list"
    assert our_booking["first_name"] == first_name
    assert our_booking["last_name"] == last_name
