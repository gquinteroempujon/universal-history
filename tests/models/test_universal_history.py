"""
Tests for the UniversalHistory model.
"""
import pytest
import json
from datetime import datetime

from universal_history.models.universal_history import UniversalHistory
from universal_history.models.event_record import EventRecord, DomainType, ContentType, SourceType, InputMethod, ProcessingMethod, RawInput, Source, Creator
from universal_history.models.trajectory_synthesis import TrajectorySynthesis, TimeFrame
from universal_history.models.state_document import StateDocument, DomainState, EventReference
from universal_history.models.domain_catalog import DomainCatalog


def test_universal_history_creation(sample_subject_id):
    """Test creating a UniversalHistory."""
    # Create a new UniversalHistory
    history = UniversalHistory(
        subject_id=sample_subject_id,
        organization=sample_organization
    )
    
    # Verify the UniversalHistory was created with the expected values
    assert history.subject_id == sample_subject_id

    assert isinstance(history.hu_id, str)
    assert isinstance(history.created_at, datetime)
    assert isinstance(history.last_updated, datetime)
    assert history.event_records == {}
    assert history.trajectory_syntheses == {}
    assert history.state_document is None
    assert history.domain_catalogs == {}


def test_add_event_record(sample_universal_history, sample_event_record):
    """Test adding an EventRecord to a UniversalHistory."""
    # Initial state
    assert len(sample_universal_history.event_records) == 0

    
    # Add the event record
    sample_universal_history.add_event_record(sample_event_record)
    
    # Verify the event record was added
    assert len(sample_universal_history.event_records) == 1
    assert sample_event_record.re_id in sample_universal_history.event_records
    assert sample_universal_history.event_records[sample_event_record.re_id] == sample_event_record


def test_add_event_record_with_different_subject_id(sample_universal_history, sample_raw_input, sample_source):
    """Test adding an EventRecord with a different subject ID."""
    # Create an event record with a different subject ID
    event_record = EventRecord(
        subject_id="different-subject",
        domain_type=DomainType.EDUCATION,
        event_type="test_event",
        raw_input=sample_raw_input,
        source=sample_source,
        organization=sample_organization
    )
    
    # Attempt to add the event record
    with pytest.raises(ValueError) as excinfo:
        sample_universal_history.add_event_record(event_record)
    
    # Verify the error message
    assert "subject ID" in str(excinfo.value)


def test_add_event_record_updates_hash_chain(sample_universal_history, sample_event_record):
    """Test that adding an EventRecord updates the hash chain."""
    # Add the first event record
    first_event = sample_event_record
    first_event.update_hash()
    sample_universal_history.add_event_record(first_event)
    
    # Create a second event record
    second_event = EventRecord(
        subject_id=sample_universal_history.subject_id,
        domain_type=DomainType.EDUCATION,
        event_type="second_test_event",
        raw_input=first_event.raw_input,
        source=first_event.source,
        organization=sample_organization
    )
    
    # Add the second event record
    sample_universal_history.add_event_record(second_event)
    
    # Verify the hash chain
    assert second_event.previous_re_hash == first_event.current_re_hash


def test_add_trajectory_synthesis(sample_universal_history):
    """Test adding a TrajectorySynthesis to a UniversalHistory."""
    # Create a time frame for the synthesis
    time_frame = TimeFrame(
        start=datetime.now(),
        end=datetime.now()
    )
    
    # Create a trajectory synthesis
    synthesis = TrajectorySynthesis(
        subject_id=sample_universal_history.subject_id,
        organization=sample_organization,
        domain_type=DomainType.EDUCATION,
        synthesis_type="test_synthesis",
        content="Test synthesis content",
        time_frame=time_frame
    )
    
    # Initial state
    assert len(sample_universal_history.trajectory_syntheses) == 0
    
    # Add the trajectory synthesis
    sample_universal_history.add_trajectory_synthesis(synthesis)
    
    # Verify the trajectory synthesis was added
    assert len(sample_universal_history.trajectory_syntheses) == 1
    assert synthesis.st_id in sample_universal_history.trajectory_syntheses
    assert sample_universal_history.trajectory_syntheses[synthesis.st_id] == synthesis


def test_add_trajectory_synthesis_with_different_subject_id(sample_universal_history):
    """Test adding a TrajectorySynthesis with a different subject ID."""
    # Create a time frame for the synthesis
    time_frame = TimeFrame(
        start=datetime.now(),
        end=datetime.now()
    )
    
    # Create a trajectory synthesis with a different subject ID
    synthesis = TrajectorySynthesis(
        subject_id="different-subject",
        organization=sample_organization,
        domain_type=DomainType.EDUCATION,
        synthesis_type="test_synthesis",
        content="Test synthesis content",
        time_frame=time_frame
    )
    
    # Attempt to add the trajectory synthesis
    with pytest.raises(ValueError) as excinfo:
        sample_universal_history.add_trajectory_synthesis(synthesis)
    
    # Verify the error message
    assert "subject ID" in str(excinfo.value)


