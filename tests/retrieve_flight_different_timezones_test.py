"""
Test Scenario 3: Retrieve flight details of different timezones for departure and arrival airport
Expected Result: Booking details are retrieved, departure time is converted to UK timezone (GMT),
and arrival time is converted to BKK timezone.
"""
import httpx
from tests.conftest import (
    find_flight_by_id,
    parse_datetime_string,
    assert_timezone_offset,
    assert_status_code
)


def test_retrieve_flight_with_different_timezones(api_client: httpx.Client) -> None:
    """
    Test retrieving flight details with different timezones.
    Departure time should be in UK timezone (Europe/London/GMT),
    arrival time should be in BKK timezone (Asia/Bangkok).
    """
    # Use AA003 which has (Test Scenario 3):
    # - Departure: Europe/London (GMT/UTC+0)
    # - Arrival: Asia/Bangkok (UTC+7)
    flight_id = "AA003"
    
    # Retrieve flight details (no booking creation needed - GET /flights doesn't require bookings)
    # The API converts times to the appropriate timezones automatically
    response = api_client.get("/flights")
    assert_status_code(response, 200)
    
    flights_data = response.json()
    assert "flights" in flights_data
    
    # Find our flight
    flight = find_flight_by_id(flights_data["flights"], flight_id)
    assert flight is not None, f"Flight {flight_id} should exist"
    
    # Verify flight details
    assert flight["id"] == flight_id
    assert flight["departure_airport"] == "LHR"
    assert flight["arrival_airport"] == "BKK"
    
    # Parse the datetime strings from the response
    departure_time_str = flight["departure_time"]
    arrival_time_str = flight["arrival_time"]
    
    # Convert to datetime objects
    departure_time = parse_datetime_string(departure_time_str)
    arrival_time = parse_datetime_string(arrival_time_str)
    
    # Verify departure time is in UK timezone (GMT/UTC+0)
    # The API converts to Europe/London timezone
    assert_timezone_offset(departure_time, 0, "Departure")
    
    # Verify the departure time value
    # Original: 2024-12-01T10:00:00Z (UTC)
    assert departure_time.hour == 10, f"Departure hour should be 10 in GMT, got {departure_time.hour}"
    assert departure_time.minute == 0, f"Departure minute should be 0, got {departure_time.minute}"
    assert departure_time.day == 1, f"Departure day should be 1, got {departure_time.day}"
    
    # Verify arrival time is in BKK timezone (Asia/Bangkok, UTC+7)
    assert_timezone_offset(arrival_time, 7, "Arrival")
    
    # Verify the arrival time value
    # Original: 2024-12-01T18:00:00Z (UTC)
    assert arrival_time.hour == 1, \
        f"Arrival hour should be 01:00 in BKK timezone (18:00 UTC + 7h = 01:00), got {arrival_time.hour}"
    assert arrival_time.minute == 0, f"Arrival minute should be 0, got {arrival_time.minute}"
    assert arrival_time.day == 2, f"Arrival day should be 2 (crosses midnight: 18:00 UTC + 7h = 01:00 Dec 2), got {arrival_time.day}"
