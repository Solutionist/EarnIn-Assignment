"""
Test Scenario 5: Update customer contact information and flight details
Expected Result: Customer information is successfully updated, and name is verified via Passport API.
"""
from datetime import datetime


def test_update_customer_information(api_client):
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
    assert "flight_id" in updated_booking, "Response should contain flight_id"
    assert "customer_id" in updated_booking, "Response should contain customer_id"
    assert "passport_id" in updated_booking, "Response should contain passport_id"
    assert "first_name" in updated_booking, "Response should contain first_name"
    assert "last_name" in updated_booking, "Response should contain last_name"
    
    # Verify all field values
    assert updated_booking["flight_id"] == flight_id, \
        f"flight_id should be {flight_id}, got {updated_booking['flight_id']}"
    assert updated_booking["customer_id"] == customer_id, \
        f"customer_id should be {customer_id}, got {updated_booking['customer_id']}"
    assert updated_booking["passport_id"] == updated_passport_id, \
        f"passport_id should be {updated_passport_id}, got {updated_booking['passport_id']}"
    assert updated_booking["first_name"] == updated_first_name, \
        f"first_name should be {updated_first_name}, got {updated_booking['first_name']}"
    assert updated_booking["last_name"] == updated_last_name, \
        f"last_name should be {updated_last_name}, got {updated_booking['last_name']}"
    
    # Verify the booking was updated by retrieving it
    get_response = api_client.get(f"/flights/{flight_id}/passengers")
    assert get_response.status_code == 200
    
    passengers = get_response.json()["passengers"]
    updated_passenger = next(
        (p for p in passengers if p["customer_id"] == customer_id),
        None
    )
    assert updated_passenger is not None, "Updated booking should be in the list"
    
    # Verify all fields in the retrieved booking
    assert updated_passenger["flight_id"] == flight_id, \
        f"Retrieved flight_id should be {flight_id}, got {updated_passenger['flight_id']}"
    assert updated_passenger["customer_id"] == customer_id, \
        f"Retrieved customer_id should be {customer_id}, got {updated_passenger['customer_id']}"
    assert updated_passenger["passport_id"] == updated_passport_id, \
        f"Retrieved passport_id should be {updated_passport_id}, got {updated_passenger['passport_id']}"
    assert updated_passenger["first_name"] == updated_first_name, \
        f"Retrieved first_name should be {updated_first_name}, got {updated_passenger['first_name']}"
    assert updated_passenger["last_name"] == updated_last_name, \
        f"Retrieved last_name should be {updated_last_name}, got {updated_passenger['last_name']}"
