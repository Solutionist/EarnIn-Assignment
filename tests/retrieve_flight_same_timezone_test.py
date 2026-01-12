"""
Test Scenario 4: Retrieve flight details of the same timezone of departure and arrival airport (Bangkok, ICT)
Expected Result: Booking details are retrieved, and both departure time and arrival time are converted 
to the Thailand (Bangkok, ICT) timezone.
"""
import httpx
from tests.conftest import (
    find_flight_by_id,
    parse_datetime_string,
    assert_timezone_offset,
    assert_status_code
)


def test_retrieve_flight_with_same_timezone(api_client: httpx.Client) -> None:
    """
    Test retrieving flight details with same timezone for departure and arrival.
    Both departure and arrival times should be in Thailand (Bangkok, ICT) timezone.
    """
    # Use AA004 which has (Test Scenario 4):
    # - Departure: Asia/Bangkok (UTC+7)
    # - Arrival: Asia/Bangkok (UTC+7)
    flight_id = "AA004"
    
    # Retrieve flight details (no booking creation needed - GET /flights doesn't require bookings)
    response = api_client.get("/flights")
    assert_status_code(response, 200)
    
    flights_data = response.json()
    assert "flights" in flights_data
    
    # Find our flight
    flight = find_flight_by_id(flights_data["flights"], flight_id)
    assert flight is not None, f"Flight {flight_id} should exist"
    
    # Verify flight details
    assert flight["id"] == flight_id
    assert flight["departure_airport"] == "DMK"
    assert flight["arrival_airport"] == "BKK"
    
    # Parse the datetime strings from the response
    departure_time_str = flight["departure_time"]
    arrival_time_str = flight["arrival_time"]
    
    # Convert to datetime objects
    departure_time = parse_datetime_string(departure_time_str)
    arrival_time = parse_datetime_string(arrival_time_str)
    
    # Verify both departure and arrival times are in Bangkok timezone (Asia/Bangkok, UTC+7)
    assert_timezone_offset(departure_time, 7, "Departure")
    assert_timezone_offset(arrival_time, 7, "Arrival")
    
    # Verify both times are in the same timezone
    assert departure_time.tzinfo == arrival_time.tzinfo, \
        f"Both departure and arrival should be in the same timezone, got {departure_time.tzinfo} and {arrival_time.tzinfo}"
    
    # Verify the departure time value
    # Original: 2024-12-01T08:00:00Z (UTC)
    assert departure_time.hour == 15, \
        f"Departure hour should be 15 in BKK timezone (08:00 UTC + 7h = 15:00), got {departure_time.hour}"
    assert departure_time.minute == 0, f"Departure minute should be 0, got {departure_time.minute}"
    assert departure_time.day == 1, f"Departure day should be 1, got {departure_time.day}"
    
    # Verify the arrival time value
    # Original: 2024-12-01T10:00:00Z (UTC)
    assert arrival_time.hour == 17, \
        f"Arrival hour should be 17 in BKK timezone (10:00 UTC + 7h = 17:00), got {arrival_time.hour}"
    assert arrival_time.minute == 0, f"Arrival minute should be 0, got {arrival_time.minute}"
    assert arrival_time.day == 1, f"Arrival day should be 1, got {arrival_time.day}"
