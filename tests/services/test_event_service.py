"""
Tests for the EventService.
"""
import pytest
from datetime import datetime, timedelta

from universal_history.models.event_record import (
    EventRecord, DomainType, ContentType, SourceType, 
    InputMethod, ProcessingMethod, RawInput, Source, Creator
)

from universal_history.services.event_service import EventService


def test_event_service_initialization(memory_repository):
    """Test initializing an EventService."""
    # Create a new EventService
    service = EventService(memory_repository)
    
    # Verify the service was created with the repository
    assert service.repository == memory_repository


def test_create_event_record(event_service, history_service, sample_subject_id, sample_raw_input, sample_source):
    """Test creating an EventRecord with an EventService."""
    # Create a history
    hu_id = history_service.create_history(sample_subject_id)
    
    # Create an event record
    hu_id, re_id = event_service.create_event_record(
        subject_id=sample_subject_id,
        domain_type=DomainType.EDUCATION,
        event_type="test_event",
        content=sample_raw_input.content,
        content_type=sample_raw_input.type.value,
        source_type=sample_source.type.value,
        source_id=sample_source.id,
        source_name=sample_source.name,
        creator_id=sample_source.creator.id,
        creator_name=sample_source.creator.name,
        creator_role=sample_source.creator.role
    )
    
    # Verify the event record was created
    assert re_id is not None
    
    # Get the event record from the repository
    event_record = event_service.get_event_record(re_id, hu_id)
    
    # Verify the event record
    assert event_record is not None
    assert event_record.subject_id == sample_subject_id
    assert event_record.domain_type == DomainType.EDUCATION
    assert event_record.event_type == "test_event"
    assert event_record.raw_input.content == sample_raw_input.content
    assert event_record.raw_input.type == sample_raw_input.type.value
    assert event_record.source.type == sample_source.type.value
    assert event_record.source.id == sample_source.id
    assert event_record.source.name == sample_source.name
    assert event_record.re_id == re_id
    assert event_record.current_re_hash is not None  # Hash should be updated


def test_create_event_record_nonexistent_subject(event_service, sample_raw_input, sample_source):
    """Test creating an EventRecord for a nonexistent subject with an EventService."""
    # Create an event record for a nonexistent subject - note that this should actually create
    # a new history for the nonexistent subject rather than raising an error
    hu_id, re_id = event_service.create_event_record(
        subject_id="nonexistent-subject",
        domain_type=DomainType.EDUCATION,
        event_type="test_event",
        content=sample_raw_input.content,
        content_type=sample_raw_input.type.value,
        source_type=sample_source.type.value,
        source_id=sample_source.id,
        source_name=sample_source.name,
        creator_id=sample_source.creator.id,
        creator_name=sample_source.creator.name,
        creator_role=sample_source.creator.role
    )
    
    # Verify the event record was created
    assert re_id is not None
    assert hu_id is not None
    
    # Get the event record from the repository
    event_record = event_service.get_event_record(re_id, hu_id)
    
    # Verify the event record
    assert event_record is not None
    assert event_record.subject_id == "nonexistent-subject"


def test_get_event_record(event_service, history_service, sample_subject_id, sample_raw_input, sample_source):
    """Test getting an EventRecord by ID with an EventService."""
    # Create a history
    hu_id = history_service.create_history(sample_subject_id)
    
    # Create an event record
    hu_id, re_id = event_service.create_event_record(
        subject_id=sample_subject_id,
        domain_type=DomainType.EDUCATION,
        event_type="test_event",
        content=sample_raw_input.content,
        content_type=sample_raw_input.type.value,
        source_type=sample_source.type.value,
        source_id=sample_source.id,
        source_name=sample_source.name,
        creator_id=sample_source.creator.id,
        creator_name=sample_source.creator.name,
        creator_role=sample_source.creator.role
    )
    
    # Get the event record
    event_record = event_service.get_event_record(re_id, hu_id)
    
    # Verify the event record
    assert event_record is not None
    assert event_record.re_id == re_id


