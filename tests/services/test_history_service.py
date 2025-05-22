"""
Tests for the HistoryService.
"""
import pytest
from datetime import datetime

from universal_history.models.event_record import EventRecord, DomainType
from universal_history.models.universal_history import UniversalHistory

from universal_history.services.history_service import HistoryService


def test_history_service_initialization(memory_repository):
    """Test initializing a HistoryService."""
    # Create a new HistoryService
    service = HistoryService(memory_repository)
    
    # Verify the service was created with the repository
    assert service.repository == memory_repository


def test_create_history(history_service, sample_subject_id):
    """Test creating a new UniversalHistory with a HistoryService."""
    # Create a new history
    hu_id = history_service.create_history(sample_subject_id)
    
    # Verify the history was created
    assert hu_id is not None
    
    # Get the history from the repository
    history = history_service.repository.get_history(hu_id)
    
    # Verify the history
    assert history is not None
    assert history.subject_id == sample_subject_id

    assert history.hu_id == hu_id


def test_create_history_existing_subject(history_service, sample_subject_id):
    """Test creating a UniversalHistory for an existing subject with a HistoryService."""
    # Create a first history
    first_hu_id = history_service.create_history(sample_subject_id)
    
    # Create a second history for the same subject
    second_hu_id = history_service.create_history(sample_subject_id)
    
    # Verify the IDs are the same
    assert first_hu_id == second_hu_id


def test_get_history(history_service, sample_subject_id):
    """Test getting a UniversalHistory by ID with a HistoryService."""
    # Create a history
    hu_id = history_service.create_history(sample_subject_id)
    
    # Get the history
    history = history_service.get_history(hu_id)
    
    # Verify the history
    assert history is not None
    assert history.subject_id == sample_subject_id
    assert history.hu_id == hu_id


def test_get_nonexistent_history(history_service):
    """Test getting a nonexistent UniversalHistory by ID with a HistoryService."""
    # Get a nonexistent history
    history = history_service.get_history("nonexistent-id")
    
    # Verify the result is None
    assert history is None


def test_get_history_by_subject(history_service, sample_subject_id):
    """Test getting a UniversalHistory by subject ID with a HistoryService."""
    # Create a history
    hu_id = history_service.create_history(sample_subject_id)
    
    # Get the history by subject
    history = history_service.get_history_by_subject(sample_subject_id)
    
    # Verify the history
    assert history is not None
    assert history.subject_id == sample_subject_id
    assert history.hu_id == hu_id


def test_get_history_by_nonexistent_subject(history_service):
    """Test getting a UniversalHistory by a nonexistent subject ID with a HistoryService."""
    # Get a history by a nonexistent subject
    history = history_service.get_history_by_subject("nonexistent-subject")
    
    # Verify the result is None
    assert history is None


def test_get_subject_domains(history_service, sample_subject_id, sample_event_record):
    """Test getting all domains for a subject with a HistoryService."""
    # Create a history
    hu_id = history_service.create_history(sample_subject_id)
    
    # Save an event record
    sample_event_record.subject_id = sample_subject_id  # Ensure the subject ID matches
    history_service.repository.save_event_record(sample_event_record, hu_id)
    
    # Get the domains
    domains = history_service.get_subject_domains(sample_subject_id)
    
    # Verify the domains
    assert domains is not None
    assert len(domains) == 1
    assert DomainType.EDUCATION.value in domains


def test_get_subject_domains_no_events(history_service, sample_subject_id):
    """Test getting domains for a subject with no events with a HistoryService."""
    # Create a history
    history_service.create_history(sample_subject_id)
    
    # Get the domains
    domains = history_service.get_subject_domains(sample_subject_id)
    
    # Verify the domains
    assert domains is not None
    assert len(domains) == 0


def test_get_subject_domains_nonexistent_subject(history_service):
    """Test getting domains for a nonexistent subject with a HistoryService."""
    # Get domains for a nonexistent subject
    domains = history_service.get_subject_domains("nonexistent-subject")
    
    # Verify the result is an empty set
    assert domains == set()


def test_verify_event_chains(history_service, sample_subject_id, sample_event_record):
    """Test verifying event chains for a subject with a HistoryService."""
    # Create a history
    hu_id = history_service.create_history(sample_subject_id)
    
    # Save an event record
    sample_event_record.subject_id = sample_subject_id  # Ensure the subject ID matches
    sample_event_record.update_hash()
    history_service.repository.save_event_record(sample_event_record, hu_id)
    
    # Verify the event chains
    results = history_service.verify_event_chains(sample_subject_id)
    
    # Verify the results
    assert results is not None
    assert DomainType.EDUCATION.value in results
    assert results[DomainType.EDUCATION.value] is True