def test_set_state_document(sample_universal_history):
    """Test setting a StateDocument for a UniversalHistory."""
    # Create domain state for the state document
    domain_state = DomainState(
        last_updated=datetime.now(),
        current_status="Active"
    )
    
    # Create a state document
    state_document = StateDocument(
        subject_id=sample_universal_history.subject_id,
        organization=sample_organization,
        general_summary="Test state document",
        domains={"education": domain_state}
    )
    
    # Initial state
    assert sample_universal_history.state_document is None
    
    # Set the state document
    sample_universal_history.set_state_document(state_document)
    
    # Verify the state document was set
    assert sample_universal_history.state_document == state_document


def test_set_state_document_with_different_subject_id(sample_universal_history):
    """Test setting a StateDocument with a different subject ID."""
    # Create domain state for the state document
    domain_state = DomainState(
        last_updated=datetime.now(),
        current_status="Active"
    )
    
    # Create a state document with a different subject ID
    state_document = StateDocument(
        subject_id="different-subject",
        organization=sample_organization,
        general_summary="Test state document",
        domains={"education": domain_state}
    )
    
    # Attempt to set the state document
    with pytest.raises(ValueError) as excinfo:
        sample_universal_history.set_state_document(state_document)
    
    # Verify the error message
    assert "subject ID" in str(excinfo.value)


def test_add_domain_catalog(sample_universal_history):
    """Test adding a DomainCatalog to a UniversalHistory."""
    # Create an organization for the domain catalog
    organization = Organization(
        id="org-123",
        name="Test Organization"
    )
    
    # Create a domain catalog
    domain_catalog = DomainCatalog(
        domain_type=DomainType.EDUCATION,
        organization=sample_organization
    )
    
    # Initial state
    assert len(sample_universal_history.domain_catalogs) == 0
    
    # Add the domain catalog
    sample_universal_history.add_domain_catalog(domain_catalog)
    
    # Verify the domain catalog was added
    assert len(sample_universal_history.domain_catalogs) == 1
    assert DomainType.EDUCATION.value in sample_universal_history.domain_catalogs
    assert sample_universal_history.domain_catalogs[DomainType.EDUCATION.value] == domain_catalog


def test_get_event_record(populated_history, sample_event_record):
    """Test getting an EventRecord from a UniversalHistory."""
    # Get the event record
    event_record = populated_history.get_event_record(sample_event_record.re_id)
    
    # Verify the event record
    assert event_record == sample_event_record


def test_get_nonexistent_event_record(sample_universal_history):
    """Test getting a nonexistent EventRecord from a UniversalHistory."""
    # Get a nonexistent event record
    event_record = sample_universal_history.get_event_record("nonexistent-id")
    
    # Verify the result is None
    assert event_record is None


def test_get_trajectory_synthesis(sample_universal_history):
    """Test getting a TrajectorySynthesis from a UniversalHistory."""
    # Create a time frame for the synthesis
    time_frame = TimeFrame(
        start=datetime.now(),
        end=datetime.now()
    )
    
    # Create and add a trajectory synthesis
    synthesis = TrajectorySynthesis(
        subject_id=sample_universal_history.subject_id,
        organization=sample_organization,
        domain_type=DomainType.EDUCATION,
        time_frame=time_frame,
        summary="Test synthesis summary"
    )
    sample_universal_history.add_trajectory_synthesis(synthesis)
    
    # Get the trajectory synthesis
    retrieved_synthesis = sample_universal_history.get_trajectory_synthesis(synthesis.st_id)
    
    # Verify the trajectory synthesis
    assert retrieved_synthesis == synthesis


def test_get_nonexistent_trajectory_synthesis(sample_universal_history):
    """Test getting a nonexistent TrajectorySynthesis from a UniversalHistory."""
    # Get a nonexistent trajectory synthesis
    synthesis = sample_universal_history.get_trajectory_synthesis("nonexistent-id")
    
    # Verify the result is None
    assert synthesis is None


def test_get_domain_catalog(sample_universal_history):
    """Test getting a DomainCatalog from a UniversalHistory."""
    # Create an organization for the domain catalog
    organization = Organization(
        id="org-123",
        name="Test Organization"
    )
    
    # Create and add a domain catalog
    domain_catalog = DomainCatalog(
        domain_type=DomainType.EDUCATION,
        organization=sample_organization
    )
    sample_universal_history.add_domain_catalog(domain_catalog)
    
    # Get the domain catalog
    retrieved_catalog = sample_universal_history.get_domain_catalog(DomainType.EDUCATION)
    
    # Verify the domain catalog
    assert retrieved_catalog == domain_catalog


def test_get_nonexistent_domain_catalog(sample_universal_history):
    """Test getting a nonexistent DomainCatalog from a UniversalHistory."""
    # Get a nonexistent domain catalog
    catalog = sample_universal_history.get_domain_catalog(DomainType.HEALTH)
    
    # Verify the result is None
    assert catalog is None


