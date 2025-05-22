"""
Tests for the MemoryHistoryRepository.
"""
import pytest
from datetime import datetime

from universal_history.models.event_record import EventRecord, DomainType
from universal_history.models.trajectory_synthesis import TrajectorySynthesis
from universal_history.models.state_document import StateDocument
from universal_history.models.domain_catalog import DomainCatalog
from universal_history.models.universal_history import UniversalHistory
from universal_history.storage.memory_repository import MemoryHistoryRepository


def test_memory_repository_initialization():
    """Test initializing a MemoryHistoryRepository."""
    # Create a new MemoryHistoryRepository
    repo = MemoryHistoryRepository()
    
    # Verify the repository was created with empty dictionaries
    assert repo.histories == {}
    assert repo.subject_to_history == {}


def test_save_history(memory_repository, sample_universal_history):
    """Test saving a UniversalHistory to a MemoryHistoryRepository."""
    # Save the history
    hu_id = memory_repository.save_history(sample_universal_history)
    
    # Verify the history was saved
    assert hu_id == sample_universal_history.hu_id
    assert hu_id in memory_repository.histories
    assert memory_repository.histories[hu_id] == sample_universal_history
    assert sample_universal_history.subject_id in memory_repository.subject_to_history
    assert memory_repository.subject_to_history[sample_universal_history.subject_id] == hu_id


def test_get_history(memory_repository, sample_universal_history):
    """Test getting a UniversalHistory from a MemoryHistoryRepository."""
    # Save the history
    memory_repository.save_history(sample_universal_history)
    
    # Get the history
    history = memory_repository.get_history(sample_universal_history.hu_id)
    
    # Verify the history
    assert history == sample_universal_history


def test_get_nonexistent_history(memory_repository):
    """Test getting a nonexistent UniversalHistory from a MemoryHistoryRepository."""
    # Get a nonexistent history
    history = memory_repository.get_history("nonexistent-id")
    
    # Verify the result is None
    assert history is None


def test_get_history_by_subject(memory_repository, sample_universal_history):
    """Test getting a UniversalHistory by subject ID from a MemoryHistoryRepository."""
    # Save the history
    memory_repository.save_history(sample_universal_history)
    
    # Get the history by subject
    history = memory_repository.get_history_by_subject(sample_universal_history.subject_id)
    
    # Verify the history
    assert history == sample_universal_history


def test_get_history_by_nonexistent_subject(memory_repository):
    """Test getting a UniversalHistory by a nonexistent subject ID from a MemoryHistoryRepository."""
    # Get a history by a nonexistent subject
    history = memory_repository.get_history_by_subject("nonexistent-subject")
    
    # Verify the result is None
    assert history is None


def test_save_event_record(memory_repository, sample_universal_history, sample_event_record):
    """Test saving an EventRecord to a UniversalHistory in a MemoryHistoryRepository."""
    # Save the history
    hu_id = memory_repository.save_history(sample_universal_history)
    
    # Save the event record
    re_id = memory_repository.save_event_record(sample_event_record, hu_id)
    
    # Verify the event record was saved
    assert re_id == sample_event_record.re_id
    assert re_id in memory_repository.histories[hu_id].event_records
    assert memory_repository.histories[hu_id].event_records[re_id] == sample_event_record



def test_save_event_record_to_nonexistent_history(memory_repository, sample_event_record):
    """Test saving an EventRecord to a nonexistent UniversalHistory in a MemoryHistoryRepository."""
    # Create an event record with organization
    event_record = EventRecord(
        subject_id="test-subject",
        domain_type=DomainType.EDUCATION,
        event_type="test_event",
        raw_input=sample_event_record.raw_input,
        source=sample_event_record.source,
        organization=sample_organization
    )
    
    # Attempt to save the event record
    with pytest.raises(ValueError) as excinfo:
        memory_repository.save_event_record(event_record, "nonexistent-id")
    
    # Verify the error message
    assert "not found" in str(excinfo.value)


