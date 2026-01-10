"""
Test Scenario 3: Retrieve flight details of different timezones for departure and arrival airport
Expected Result: Booking details are retrieved, departure time is converted to UK timezone (GMT),
and arrival time is converted to BKK timezone.
"""
from datetime import datetime


def test_retrieve_flight_with_different_timezones(api_client):
    """
    Test retrieving flight details with different timezones.
    Departure time should be in UK timezone (Europe/London/GMT),
    arrival time should be in BKK timezone (Asia/Bangkok).
    """
    # Use LHR002 which has:
    # - Departure: Europe/London (GMT/UTC+0)
    # - Arrival: Asia/Bangkok (UTC+7)
    flight_id = "LHR002"
    
    # Retrieve flight details (no booking creation needed - GET /flights doesn't require bookings)
    # The API converts times to the appropriate timezones automatically
    response = api_client.get("/flights")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
    
    flights_data = response.json()
    assert "flights" in flights_data
    
    # Find our flight
    flight = next(
        (f for f in flights_data["flights"] if f["id"] == flight_id),
        None
    )
    assert flight is not None, f"Flight {flight_id} should exist"
    
    # Verify flight details
    assert flight["id"] == flight_id
    assert flight["departure_airport"] == "LHR"
    assert flight["arrival_airport"] == "BKK"
    
    # Parse the datetime strings from the response
    departure_time_str = flight["departure_time"]
    arrival_time_str = flight["arrival_time"]
    
    # Convert to datetime objects
    if departure_time_str.endswith('Z'):
        departure_time = datetime.fromisoformat(departure_time_str.replace('Z', '+00:00'))
    else:
        departure_time = datetime.fromisoformat(departure_time_str)
    
    # Arrival should be in +07:00 format (BKK timezone)
    arrival_time = datetime.fromisoformat(arrival_time_str)
    
    # Verify departure time is in UK timezone (GMT/UTC+0)
    # The API converts to Europe/London timezone
    assert departure_time.tzinfo is not None, "Departure time should have timezone info"
    departure_offset = departure_time.utcoffset()
    assert departure_offset.total_seconds() == 0, \
        f"Departure time should be in GMT/UTC+0 (Europe/London in winter), got offset {departure_offset}"
    
    # Verify the departure time value
    # Original: 2024-12-01T10:00:00Z (UTC)
    assert departure_time.hour == 10, f"Departure hour should be 10 in GMT, got {departure_time.hour}"
    assert departure_time.minute == 0, f"Departure minute should be 0, got {departure_time.minute}"
    assert departure_time.day == 1, f"Departure day should be 1, got {departure_time.day}"
    
    # Verify arrival time is in BKK timezone (Asia/Bangkok, UTC+7)
    assert arrival_time.tzinfo is not None, "Arrival time should have timezone info"
    # Check that it's in Asia/Bangkok timezone (UTC+7)
    arrival_offset = arrival_time.utcoffset()
    assert arrival_offset.total_seconds() == 7 * 3600, \
        f"Arrival time should be in Asia/Bangkok timezone (UTC+7), got offset {arrival_offset}"
    
    # Verify the arrival time value
    # Original: 2024-12-01T18:00:00Z (UTC)
    assert arrival_time.hour == 1, \
        f"Arrival hour should be 01:00 in BKK timezone (18:00 UTC + 7h = 01:00), got {arrival_time.hour}"
    assert arrival_time.minute == 0, f"Arrival minute should be 0, got {arrival_time.minute}"
    assert arrival_time.day == 2, f"Arrival day should be 2 (crosses midnight: 18:00 UTC + 7h = 01:00 Dec 2), got {arrival_time.day}"