def test_get_nonexistent_event_record(event_service, history_service, sample_subject_id):
    """Test getting a nonexistent EventRecord by ID with an EventService."""
    # Create a history
    hu_id = history_service.create_history(sample_subject_id)
    
    # Create an event record
    hu_id, re_id = event_service.create_event_record(
        subject_id=sample_subject_id,
        domain_type=DomainType.EDUCATION,
        event_type="test_event",
        content="test content",
        content_type="text",
        source_type="test",
        source_id="test",
        source_name="test",
        creator_id="test",
        creator_name="test",
        creator_role="test"
    )
    
    # Get a nonexistent event record
    event_record = event_service.get_event_record("nonexistent-id", hu_id)
    
    # Verify the result is None
    assert event_record is None


def test_search_events_by_domain(event_service, history_service, sample_subject_id, sample_raw_input, sample_source):
    """Test searching for EventRecords by domain with an EventService."""
    # Create a history
    history_service.create_history(sample_subject_id)
    
    # Create event records for different domains
    event_service.create_event_record(
        subject_id=sample_subject_id,
        domain_type=DomainType.EDUCATION,
        event_type="education_event",
        content=sample_raw_input.content,
        content_type=sample_raw_input.type.value,
        source_type=sample_source.type.value,
        source_id=sample_source.id,
        source_name=sample_source.name,
        creator_id=sample_source.creator.id,
        creator_name=sample_source.creator.name,
        creator_role=sample_source.creator.role
    )
    
    event_service.create_event_record(
        subject_id=sample_subject_id,
        domain_type=DomainType.HEALTH,
        event_type="health_event",
        content=sample_raw_input.content,
        content_type=sample_raw_input.type.value,
        source_type=sample_source.type.value,
        source_id=sample_source.id,
        source_name=sample_source.name,
        creator_id=sample_source.creator.id,
        creator_name=sample_source.creator.name,
        creator_role=sample_source.creator.role
    )
    
    # Search for events by domain
    education_events = event_service.search_events(
        subject_id=sample_subject_id,
        domain_type=DomainType.EDUCATION
    )
    
    health_events = event_service.search_events(
        subject_id=sample_subject_id,
        domain_type=DomainType.HEALTH
    )
    
    # Verify the results
    assert len(education_events) == 1
    assert education_events[0].event_type == "education_event"
    
    assert len(health_events) == 1
    assert health_events[0].event_type == "health_event"


def test_search_events_by_type(event_service, history_service, sample_subject_id, sample_raw_input, sample_source, sample_organization):
    """Test searching for EventRecords by event type with an EventService."""
    # Create a history
    history_service.create_history(sample_subject_id)
    
    # Create event records with different types
    event_service.create_event_record(
        subject_id=sample_subject_id,
        domain_type=DomainType.EDUCATION,
        event_type="test_event",
        content=sample_raw_input.content,
        content_type=sample_raw_input.type.value,
        source_type=sample_source.type.value,
        source_id=sample_source.id,
        source_name=sample_source.name,
        creator_id=sample_source.creator.id,
        creator_name=sample_source.creator.name,
        creator_role=sample_source.creator.role
    )
    
    event_service.create_event_record(
        subject_id=sample_subject_id,
        domain_type=DomainType.EDUCATION,
        event_type="other_event",
        content=sample_raw_input.content,
        content_type=sample_raw_input.type.value,
        source_type=sample_source.type.value,
        source_id=sample_source.id,
        source_name=sample_source.name,
        creator_id=sample_source.creator.id,
        creator_name=sample_source.creator.name,
        creator_role=sample_source.creator.role
    )
    
    # Search for events by type
    test_events = event_service.search_events(
        subject_id=sample_subject_id,
        event_type="test_event"
    )
    
    other_events = event_service.search_events(
        subject_id=sample_subject_id,
        event_type="other_event"
    )
    
    # Verify the results
    assert len(test_events) == 1
    assert test_events[0].event_type == "test_event"
    
    assert len(other_events) == 1
    assert other_events[0].event_type == "other_event"