def test_get_event_record(memory_repository, sample_universal_history, sample_event_record):
    """Test getting an EventRecord from a UniversalHistory in a MemoryHistoryRepository."""
    # Save the history and event record
    hu_id = memory_repository.save_history(sample_universal_history)
    memory_repository.save_event_record(sample_event_record, hu_id)
    
    # Get the event record
    event_record = memory_repository.get_event_record(sample_event_record.re_id, hu_id)
    
    # Verify the event record
    assert event_record == sample_event_record



def test_get_nonexistent_event_record(memory_repository, sample_universal_history):
    """Test getting a nonexistent EventRecord from a UniversalHistory in a MemoryHistoryRepository."""
    # Save the history
    hu_id = memory_repository.save_history(sample_universal_history)
    
    # Create an event record with organization
    event_record = EventRecord(
        subject_id="test-subject",
        domain_type=DomainType.EDUCATION,
        event_type="test_event",
        raw_input=sample_universal_history.event_records.get("nonexistent-id", {}).raw_input if "nonexistent-id" in sample_universal_history.event_records else None,
        source=sample_universal_history.event_records.get("nonexistent-id", {}).source if "nonexistent-id" in sample_universal_history.event_records else None,
        organization=sample_organization
    )
    
    # Get a nonexistent event record
    event_record = memory_repository.get_event_record("nonexistent-id", hu_id)
    
    # Verify the result is None
    assert event_record is None


def test_get_event_record_from_nonexistent_history(memory_repository):
    """Test getting an EventRecord from a nonexistent UniversalHistory in a MemoryHistoryRepository."""
    # Get an event record from a nonexistent history
    event_record = memory_repository.get_event_record("event-id", "nonexistent-id")
    
    # Verify the result is None
    assert event_record is None


def test_save_trajectory_synthesis(memory_repository, sample_universal_history):
    """Test saving a TrajectorySynthesis to a UniversalHistory in a MemoryHistoryRepository."""
    # Save the history
    hu_id = memory_repository.save_history(sample_universal_history)
    
    # Create a time frame for the synthesis
    from datetime import datetime
    time_frame = {
        "start": datetime.now().isoformat(),
        "end": datetime.now().isoformat()
    }
    
    # Create a trajectory synthesis
    synthesis = TrajectorySynthesis(
        subject_id=sample_universal_history.subject_id,
        domain_type=DomainType.EDUCATION,
        time_frame=time_frame,
        content="Test synthesis summary"
    )
    
    # Save the trajectory synthesis
    st_id = memory_repository.save_trajectory_synthesis(synthesis, hu_id)
    
    # Verify the trajectory synthesis was saved
    assert st_id == synthesis.st_id
    assert st_id in memory_repository.histories[hu_id].trajectory_syntheses
    assert memory_repository.histories[hu_id].trajectory_syntheses[st_id] == synthesis


def test_save_trajectory_synthesis_to_nonexistent_history(memory_repository, sample_universal_history):
    """Test saving a TrajectorySynthesis to a nonexistent UniversalHistory in a MemoryHistoryRepository."""
    # Create a trajectory synthesis
    synthesis = TrajectorySynthesis(
        subject_id="test-subject",
        organization=sample_organization,
        domain_type=DomainType.EDUCATION,
        time_frame={"start": datetime.now(), "end": datetime.now()},
        content="Test synthesis content"
    )
    
    # Attempt to save the trajectory synthesis
    with pytest.raises(ValueError) as excinfo:
        memory_repository.save_trajectory_synthesis(synthesis, "nonexistent-id")
    
    # Verify the error message
    assert "not found" in str(excinfo.value)


