"""
Test Scenario 7: Delete a valid booking
Expected Result: Booking is successfully deleted from the system.
"""
import httpx
from tests.conftest import (
    create_booking,
    get_passengers,
    find_passenger_by_customer_id,
    assert_status_code
)


def test_delete_valid_booking(api_client: httpx.Client) -> None:
    """
    Test deleting a valid booking.
    The booking should be successfully removed from the system.
    """
    # Use test flight from schema.sql (Test Scenario 7)
    flight_id = "AA007"
    
    # Step 1: Create a booking first (so we have something to delete)
    # Using static mapping from delete_booking.json (Test Scenario 7)
    passport_id = "PP007"
    first_name = "David"
    last_name = "Wilson"
    
    created_booking = create_booking(api_client, flight_id, passport_id, first_name, last_name)
    customer_id = created_booking["customer_id"]
    
    # Verify the booking exists before deletion
    passengers_before = get_passengers(api_client, flight_id)
    booking_before = find_passenger_by_customer_id(passengers_before, customer_id)
    assert booking_before is not None, "Booking should exist before deletion"
    
    # Step 2: Delete the booking
    delete_response = api_client.delete(
        f"/flights/{flight_id}/passengers/{customer_id}"
    )
    
    # Assertions - delete should succeed
    assert_status_code(delete_response, 200)
    
    # Step 3: Verify the booking was deleted by trying to retrieve it
    passengers_after = get_passengers(api_client, flight_id)
    
    # The booking should no longer exist
    deleted_booking = find_passenger_by_customer_id(passengers_after, customer_id)
    assert deleted_booking is None, \
        f"Booking with customer_id {customer_id} should be deleted, but it still exists"
    
    # Verify the number of passengers decreased
    assert len(passengers_after) == len(passengers_before) - 1, \
        f"Number of passengers should decrease by 1 after deletion. Before: {len(passengers_before)}, After: {len(passengers_after)}"
    
    # Step 4: Verify attempting to delete again returns 404
    delete_again_response = api_client.delete(
        f"/flights/{flight_id}/passengers/{customer_id}"
    )
    assert_status_code(delete_again_response, 404)
