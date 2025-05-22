"""
Tests for the validation module.
"""
import pytest
from datetime import datetime

from universal_history.models.event_record import DomainType, ContentType, SourceType, ConfidentialityLevel
from universal_history.utils.validation import (
    validate_required_fields, validate_event_record, validate_synthesis,
    validate_state_document, validate_domain_catalog, is_valid_iso_date,
    is_valid_domain_type, get_valid_domain_types
)


def test_validate_required_fields():
    """Test validating required fields."""
    # Create a test dictionary
    data = {
        "field1": "value1",
        "field2": "value2",
        "field3": None,
        # field4 is missing
    }
    
    # Validate required fields
    missing_fields = validate_required_fields(data, ["field1", "field2", "field3", "field4"])
    
    # Verify the result
    assert isinstance(missing_fields, list)
    assert len(missing_fields) == 2
    assert "field3" in missing_fields
    assert "field4" in missing_fields


def test_validate_required_fields_all_present():
    """Test validating required fields when all are present."""
    # Create a test dictionary
    data = {
        "field1": "value1",
        "field2": "value2"
    }
    
    # Validate required fields
    missing_fields = validate_required_fields(data, ["field1", "field2"])
    
    # Verify the result
    assert isinstance(missing_fields, list)
    assert len(missing_fields) == 0


def test_validate_event_record():
    """Test validating an event record."""
    # Create a test event record
    event_data = {
        "subject_id": "test-subject",
        "domain_type": "education",
        "event_type": "test_event",
        "raw_input": {
            "type": "text",
            "content": "Test content"
        },
        "source": {
            "type": "system",
            "id": "test-source",
            "name": "Test Source"
        }
    }
    
    # Validate the event record
    errors = validate_event_record(event_data)
    
    # Verify the result
    assert isinstance(errors, dict)
    assert len(errors) == 0


def test_validate_event_record_missing_fields():
    """Test validating an event record with missing fields."""
    # Create a test event record with missing fields
    event_data = {
        "subject_id": "test-subject",
        "domain_type": "education",
        # event_type is missing
        "raw_input": {
            "type": "text",
            # content is missing
        },
        # source is missing
    }
    
    # Validate the event record
    errors = validate_event_record(event_data)
    
    # Verify the result
    assert isinstance(errors, dict)
    assert len(errors) > 0
    assert "required_fields" in errors
    assert any("event_type" in msg for msg in errors["required_fields"])
    assert any("source" in msg for msg in errors["required_fields"])


def test_validate_event_record_invalid_domain_type():
    """Test validating an event record with an invalid domain type."""
    # Create a test event record with an invalid domain type
    event_data = {
        "subject_id": "test-subject",
        "domain_type": "invalid_domain",
        "event_type": "test_event",
        "raw_input": {
            "type": "text",
            "content": "Test content"
        },
        "source": {
            "type": "system",
            "id": "test-source",
            "name": "Test Source"
        }
    }
    
    # Validate the event record
    errors = validate_event_record(event_data)
    
    # Verify the result
    assert isinstance(errors, dict)
    assert len(errors) > 0
    assert "domain_type" in errors
    assert any("Invalid domain type" in msg for msg in errors["domain_type"])


def test_validate_event_record_invalid_raw_input():
    """Test validating an event record with an invalid raw input."""
    # Create a test event record with an invalid raw input
    event_data = {
        "subject_id": "test-subject",
        "domain_type": "education",
        "event_type": "test_event",
        "raw_input": "not_a_dict",  # Should be a dictionary
        "source": {
            "type": "system",
            "id": "test-source",
            "name": "Test Source"
        }
    }
    
    # Validate the event record
    errors = validate_event_record(event_data)
    
    # Verify the result
    assert isinstance(errors, dict)
    assert len(errors) > 0
    assert "raw_input" in errors
    assert any("must be a dictionary" in msg for msg in errors["raw_input"])


def test_validate_synthesis():
    """Test validating a trajectory synthesis."""
    # Create a test synthesis
    synthesis_data = {
        "subject_id": "test-subject",
        "domain_type": "education",
        "time_frame": {
            "start": "2023-01-01T00:00:00",
            "end": "2023-01-31T23:59:59"
        },
        "summary": "Test summary"
    }
    
    # Validate the synthesis
    errors = validate_synthesis(synthesis_data)
    
    # Verify the result
    assert isinstance(errors, dict)
    assert len(errors) == 0


def test_validate_synthesis_missing_fields():
    """Test validating a trajectory synthesis with missing fields."""
    # Create a test synthesis with missing fields
    synthesis_data = {
        "subject_id": "test-subject",
        "domain_type": "education",
        # time_frame is missing
        # summary is missing
    }
    
    # Validate the synthesis
    errors = validate_synthesis(synthesis_data)
    
    # Verify the result
    assert isinstance(errors, dict)
    assert len(errors) > 0
    assert "required_fields" in errors
    assert any("time_frame" in msg for msg in errors["required_fields"])
    assert any("summary" in msg for msg in errors["required_fields"])


def test_validate_synthesis_invalid_domain_type():
    """Test validating a trajectory synthesis with an invalid domain type."""
    # Create a test synthesis with an invalid domain type
    synthesis_data = {
        "subject_id": "test-subject",
        "domain_type": "invalid_domain",
        "time_frame": {
            "start": "2023-01-01T00:00:00",
            "end": "2023-01-31T23:59:59"
        },
        "summary": "Test summary"
    }
    
    # Validate the synthesis
    errors = validate_synthesis(synthesis_data)
    
    # Verify the result
    assert isinstance(errors, dict)
    assert len(errors) > 0
    assert "domain_type" in errors
    assert any("Invalid domain type" in msg for msg in errors["domain_type"])