def test_verify_event_chains_nonexistent_subject(history_service):
    """Test verifying event chains for a nonexistent subject with a HistoryService."""
    # Verify event chains for a nonexistent subject
    results = history_service.verify_event_chains("nonexistent-subject")
    
    # Verify the result is an empty dictionary
    assert results == {}


def test_export_history(history_service, sample_subject_id, sample_event_record):
    """Test exporting a UniversalHistory as a dictionary with a HistoryService."""
    # Create a history
    hu_id = history_service.create_history(sample_subject_id)
    
    # Save an event record
    sample_event_record.subject_id = sample_subject_id  # Ensure the subject ID matches
    history_service.repository.save_event_record(sample_event_record, hu_id)
    
    # Export the history
    export_data = history_service.export_history(sample_subject_id)
    
    # Verify the export data
    assert export_data is not None
    assert "hu_id" in export_data
    assert "subject_id" in export_data
    assert "created_at" in export_data
    assert "last_updated" in export_data
    assert "event_records" in export_data
    
    # Verify the values
    assert export_data["hu_id"] == hu_id
    assert export_data["subject_id"] == sample_subject_id
    assert sample_event_record.re_id in export_data["event_records"]


def test_export_history_selective(history_service, sample_subject_id, sample_event_record):
    """Test selectively exporting a UniversalHistory as a dictionary with a HistoryService."""
    # Create a history
    hu_id = history_service.create_history(sample_subject_id)
    
    # Save an event record
    sample_event_record.subject_id = sample_subject_id  # Ensure the subject ID matches
    history_service.repository.save_event_record(sample_event_record, hu_id)
    
    # Export the history without events
    export_data = history_service.export_history(sample_subject_id, include_events=False)
    
    # Verify the export data
    assert export_data is not None
    assert "hu_id" in export_data
    assert "subject_id" in export_data
    assert "created_at" in export_data
    assert "last_updated" in export_data
    assert "event_records" not in export_data


def test_export_history_nonexistent_subject(history_service):
    """Test exporting a UniversalHistory for a nonexistent subject with a HistoryService."""
    # Attempt to export a history for a nonexistent subject
    with pytest.raises(ValueError) as excinfo:
        history_service.export_history("nonexistent-subject")
    
    # Verify the error message
    assert "No Universal History found" in str(excinfo.value)


def test_import_history(history_service):
    """Test importing a UniversalHistory from a dictionary with a HistoryService."""
    # Create a history dictionary
    history_data = {
        "hu_id": "test-hu-id",
        "subject_id": "test-subject",
        "created_at": datetime.now().isoformat(),
        "last_updated": datetime.now().isoformat(),
        "event_records": {},
        "trajectory_syntheses": {},
        "domain_catalogs": {}
    }
    
    # Import the history
    hu_id = history_service.import_history(history_data)
    
    # Verify the history was imported
    assert hu_id == "test-hu-id"
    
    # Get the history from the repository
    history = history_service.repository.get_history(hu_id)
    
    # Verify the history
    assert history is not None
    assert history.hu_id == "test-hu-id"
    assert history.subject_id == "test-subject"


def test_copy_history(history_service, sample_subject_id, sample_event_record, sample_organization):
    """Test copying a UniversalHistory from one subject to another with a HistoryService."""
    # Create a source history
    source_hu_id = history_service.create_history(sample_subject_id, sample_organization)
    
    # Save an event record
    sample_event_record.subject_id = sample_subject_id  # Ensure the subject ID matches
    source_history = history_service.get_history(source_hu_id)
    source_history.add_event_record(sample_event_record)
    history_service.repository.save_history(source_history)
    
    # Copy the history
    target_subject_id = "target-subject"
    target_hu_id = history_service.copy_history(sample_subject_id, target_subject_id)
    
    # Verify the copy
    assert target_hu_id is not None
    assert target_hu_id != source_hu_id
    
    # Get the copied history
    target_history = history_service.get_history(target_hu_id)
    
    # Verify the copied history
    assert target_history is not None
    assert target_history.subject_id == target_subject_id
    
    # The event records should be copied with updated subject IDs
    # Find the copied event by comparing fields other than re_id
    found_event = False
    for event_record in target_history.event_records.values():
        if (event_record.event_type == sample_event_record.event_type and
            event_record.domain_type == sample_event_record.domain_type):
            found_event = True
            break
    
    assert found_event, "Copied event not found in target history"