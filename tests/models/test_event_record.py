"""
Tests for the EventRecord model.
"""
import pytest
import json
from datetime import datetime

from universal_history.models.event_record import (
    EventRecord, DomainType, ContentType, SourceType, 
    InputMethod, ProcessingMethod, RawInput, Source, Creator
)



def test_event_record_creation(sample_event_record):
    """Test creating an EventRecord."""
    # Verify the EventRecord was created with the expected values
    assert sample_event_record.subject_id is not None
    assert sample_event_record.domain_type == DomainType.EDUCATION
    assert sample_event_record.event_type == "test_event"
    assert isinstance(sample_event_record.re_id, str)
    assert isinstance(sample_event_record.timestamp, datetime)
    assert sample_event_record.current_re_hash is None  # Hash hasn't been calculated yet


def test_event_record_update_hash(sample_event_record):
    """Test updating the hash of an EventRecord."""
    # Initial state
    assert sample_event_record.current_re_hash is None
    
    # Update the hash
    sample_event_record.update_hash()
    
    # Verify the hash was updated
    assert sample_event_record.current_re_hash is not None
    assert isinstance(sample_event_record.current_re_hash, str)
    assert len(sample_event_record.current_re_hash) > 0


def test_event_record_to_dict(sample_event_record):
    """Test converting an EventRecord to a dictionary."""
    # Update the hash to ensure it's included in the dictionary
    sample_event_record.update_hash()
    
    # Convert to dictionary
    event_dict = sample_event_record.to_dict()
    
    # Verify the dictionary contains the expected keys
    assert "subject_id" in event_dict
    assert "domain_type" in event_dict
    assert "event_type" in event_dict
    assert "re_id" in event_dict
    assert "timestamp" in event_dict
    assert "current_re_hash" in event_dict
    assert "raw_input" in event_dict
    assert "source" in event_dict
    # Verify the values
    assert event_dict["subject_id"] == sample_event_record.subject_id
    assert event_dict["domain_type"] == DomainType.EDUCATION.value
    assert event_dict["event_type"] == "test_event"
    assert isinstance(event_dict["timestamp"], str)  # Should be converted to ISO format string


def test_event_record_to_json(sample_event_record):
    """Test converting an EventRecord to JSON."""
    # Update the hash to ensure it's included in the JSON
    sample_event_record.update_hash()
    
    # Convert to JSON
    event_json = sample_event_record.to_json()
    
    # Verify the JSON is valid
    event_dict = json.loads(event_json)
    
    # Verify the dictionary contains the expected keys
    assert "subject_id" in event_dict
    assert "domain_type" in event_dict
    assert "event_type" in event_dict
    
    # Verify the values
    assert event_dict["subject_id"] == sample_event_record.subject_id
    assert event_dict["domain_type"] == DomainType.EDUCATION.value
    assert event_dict["event_type"] == "test_event"


def test_event_record_from_dict(sample_organization):
    """Test creating an EventRecord from a dictionary."""
    # Create a dictionary
    event_dict = {
        "subject_id": "test-subject",
        "domain_type": "education",
        "event_type": "test_event",
        "re_id": "test-id",
        "timestamp": datetime.now().isoformat(),
        "raw_input": {
            "type": "text",
            "content": "Test content",
            "context": "Test context"
        },
        "source": {
            "type": "system",
            "id": "test-source",
            "name": "Test Source",
            "input_method": "automatic",
            "processing_method": "AI_analysis"
        }
    }
    
    # Create an EventRecord from the dictionary
    event_record = EventRecord.from_dict(event_dict)
    
    # Verify the EventRecord has the expected values
    assert event_record.subject_id == "test-subject"
    assert event_record.domain_type == DomainType.EDUCATION
    assert event_record.event_type == "test_event"
    assert event_record.re_id == "test-id"
    assert isinstance(event_record.timestamp, datetime)
    assert event_record.raw_input.content == "Test content"
    assert event_record.source.name == "Test Source"


def test_event_record_from_json():
    """Test creating an EventRecord from JSON."""
    # Create a JSON string
    event_json = json.dumps({
        "subject_id": "test-subject",
        "domain_type": "education",
        "event_type": "test_event",
        "re_id": "test-id",
        "timestamp": datetime.now().isoformat(),
        "raw_input": {
            "type": "text",
            "content": "Test content",
            "context": "Test context"
        },
        "source": {
            "type": "system",
            "id": "source-123",
            "name": "Test Source",
            "creator": {
                "id": "creator-123",
                "role": "tester",
                "name": "Test Creator",
                "qualifications": ["Testing"]
            },
            "input_method": "automatic",
            "processing_method": "AI_analysis"
        }
    })
    
    # Create an EventRecord from the JSON
    event_record = EventRecord.from_json(event_json)
    
    # Verify the EventRecord has the expected values
    assert event_record.subject_id == "test-subject"
    assert event_record.domain_type == DomainType.EDUCATION
    assert event_record.event_type == "test_event"
    assert event_record.re_id == "test-id"
    assert isinstance(event_record.timestamp, datetime)
    assert event_record.raw_input.content == "Test content"
    assert event_record.source.name == "Test Source"


def test_event_record_calculate_hash(sample_event_record):
    """Test calculating the hash of an EventRecord."""
    # Calculate the hash
    hash_value = sample_event_record.calculate_hash()
    
    # Verify the hash is a non-empty string
    assert hash_value is not None
    assert isinstance(hash_value, str)
    assert len(hash_value) > 0
    
    # Calculate the hash again
    hash_value2 = sample_event_record.calculate_hash()
    
    # Verify the hash is the same
    assert hash_value == hash_value2
    
    # Modify the EventRecord
    original_event_type = sample_event_record.event_type
    sample_event_record.event_type = "modified_event"
    
    # Calculate the hash again
    hash_value3 = sample_event_record.calculate_hash()
    
    # Verify the hash is different
    assert hash_value != hash_value3
    
    # Restore the original value
    sample_event_record.event_type = original_event_type
    
    # Calculate the hash again
    hash_value4 = sample_event_record.calculate_hash()
    
    # Verify the hash is the same as the original
    assert hash_value == hash_value4