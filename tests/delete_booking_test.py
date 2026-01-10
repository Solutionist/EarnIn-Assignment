"""
Test Scenario 7: Delete a valid booking
Expected Result: Booking is successfully deleted from the system.
"""
from datetime import datetime


def test_delete_valid_booking(api_client):
    """
    Test deleting a valid booking.
    The booking should be successfully removed from the system.
    """
    # Use test flight from schema.sql
    flight_id = "LHR001"
    
    # Step 1: Create a booking first (so we have something to delete)
    # Using static mapping from passport_match.json (BC1500)
    passport_id = "BC1500"
    first_name = "Shauna"
    last_name = "Davila"
    
    create_data = {
        "passport_id": passport_id,
        "first_name": first_name,
        "last_name": last_name
    }
    
    create_response = api_client.post(
        f"/flights/{flight_id}/passengers",
        json=create_data,
        headers={"Content-Type": "application/json"}
    )
    assert create_response.status_code == 200, \
        f"Booking creation should succeed: {create_response.status_code}: {create_response.text}"
    
    created_booking = create_response.json()
    customer_id = created_booking["customer_id"]
    
    # Verify the booking exists before deletion
    get_response_before = api_client.get(f"/flights/{flight_id}/passengers")
    assert get_response_before.status_code == 200
    
    passengers_before = get_response_before.json()["passengers"]
    booking_before = next(
        (p for p in passengers_before if p["customer_id"] == customer_id),
        None
    )
    assert booking_before is not None, "Booking should exist before deletion"
    
    # Step 2: Delete the booking
    delete_response = api_client.delete(
        f"/flights/{flight_id}/passengers/{customer_id}"
    )
    
    # Assertions - delete should succeed
    assert delete_response.status_code == 200, \
        f"Expected 200, got {delete_response.status_code}: {delete_response.text}"
    
    # Step 3: Verify the booking was deleted by trying to retrieve it
    get_response_after = api_client.get(f"/flights/{flight_id}/passengers")
    assert get_response_after.status_code == 200
    
    passengers_after = get_response_after.json()["passengers"]
    
    # The booking should no longer exist
    deleted_booking = next(
        (p for p in passengers_after if p["customer_id"] == customer_id),
        None
    )
    assert deleted_booking is None, \
        f"Booking with customer_id {customer_id} should be deleted, but it still exists"
    
    # Verify the number of passengers decreased
    assert len(passengers_after) == len(passengers_before) - 1, \
        f"Number of passengers should decrease by 1 after deletion. Before: {len(passengers_before)}, After: {len(passengers_after)}"
    
    # Step 4: Verify attempting to delete again returns 404
    delete_again_response = api_client.delete(
        f"/flights/{flight_id}/passengers/{customer_id}"
    )
    assert delete_again_response.status_code == 404, \
        f"Deleting non-existent booking should return 404, got {delete_again_response.status_code}"
