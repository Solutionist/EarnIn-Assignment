"""
Test Scenario 5: Update customer contact information and flight details
Expected Result: Customer information is successfully updated, and name is verified via Passport API.
"""
import httpx
from tests.conftest import (
    create_booking,
    get_passengers,
    find_passenger_by_customer_id,
    assert_passenger_fields_match
)


def test_update_customer_information(api_client: httpx.Client) -> None:
    """
    Test updating customer contact information.
    The Passport API should be called to verify the updated names.
    """
    # Use test flight from schema.sql
    flight_id = "LHR001"
    
    # Step 1: Create a booking first (so we have something to update)
    initial_passport_id = "BC1500"
    initial_first_name = "Shauna"
    initial_last_name = "Davila"
    
    created_booking = create_booking(api_client, flight_id, initial_passport_id, 
        initial_first_name, initial_last_name)
    customer_id = created_booking["customer_id"]
    
    # Step 2: Update the customer information to DIFFERENT values
    updated_passport_id = "UPDATE001"
    updated_first_name = "Alice"
    updated_last_name = "Johnson"
    
    update_data = {
        "passport_id": updated_passport_id,
        "first_name": updated_first_name,
        "last_name": updated_last_name
    }
    
    # Make API call to update booking
    # flight_id and customer_id are in the URL path to identify which passenger to update
    update_response = api_client.put(
        f"/flights/{flight_id}/passengers/{customer_id}",
        json=update_data,
        headers={"Content-Type": "application/json"}
    )
    
    # Assertions - update should succeed
    assert update_response.status_code == 200, \
        f"Expected 200, got {update_response.status_code}: {update_response.text}"
    
    updated_booking = update_response.json()
    
    # Verify ALL fields in the response are correct
    assert_passenger_fields_match(
        updated_booking, 
        flight_id=flight_id, 
        customer_id=customer_id,
        passport_id=updated_passport_id,
        first_name=updated_first_name,
        last_name=updated_last_name
    )
    
    # Verify the booking was updated by retrieving it
    passengers = get_passengers(api_client, flight_id)
    updated_passenger = find_passenger_by_customer_id(passengers, customer_id)
    assert updated_passenger is not None, "Updated booking should be in the list"
    
    # Verify all fields in the retrieved booking
    assert_passenger_fields_match(
        updated_passenger,
        flight_id=flight_id,
        customer_id=customer_id,
        passport_id=updated_passport_id,
        first_name=updated_first_name,
        last_name=updated_last_name
    )