def test_validate_synthesis_invalid_time_frame():
    """Test validating a trajectory synthesis with an invalid time frame."""
    # Create a test synthesis with an invalid time frame
    synthesis_data = {
        "subject_id": "test-subject",
        "domain_type": "education",
        "time_frame": {
            "start": "2023-01-31T23:59:59",  # End date before start date
            "end": "2023-01-01T00:00:00"
        },
        "summary": "Test summary"
    }
    
    # Validate the synthesis
    errors = validate_synthesis(synthesis_data)
    
    # Verify the result
    assert isinstance(errors, dict)
    assert len(errors) > 0
    assert "time_frame" in errors
    assert any("End date must be after start date" in msg for msg in errors["time_frame"])


def test_validate_state_document():
    """Test validating a state document."""
    # Create a test state document
    state_data = {
        "subject_id": "test-subject",
        "general_summary": "Test summary",
        "domains": {
            "education": {
                "last_updated": "2023-01-01T00:00:00",
                "current_status": "active"
            }
        }
    }
    
    # Validate the state document
    errors = validate_state_document(state_data)
    
    # Verify the result
    assert isinstance(errors, dict)
    assert len(errors) == 0


def test_validate_state_document_missing_fields():
    """Test validating a state document with missing fields."""
    # Create a test state document with missing fields
    state_data = {
        "subject_id": "test-subject",
        # general_summary is missing
        # domains is missing
    }
    
    # Validate the state document
    errors = validate_state_document(state_data)
    
    # Verify the result
    assert isinstance(errors, dict)
    assert len(errors) > 0
    assert "required_fields" in errors
    assert any("general_summary" in msg for msg in errors["required_fields"])
    assert any("domains" in msg for msg in errors["required_fields"])


def test_validate_state_document_invalid_domains():
    """Test validating a state document with invalid domains."""
    # Create a test state document with invalid domains
    state_data = {
        "subject_id": "test-subject",
        "general_summary": "Test summary",
        "domains": {
            "education": {
                # last_updated is missing
                "current_status": "active"
            }
        }
    }
    
    # Validate the state document
    errors = validate_state_document(state_data)
    
    # Verify the result
    assert isinstance(errors, dict)
    assert len(errors) > 0
    assert "domains" in errors
    assert any("Missing required field in domain education: last_updated" in msg for msg in errors["domains"])


def test_validate_domain_catalog():
    """Test validating a domain catalog."""
    # Create a test domain catalog
    catalog_data = {
        "domain_type": "education",
        "organization": {
            "id": "org-id",
            "name": "Test Organization"
        }
    }
    
    # Validate the domain catalog
    errors = validate_domain_catalog(catalog_data)
    
    # Verify the result
    assert isinstance(errors, dict)
    assert len(errors) == 0


def test_validate_domain_catalog_missing_fields():
    """Test validating a domain catalog with missing fields."""
    # Create a test domain catalog with missing fields
    catalog_data = {
        "domain_type": "education",
        # organization is missing
    }
    
    # Validate the domain catalog
    errors = validate_domain_catalog(catalog_data)
    
    # Verify the result
    assert isinstance(errors, dict)
    assert len(errors) > 0
    assert "required_fields" in errors
    assert any("organization" in msg for msg in errors["required_fields"])


def test_validate_domain_catalog_invalid_domain_type():
    """Test validating a domain catalog with an invalid domain type."""
    # Create a test domain catalog with an invalid domain type
    catalog_data = {
        "domain_type": "invalid_domain",
        "organization": {
            "id": "org-id",
            "name": "Test Organization"
        }
    }
    
    # Validate the domain catalog
    errors = validate_domain_catalog(catalog_data)
    
    # Verify the result
    assert isinstance(errors, dict)
    assert len(errors) > 0
    assert "domain_type" in errors
    assert any("Invalid domain type" in msg for msg in errors["domain_type"])


def test_validate_domain_catalog_invalid_organization():
    """Test validating a domain catalog with an invalid organization."""
    # Create a test domain catalog with an invalid organization
    catalog_data = {
        "domain_type": "education",
        "organization": {
            "id": "org-id",
            # name is missing
        }
    }
    
    # Validate the domain catalog
    errors = validate_domain_catalog(catalog_data)
    
    # Verify the result
    assert isinstance(errors, dict)
    assert len(errors) > 0
    assert "organization" in errors
    assert any("Missing required field in organization: name" in msg for msg in errors["organization"])


def test_is_valid_iso_date():
    """Test checking if a string is a valid ISO format date."""
    # Test with valid and invalid date strings
    assert is_valid_iso_date("2023-01-01T00:00:00") is True
    assert is_valid_iso_date("invalid-date") is False
    assert is_valid_iso_date("2023-13-01T00:00:00") is False  # Invalid month
    assert is_valid_iso_date(None) is False


def test_is_valid_domain_type():
    """Test checking if a string is a valid domain type."""
    # Test with valid and invalid domain types
    assert is_valid_domain_type("education") is True
    assert is_valid_domain_type("health") is True
    assert is_valid_domain_type("invalid_domain") is False


def test_get_valid_domain_types():
    """Test getting the set of valid domain types."""
    # Get the valid domain types
    domain_types = get_valid_domain_types()
    
    # Verify the result
    assert isinstance(domain_types, set)
    assert len(domain_types) > 0
    assert "education" in domain_types
    assert "health" in domain_types
    assert "work" in domain_types