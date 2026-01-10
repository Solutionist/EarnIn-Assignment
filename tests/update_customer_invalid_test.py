"""
Test Scenario 6: Attempt to update customer name with mismatched details in Passport API
Expected Result: Update fails. The Passport API returns a 'Firstname or Lastname is mismatch.' error.
"""
import httpx
from tests.conftest import (
    create_booking,
    get_passengers,
    find_passenger_by_customer_id,
    assert_mismatch_error,
    assert_passenger_fields_match
)


def test_update_customer_with_mismatched_name(api_client: httpx.Client) -> None:
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
    
    created_booking = create_booking(api_client, flight_id, initial_passport_id,
        initial_first_name, initial_last_name)
    customer_id = created_booking["customer_id"]
    
    # Step 2: Attempt to update with MISMATCHED names
    # Using static mapping from passport_invalid_customer_flight.json (DOE12345)
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
    assert_mismatch_error(update_response)
    
    # Verify the booking was NOT updated by retrieving it
    passengers = get_passengers(api_client, flight_id)
    original_passenger = find_passenger_by_customer_id(passengers, customer_id)
    assert original_passenger is not None, "Original booking should still exist"
    
    # Verify the booking still has the original values (not updated)
    assert_passenger_fields_match(
        original_passenger,
        passport_id=initial_passport_id,
        first_name=initial_first_name,
        last_name=initial_last_name
    )