def test_get_trajectory_synthesis(memory_repository, sample_universal_history):
    """Test getting a TrajectorySynthesis from a UniversalHistory in a MemoryHistoryRepository."""
    # Save the history
    hu_id = memory_repository.save_history(sample_universal_history)
    
    # Create and save a trajectory synthesis
    synthesis = TrajectorySynthesis(
        subject_id=sample_universal_history.subject_id,
        domain_type=DomainType.EDUCATION,
        synthesis_type="test_synthesis",
        content="Test synthesis content"
    )
    memory_repository.save_trajectory_synthesis(synthesis, hu_id)
    
    # Get the trajectory synthesis
    retrieved_synthesis = memory_repository.get_trajectory_synthesis(synthesis.st_id, hu_id)
    
    # Verify the trajectory synthesis
    assert retrieved_synthesis == synthesis


def test_get_nonexistent_trajectory_synthesis(memory_repository, sample_universal_history):
    """Test getting a nonexistent TrajectorySynthesis from a UniversalHistory in a MemoryHistoryRepository."""
    # Save the history
    hu_id = memory_repository.save_history(sample_universal_history)
    
    # Get a nonexistent trajectory synthesis
    synthesis = memory_repository.get_trajectory_synthesis("nonexistent-id", hu_id)
    
    # Verify the result is None
    assert synthesis is None


def test_get_trajectory_synthesis_from_nonexistent_history(memory_repository):
    """Test getting a TrajectorySynthesis from a nonexistent UniversalHistory in a MemoryHistoryRepository."""
    # Get a trajectory synthesis from a nonexistent history
    synthesis = memory_repository.get_trajectory_synthesis("synthesis-id", "nonexistent-id")
    
    # Verify the result is None
    assert synthesis is None


def test_save_state_document(memory_repository, sample_universal_history):
    """Test saving a StateDocument to a UniversalHistory in a MemoryHistoryRepository."""
    # Save the history
    hu_id = memory_repository.save_history(sample_universal_history)
    
    # Create a state document
    state_document = StateDocument(subject_id=sample_universal_history.subject_id)
    
    # Save the state document
    de_id = memory_repository.save_state_document(state_document, hu_id)
    
    # Verify the state document was saved
    assert de_id == state_document.de_id
    assert memory_repository.histories[hu_id].state_document == state_document


def test_save_state_document_to_nonexistent_history(memory_repository, sample_universal_history):
    """Test saving a StateDocument to a nonexistent UniversalHistory in a MemoryHistoryRepository."""
    # Create a state document
    state_document = StateDocument(subject_id=sample_universal_history.subject_id)
    
    # Attempt to save the state document
    with pytest.raises(ValueError) as excinfo:
        memory_repository.save_state_document(state_document, "nonexistent-id")
    
    # Verify the error message
    assert "not found" in str(excinfo.value)


def test_get_state_document(memory_repository, sample_universal_history):
    """Test getting a StateDocument from a UniversalHistory in a MemoryHistoryRepository."""
    # Save the history
    hu_id = memory_repository.save_history(sample_universal_history)
    
    # Create and save a state document
    state_document = StateDocument(subject_id=sample_universal_history.subject_id)
    memory_repository.save_state_document(state_document, hu_id)
    
    # Get the state document
    retrieved_document = memory_repository.get_state_document(hu_id)
    
    # Verify the state document
    assert retrieved_document == state_document


def test_get_state_document_from_nonexistent_history(memory_repository):
    """Test getting a StateDocument from a nonexistent UniversalHistory in a MemoryHistoryRepository."""
    # Get a state document from a nonexistent history
    document = memory_repository.get_state_document("nonexistent-id")
    
    # Verify the result is None
    assert document is None


def test_save_domain_catalog(memory_repository, sample_universal_history):
    """Test saving a DomainCatalog to a UniversalHistory in a MemoryHistoryRepository."""
    # Save the history
    hu_id = memory_repository.save_history(sample_universal_history)
    
    # Create a domain catalog
    domain_catalog = DomainCatalog(
        domain_type=DomainType.EDUCATION,
        organization=sample_universal_history.organization,
        event_types=["test_event"],
        properties={"key": "value"}
    )
    
    # Save the domain catalog
    cdd_id = memory_repository.save_domain_catalog(domain_catalog, hu_id)
    
    # Verify the domain catalog was saved
    assert cdd_id == domain_catalog.cdd_id
    assert DomainType.EDUCATION.value in memory_repository.histories[hu_id].domain_catalogs
    assert memory_repository.histories[hu_id].domain_catalogs[DomainType.EDUCATION.value] == domain_catalog