def test_get_events_by_domain(sample_universal_history, sample_event_record):
    """Test getting EventRecords by domain from a UniversalHistory."""
    # Add an event record
    sample_universal_history.add_event_record(sample_event_record)
    
    # Get the events by domain
    events = sample_universal_history.get_events_by_domain(DomainType.EDUCATION)
    
    # Verify the events
    assert len(events) == 1
    assert events[0] == sample_event_record


def test_get_events_by_nonexistent_domain(sample_universal_history):
    """Test getting EventRecords by a nonexistent domain from a UniversalHistory."""
    # Get the events by a nonexistent domain
    events = sample_universal_history.get_events_by_domain(DomainType.HEALTH)
    
    # Verify the result is an empty list
    assert events == []


def test_to_dict(populated_history, sample_event_record):
    """Test converting a UniversalHistory to a dictionary."""
    # Convert to dictionary
    history_dict = populated_history.to_dict()
    
    # Verify the dictionary contains the expected keys
    assert "subject_id" in history_dict
    assert "hu_id" in history_dict
    assert "created_at" in history_dict
    assert "last_updated" in history_dict
    assert "event_records" in history_dict
    assert "trajectory_syntheses" in history_dict
    assert "state_document" in history_dict
    assert "domain_catalogs" in history_dict
    assert "organization" in history_dict
    
    # Verify the values
    assert history_dict["subject_id"] == populated_history.subject_id
    assert history_dict["hu_id"] == populated_history.hu_id
    assert isinstance(history_dict["created_at"], str)
    assert isinstance(history_dict["last_updated"], str)
    assert len(history_dict["event_records"]) == 1
    assert history_dict["organization"]["id"] == sample_organization.id


def test_to_json(populated_history):
    """Test converting a UniversalHistory to JSON."""
    # Convert to JSON
    history_json = populated_history.to_json()
    
    # Verify the JSON is valid
    history_dict = json.loads(history_json)
    
    # Verify the dictionary contains the expected keys
    assert "subject_id" in history_dict
    assert "hu_id" in history_dict
    assert "event_records" in history_dict
    assert "trajectory_syntheses" in history_dict
    assert "state_document" in history_dict
    assert "domain_catalogs" in history_dict
    assert "organization" in history_dict
    
    # Verify the values
    assert history_dict["subject_id"] == populated_history.subject_id
    assert history_dict["hu_id"] == populated_history.hu_id
    assert len(history_dict["event_records"]) == 1
    assert history_dict["organization"]["id"] == sample_organization.id


def test_from_dict():
    """Test creating a UniversalHistory from a dictionary."""
    # Create a dictionary
    history_dict = {
        "hu_id": "test-id",
        "subject_id": "test-subject",
        "created_at": datetime.now().isoformat(),
        "last_updated": datetime.now().isoformat(),
        "event_records": {},
        "trajectory_syntheses": {},
        "domain_catalogs": {},
        "organization": {
            "id": sample_organization.id,
            "name": sample_organization.name
        }
    }
    
    # Create a UniversalHistory from the dictionary
    history = UniversalHistory.from_dict(history_dict)
    
    # Verify the UniversalHistory was created with the expected values
    assert history.hu_id == "test-id"
    assert history.subject_id == "test-subject"
    assert isinstance(history.created_at, datetime)
    assert isinstance(history.last_updated, datetime)
    assert history.event_records == {}
    assert history.trajectory_syntheses == {}
    assert history.domain_catalogs == {}
    assert history.organization.id == sample_organization.id


def test_from_json():
    """Test creating a UniversalHistory from JSON."""
    # Create a JSON string
    history_json = json.dumps({
        "hu_id": "test-id",
        "subject_id": "test-subject",
        "created_at": datetime.now().isoformat(),
        "last_updated": datetime.now().isoformat(),
        "event_records": {},
        "trajectory_syntheses": {},
        "domain_catalogs": {},
        "organization": {
            "id": sample_organization.id,
            "name": sample_organization.name
        }
    })
    
    # Create a UniversalHistory from the JSON
    history = UniversalHistory.from_json(history_json)
    
    # Verify the UniversalHistory was created with the expected values
    assert history.hu_id == "test-id"
    assert history.subject_id == "test-subject"
    assert isinstance(history.created_at, datetime)
    assert isinstance(history.last_updated, datetime)
    assert history.event_records == {}
    assert history.trajectory_syntheses == {}
    assert history.domain_catalogs == {}
    assert history.organization.id == sample_organization.id


def test_verify_event_chain(sample_universal_history, sample_event_record):
    """Test verifying the event chain of a UniversalHistory."""
    # Add an event record
    sample_event_record.update_hash()
    sample_universal_history.add_event_record(sample_event_record)
    
    # Verify the event chain
    assert sample_universal_history.verify_event_chain(DomainType.EDUCATION)
    
    # Tamper with the event record
    sample_event_record.current_re_hash = "tampered-hash"
    
    # Verify the event chain again
    assert not sample_universal_history.verify_event_chain(DomainType.EDUCATION)