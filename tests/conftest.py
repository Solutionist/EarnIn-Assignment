import pytest
import httpx
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Test configuration
AIRLINE_API_URL = os.getenv("AIRLINE_API_URL", "http://localhost:8000")
WIREMOCK_URL = os.getenv("WIREMOCK_URL", "http://localhost:8081")
WIREMOCK_ADMIN_URL = f"{WIREMOCK_URL}/__admin"
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/airline")


@pytest.fixture(autouse=True)
def reset_database():
    """
    Reset database state before each test.
    Cleans up passengers and customers, but keeps flights intact.
    This ensures each test starts with a fresh state.
    """
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # Delete all passengers first (due to foreign key constraint)
        session.execute(text("DELETE FROM passengers"))
        # Delete all customers
        session.execute(text("DELETE FROM customers"))
        # Reset the sequence for customer IDs
        session.execute(text("ALTER SEQUENCE customers_id_seq RESTART WITH 1"))
        session.commit()
    except Exception as e:
        session.rollback()
        # If tables don't exist yet, that's okay - schema will be applied
        pass
    finally:
        session.close()
    
    yield


@pytest.fixture
def api_client():
    """HTTP client for making requests to the airline API"""
    with httpx.Client(base_url=AIRLINE_API_URL, timeout=30.0) as client:
        yield client


@pytest.fixture
def wiremock_client():
    """HTTP client for Wiremock admin API"""
    with httpx.Client(base_url=WIREMOCK_ADMIN_URL, timeout=10.0) as client:
        yield client