def test_save_domain_catalog_to_nonexistent_history(memory_repository):
    """Test saving a DomainCatalog to a nonexistent UniversalHistory in a MemoryHistoryRepository."""
    # Create a domain catalog
    domain_catalog = DomainCatalog(
        domain_type=DomainType.EDUCATION,
        organization=sample_organization,
        event_types=["test_event"],
        properties={"key": "value"}
    )
    
    # Attempt to save the domain catalog
    with pytest.raises(ValueError) as excinfo:
        memory_repository.save_domain_catalog(domain_catalog, "nonexistent-id")
    
    # Verify the error message
    assert "not found" in str(excinfo.value)


def test_get_domain_catalog(memory_repository, sample_universal_history):
    """Test getting a DomainCatalog from a UniversalHistory in a MemoryHistoryRepository."""
    # Save the history
    hu_id = memory_repository.save_history(sample_universal_history)
    
    # Create and save a domain catalog
    domain_catalog = DomainCatalog(
        domain_type=DomainType.EDUCATION,
        event_types=["test_event"],
        properties={"key": "value"}
    )
    memory_repository.save_domain_catalog(domain_catalog, hu_id)
    
    # Get the domain catalog
    retrieved_catalog = memory_repository.get_domain_catalog(DomainType.EDUCATION, hu_id)
    
    # Verify the domain catalog
    assert retrieved_catalog == domain_catalog


def test_get_nonexistent_domain_catalog(memory_repository, sample_universal_history):
    """Test getting a nonexistent DomainCatalog from a UniversalHistory in a MemoryHistoryRepository."""
    # Save the history
    hu_id = memory_repository.save_history(sample_universal_history)
    
    # Get a nonexistent domain catalog
    catalog = memory_repository.get_domain_catalog(DomainType.HEALTH, hu_id)
    
    # Verify the result is None
    assert catalog is None


def test_get_domain_catalog_from_nonexistent_history(memory_repository):
    """Test getting a DomainCatalog from a nonexistent UniversalHistory in a MemoryHistoryRepository."""
    # Get a domain catalog from a nonexistent history
    catalog = memory_repository.get_domain_catalog(DomainType.EDUCATION, "nonexistent-id")
    
    # Verify the result is None
    assert catalog is None


def test_get_events_by_domain(memory_repository, sample_universal_history, sample_event_record):
    """Test getting EventRecords by domain from a UniversalHistory in a MemoryHistoryRepository."""
    # Save the history and event record
    hu_id = memory_repository.save_history(sample_universal_history)
    memory_repository.save_event_record(sample_event_record, hu_id)
    
    # Get the events by domain
    events = memory_repository.get_events_by_domain(DomainType.EDUCATION, hu_id)
    
    # Verify the events
    assert len(events) == 1
    assert events[0] == sample_event_record


def test_get_events_by_nonexistent_domain(memory_repository, sample_universal_history):
    """Test getting EventRecords by a nonexistent domain from a UniversalHistory in a MemoryHistoryRepository."""
    # Save the history
    hu_id = memory_repository.save_history(sample_universal_history)
    
    # Get the events by a nonexistent domain
    events = memory_repository.get_events_by_domain(DomainType.HEALTH, hu_id)
    
    # Verify the result is an empty list
    assert events == []


def test_get_events_by_domain_from_nonexistent_history(memory_repository):
    """Test getting EventRecords by domain from a nonexistent UniversalHistory in a MemoryHistoryRepository."""
    # Get events by domain from a nonexistent history
    events = memory_repository.get_events_by_domain(DomainType.EDUCATION, "nonexistent-id")
    
    # Verify the result is an empty list
    assert events == []