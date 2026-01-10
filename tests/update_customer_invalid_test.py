"""
Test Scenario 6: Attempt to update customer name with mismatched details in Passport API
Expected Result: Update fails. The Passport API returns a 'Firstname or Lastname is mismatch.' error.
"""
from datetime import datetime


def test_update_customer_with_mismatched_name(api_client):
    """
    Test updating customer information with names that don't match the passport.
    The Passport API should return a mismatch error.
    """
    # Use test flight from schema.sql
    flight_id = "LHR001"
    
    # Step 1: Create a booking first (so we have something to update)
    # Using static mapping from passport_match.json (BC1500)
    initial_passport_id = "BC1500"
    initial_first_name = "Shauna"
    initial_last_name = "Davila"
    
    create_data = {
        "passport_id": initial_passport_id,
        "first_name": initial_first_name,
        "last_name": initial_last_name
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
    
    # Step 2: Attempt to update with MISMATCHED names
    # Using static mapping from passport_invalid_customer_flight.json (DOE12345)
    # This mapping returns: passport_id="DOE12345", first_name="Jane", last_name="Smith"
    # But we're sending "John Doe" which doesn't match
    updated_passport_id = "DOE12345"  # Different passport
    updated_first_name = "John"        # Different from passport's "Jane"
    updated_last_name = "Doe"          # Different from passport's "Smith"
    
    update_data = {
        "passport_id": updated_passport_id,
        "first_name": updated_first_name,
        "last_name": updated_last_name
    }
    
    # Make API call to update booking - should fail with mismatch error
    update_response = api_client.put(
        f"/flights/{flight_id}/passengers/{customer_id}",
        json=update_data,
        headers={"Content-Type": "application/json"}
    )
    
    # Assertions - update should fail with 400 and mismatch error
    assert update_response.status_code == 400, \
        f"Expected 400, got {update_response.status_code}: {update_response.text}"
    
    # Verify the error message
    error_data = update_response.json()
    assert "detail" in error_data, "Error response should contain 'detail' field"
    assert "Firstname or Lastname is mismatch" in error_data["detail"], \
        f"Error should mention mismatch, got: {error_data['detail']}"
    
    # Verify the booking was NOT updated by retrieving it
    get_response = api_client.get(f"/flights/{flight_id}/passengers")
    assert get_response.status_code == 200
    
    passengers = get_response.json()["passengers"]
    original_passenger = next(
        (p for p in passengers if p["customer_id"] == customer_id),
        None
    )
    assert original_passenger is not None, "Original booking should still exist"
    
    # Verify the booking still has the original values (not updated)
    assert original_passenger["passport_id"] == initial_passport_id, \
        f"Passport ID should remain {initial_passport_id}, got {original_passenger['passport_id']}"
    assert original_passenger["first_name"] == initial_first_name, \
        f"First name should remain {initial_first_name}, got {original_passenger['first_name']}"
    assert original_passenger["last_name"] == initial_last_name, \
        f"Last name should remain {initial_last_name}, got {original_passenger['last_name']}"
