"""
Tests for the StateDocument model.
"""
import pytest
import json
from datetime import datetime

from universal_history.models.state_document import StateDocument, DomainState, EventReference
from universal_history.models.domain_catalog import DomainType
from universal_history.models.event_record import ContentType, SourceType, InputMethod, ProcessingMethod, RawInput, Source, Creator


def test_state_document_creation():
    """Test creating a StateDocument."""
    # Create a sample domain state
    domain_state = DomainState(
        domain_type="education",
        current_state={"status": "active", "level": "high"},
        previous_states=[{"status": "active", "level": "medium"}]
    )
    
    # Create a sample event reference
    event_ref = EventReference(
        re_id="event-123",
        timestamp=datetime.now(),
        event_type="test_event"
    )
    
    # Create a StateDocument
    state_doc = StateDocument(
        subject_id="test-subject",
        organization=sample_organization,
        domain_states=[domain_state],
        event_references=[event_ref]
    )
    
    # Verify the StateDocument was created with the expected values
    assert state_doc.subject_id == "test-subject"

    assert len(state_doc.domain_states) == 1
    assert len(state_doc.event_references) == 1
    assert state_doc.current_sd_hash is None  # Hash hasn't been calculated yet

def test_state_document_update_hash():
    """Test updating the hash of a StateDocument."""
    # Create a StateDocument
    state_doc = StateDocument(
        subject_id="test-subject",
        organization=sample_organization,
        domain_states=[],
        event_references=[]
    )
    
    # Initial state
    assert state_doc.current_sd_hash is None
    
    # Update the hash
    state_doc.update_hash()
    
    # Verify the hash was updated
    assert state_doc.current_sd_hash is not None
    assert isinstance(state_doc.current_sd_hash, str)
    assert len(state_doc.current_sd_hash) > 0

def test_state_document_to_dict():
    """Test converting a StateDocument to a dictionary."""
    # Create a StateDocument with some data
    state_doc = StateDocument(
        subject_id="test-subject",
        organization=sample_organization,
        domain_states=[],
        event_references=[]
    )
    
    # Update the hash to ensure it's included in the dictionary
    state_doc.update_hash()
    
    # Convert to dictionary
    state_dict = state_doc.to_dict()
    
    # Verify the dictionary contains the expected keys
    assert "subject_id" in state_dict
    assert "organization" in state_dict
    assert "domain_states" in state_dict
    assert "event_references" in state_dict
    assert "current_sd_hash" in state_dict
    
    # Verify the values
    assert state_dict["subject_id"] == "test-subject"
    assert state_dict["organization"]["id"] == sample_organization.id
    assert isinstance(state_dict["current_sd_hash"], str)

def test_state_document_to_json():
    """Test converting a StateDocument to JSON."""
    # Create a StateDocument with some data
    state_doc = StateDocument(
        subject_id="test-subject",
        organization=sample_organization,
        domain_states=[],
        event_references=[]
    )
    
    # Update the hash to ensure it's included in the JSON
    state_doc.update_hash()
    
    # Convert to JSON
    state_json = state_doc.to_json()
    
    # Verify the JSON is valid
    state_dict = json.loads(state_json)
    
    # Verify the dictionary contains the expected keys
    assert "subject_id" in state_dict
    assert "organization" in state_dict
    assert "current_sd_hash" in state_dict
    
    # Verify the values
    assert state_dict["subject_id"] == "test-subject"
    assert state_dict["organization"]["id"] == sample_organization.id
    assert isinstance(state_dict["current_sd_hash"], str)

def test_state_document_from_dict():
    """Test creating a StateDocument from a dictionary."""
    # Create a dictionary
    state_dict = {
        "subject_id": "test-subject",
        "organization": {
            "id": sample_organization.id,
            "name": sample_organization.name,
            "description": sample_organization.description,
            "contact_info": sample_organization.contact_info
        },
        "domain_states": [],
        "event_references": [],
        "current_sd_hash": "test-hash"
    }
    
    # Create a StateDocument from the dictionary
    state_doc = StateDocument.from_dict(state_dict)
    
    # Verify the StateDocument was created with the expected values
    assert state_doc.subject_id == "test-subject"
    assert state_doc.organization.id == sample_organization.id
    assert state_doc.domain_states == []
    assert state_doc.event_references == []
    assert state_doc.current_sd_hash == "test-hash"

def test_state_document_from_json():
    """Test creating a StateDocument from JSON."""
    # Create a JSON string
    state_json = json.dumps({
        "subject_id": "test-subject",
        "organization": {
            "id": sample_organization.id,
            "name": sample_organization.name,
            "description": sample_organization.description,
            "contact_info": sample_organization.contact_info
        },
        "domain_states": [],
        "event_references": [],
        "current_sd_hash": "test-hash"
    })
    
    # Create a StateDocument from the JSON
    state_doc = StateDocument.from_json(state_json)
    
    # Verify the StateDocument was created with the expected values
    assert state_doc.subject_id == "test-subject"
    assert state_doc.organization.id == sample_organization.id
    assert state_doc.domain_states == []
    assert state_doc.event_references == []
    assert state_doc.current_sd_hash == "test-hash"