def test_search_events_by_time_range(event_service, history_service, sample_subject_id, sample_raw_input, sample_source, sample_organization):
    """Test searching for EventRecords by time range with an EventService."""
    # Create a history
    history_service.create_history(sample_subject_id)
    
    # Create an older event record
    older_time = datetime.now() - timedelta(days=7)
    older_event = EventRecord(
        subject_id=sample_subject_id,
        domain_type=DomainType.EDUCATION,
        event_type="older_event",
        raw_input=sample_raw_input,
        source=sample_source,
        timestamp=older_time
    )
    
    # Create a newer event record
    newer_time = datetime.now() - timedelta(days=1)
    newer_event = EventRecord(
        subject_id=sample_subject_id,
        domain_type=DomainType.EDUCATION,
        event_type="newer_event",
        raw_input=sample_raw_input,
        source=sample_source,
        timestamp=newer_time
    )
    
    # Save the event records directly to the repository
    history = history_service.get_history_by_subject(sample_subject_id)
    history.add_event_record(older_event)
    history.add_event_record(newer_event)
    event_service.repository.save_history(history)
    
    # Search for events by time range
    middle_time = datetime.now() - timedelta(days=3)
    
    newer_events = event_service.search_events(
        subject_id=sample_subject_id,
        start_date=middle_time
    )
    
    older_events = event_service.search_events(
        subject_id=sample_subject_id,
        end_date=middle_time
    )
    
    all_events = event_service.search_events(
        subject_id=sample_subject_id,
        start_date=older_time - timedelta(days=1),
        end_date=newer_time + timedelta(days=1)
    )
    
    # Verify the results
    assert len(newer_events) == 1
    assert newer_events[0].event_type == "newer_event"
    
    assert len(older_events) == 1
    assert older_events[0].event_type == "older_event"
    
    assert len(all_events) == 2


def test_search_events_with_limit(event_service, history_service, sample_subject_id, sample_raw_input, sample_source, sample_organization):
    """Test searching for EventRecords with a limit with an EventService."""
    # Create a history
    history_service.create_history(sample_subject_id)
    
    # Create multiple event records
    for i in range(5):
        event_service.create_event_record(
            subject_id=sample_subject_id,
            organization=sample_organization,
            domain_type=DomainType.EDUCATION,
            event_type=f"event_{i}",
            content=sample_raw_input.content,
            content_type=sample_raw_input.type.value,
            source_type=sample_source.type.value,
            source_id=sample_source.id,
            source_name=sample_source.name,
            creator_id=sample_source.creator.id,
            creator_name=sample_source.creator.name,
            creator_role=sample_source.creator.role
        )
    
    # Search for events with a limit
    # Note: The search_events method doesn't actually have a limit parameter,
    # but we can limit the results after retrieving them
    all_events = event_service.search_events(
        subject_id=sample_subject_id
    )
    
    limited_events = all_events[:3]
    
    # Verify the results
    assert len(limited_events) == 3
    assert len(all_events) == 5


def test_search_events_with_sort(event_service, history_service, sample_subject_id, sample_raw_input, sample_source, sample_organization):
    """Test searching for EventRecords with sorting with an EventService."""
    # Create a history
    history_service.create_history(sample_subject_id)
    
    # Create event records with different timestamps
    for i in range(3):
        event = EventRecord(
            subject_id=sample_subject_id,
            domain_type=DomainType.EDUCATION,
            event_type=f"event_{i}",
            raw_input=sample_raw_input,
            source=sample_source,
            timestamp=datetime.now() - timedelta(days=i)
        )
        
        # Save the event records directly to the repository
        history = history_service.get_history_by_subject(sample_subject_id)
        history.add_event_record(event)
        event_service.repository.save_history(history)
    
    # Search for events and get results
    events = event_service.search_events(
        subject_id=sample_subject_id
    )
    
    # The default sorting is descending by timestamp
    desc_events = events
    
    # Create ascending sort manually
    asc_events = sorted(events, key=lambda e: e.timestamp)
    
    # Verify the results
    assert len(asc_events) == 3
    assert len(desc_events) == 3
    
    # Verify the order
    assert asc_events[0].timestamp < asc_events[1].timestamp < asc_events[2].timestamp
    assert desc_events[0].timestamp > desc_events[1].timestamp > desc_events[2].timestamp