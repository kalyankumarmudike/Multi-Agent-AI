"""
Pytest configuration and fixtures.
"""

import pytest
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


@pytest.fixture(scope="session")
def api_base_url():
    """Get API base URL."""
    import os
    return os.getenv("API_BASE_URL", "http://localhost:8000")


@pytest.fixture(scope="session")
def sample_document():
    """Get sample document for testing."""
    return """
    Team Meeting Notes - Product Launch Planning
    
    The product team met to discuss the upcoming launch. Key decisions were made:
    
    1. Launch date is set for March 15th, 2024
    2. Marketing materials must be ready by March 1st
    3. Engineering will complete final testing by February 28th
    4. Sales team needs training materials by February 20th
    
    Open issues:
    - Budget approval is still pending from finance
    - Legal review of marketing claims not yet started
    - Third-party vendor integration timeline unclear
    
    Action items:
    - John to finalize product specifications (Due: Jan 30)
    - Sarah to coordinate with marketing agency (Due: Feb 5)
    - Mike to schedule engineering review meeting
    - Lisa to follow up with legal department
    
    Risks identified:
    - Tight timeline may not allow for adequate testing
    - External dependencies could cause delays
    - Budget constraints may limit marketing reach
    """
