"""
Tests for the SynthesisService.
"""
import pytest
from datetime import datetime

from universal_history.models.event_record import (
    EventRecord, DomainType, ContentType, SourceType, 
    InputMethod, ProcessingMethod, RawInput, Source, Creator
)

from universal_history.models.trajectory_synthesis import TrajectorySynthesis
from universal_history.services.synthesis_service import SynthesisService


def test_synthesis_service_initialization(memory_repository):
    """Test initializing a SynthesisService."""
    # Create a new SynthesisService
    service = SynthesisService(memory_repository)
    
    # Verify the service was created with the repository
    assert service.repository == memory_repository


def test_create_trajectory_synthesis(synthesis_service, history_service, sample_subject_id):
    """Test creating a TrajectorySynthesis with a SynthesisService."""
    # Create a history
    history_service.create_history(sample_subject_id)
    
    # Create a trajectory synthesis
    st_id = synthesis_service.create_trajectory_synthesis(
        subject_id=sample_subject_id,
        domain_type=DomainType.EDUCATION,
        synthesis_type="test_synthesis",
        content="Test synthesis content"
    )
    
    # Verify the trajectory synthesis was created
    assert st_id is not None
    
    # Get the history
    history = history_service.get_history_by_subject(sample_subject_id)
    
    # Verify the trajectory synthesis was added to the history
    assert st_id in history.trajectory_syntheses
    synthesis = history.trajectory_syntheses[st_id]
    assert synthesis.subject_id == sample_subject_id
    assert synthesis.domain_type == DomainType.EDUCATION
    assert synthesis.synthesis_type == "test_synthesis"
    assert synthesis.content == "Test synthesis content"


def test_create_trajectory_synthesis_nonexistent_subject(synthesis_service):
    """Test creating a TrajectorySynthesis for a nonexistent subject with a SynthesisService."""
    # Create a trajectory synthesis for a nonexistent subject
    with pytest.raises(ValueError) as excinfo:
        synthesis_service.create_trajectory_synthesis(
            subject_id="nonexistent-subject",
            domain_type=DomainType.EDUCATION,
            synthesis_type="test_synthesis",
            content="Test synthesis content"
        )
    
    # Verify the error message
    assert "No Universal History found" in str(excinfo.value)


def test_get_trajectory_synthesis(synthesis_service, history_service, sample_subject_id):
    """Test getting a TrajectorySynthesis by ID with a SynthesisService."""
    # Create a history
    hu_id = history_service.create_history(sample_subject_id)
    
    # Create a trajectory synthesis
    st_id = synthesis_service.create_trajectory_synthesis(
        subject_id=sample_subject_id,
        domain_type=DomainType.EDUCATION,
        synthesis_type="test_synthesis",
        content="Test synthesis content"
    )
    
    # Get the trajectory synthesis
    synthesis = synthesis_service.get_trajectory_synthesis(st_id, hu_id)
    
    # Verify the trajectory synthesis
    assert synthesis is not None
    assert synthesis.st_id == st_id
    assert synthesis.subject_id == sample_subject_id
    assert synthesis.domain_type == DomainType.EDUCATION
    assert synthesis.synthesis_type == "test_synthesis"
    assert synthesis.content == "Test synthesis content"


def test_get_nonexistent_trajectory_synthesis(synthesis_service, history_service, sample_subject_id):
    """Test getting a nonexistent TrajectorySynthesis by ID with a SynthesisService."""
    # Create a history
    hu_id = history_service.create_history(sample_subject_id)
    
    # Get a nonexistent trajectory synthesis
    synthesis = synthesis_service.get_trajectory_synthesis("nonexistent-id", hu_id)
    
    # Verify the result is None
    assert synthesis is None


def test_generate_synthesis_from_events(synthesis_service, history_service, event_service, sample_subject_id, sample_raw_input, sample_source):
    """Test generating a TrajectorySynthesis from events with a SynthesisService."""
    # Create a history
    history_service.create_history(sample_subject_id)
    
    # Create some event records
    event_records = []
    for i in range(3):
        hu_id, re_id = event_service.create_event_record(
            subject_id=sample_subject_id,
            
            domain_type=DomainType.EDUCATION,
            event_type=f"test_event_{i}",
            content=sample_raw_input.content,
            content_type=sample_raw_input.type.value,
            source_type=sample_source.type.value,
            source_id=sample_source.id,
            source_name=sample_source.name,
            creator_id=sample_source.creator.id,
            creator_name=sample_source.creator.name,
            creator_role=sample_source.creator.role
        )
        event_records.append(re_id)
    
    # Generate a synthesis from events
    st_id = synthesis_service.generate_synthesis_from_events(
        subject_id=sample_subject_id,
        domain_type=DomainType.EDUCATION,
        synthesis_type="generated_synthesis",
        generator=lambda events: f"Generated content from {len(events)} events"
    )
    
    # Verify the synthesis was created
    assert st_id is not None
    
    # Get the history
    history = history_service.get_history_by_subject(sample_subject_id)
    
    # Verify the synthesis was added to the history
    assert st_id in history.trajectory_syntheses
    synthesis = history.trajectory_syntheses[st_id]
    assert synthesis.subject_id == sample_subject_id
    assert synthesis.domain_type == DomainType.EDUCATION
    assert synthesis.synthesis_type == "generated_synthesis"
    assert synthesis.content == "Generated content from 2 events"


def test_generate_synthesis_from_events_nonexistent_subject(synthesis_service):
    """Test generating a TrajectorySynthesis from events for a nonexistent subject with a SynthesisService."""
    # Generate a synthesis for a nonexistent subject
    with pytest.raises(ValueError) as excinfo:
        synthesis_service.generate_synthesis_from_events(
            subject_id="nonexistent-subject",
            domain_type=DomainType.EDUCATION,
            synthesis_type="generated_synthesis",
            generator=lambda events: "Generated content"
        )
    
    # Verify the error message
    assert "No Universal History found" in str(excinfo.value)


def test_generate_synthesis_from_events_no_events(synthesis_service, history_service, sample_subject_id):
    """Test generating a TrajectorySynthesis when there are no events with a SynthesisService."""
    # Create a history
    history_service.create_history(sample_subject_id)
    
    # Generate a synthesis from events
    st_id = synthesis_service.generate_synthesis_from_events(
        subject_id=sample_subject_id,
        domain_type=DomainType.EDUCATION,
        synthesis_type="generated_synthesis",
        generator=lambda events: f"Generated content from {len(events)} events"
    )
    
    # Verify the synthesis was created
    assert st_id is not None
    
    # Get the history
    history = history_service.get_history_by_subject(sample_subject_id)
    
    # Verify the synthesis was added to the history
    assert st_id in history.trajectory_syntheses
    synthesis = history.trajectory_syntheses[st_id]
    assert synthesis.content == "Generated content from 0 events"


def test_get_syntheses_by_domain(synthesis_service, history_service, sample_subject_id):
    """Test getting TrajectorySyntheses by domain with a SynthesisService."""
    # Create a history
    hu_id = history_service.create_history(sample_subject_id)
    
    # Create trajectory syntheses in different domains
    education_st_id = synthesis_service.create_trajectory_synthesis(
        subject_id=sample_subject_id,
        domain_type=DomainType.EDUCATION,
        synthesis_type="education_synthesis",
        content="Education synthesis content"
    )
    
    health_st_id = synthesis_service.create_trajectory_synthesis(
        subject_id=sample_subject_id,
        domain_type=DomainType.HEALTH,
        synthesis_type="health_synthesis",
        content="Health synthesis content"
    )
    
    # Get the syntheses by domain
    education_syntheses = synthesis_service.repository.get_syntheses_by_domain(
        domain_type=DomainType.EDUCATION,
        hu_id=hu_id
    )
    
    health_syntheses = synthesis_service.repository.get_syntheses_by_domain(
        domain_type=DomainType.HEALTH,
        hu_id=hu_id
    )
    
    # Verify the results
    assert len(education_syntheses) == 1
    assert education_syntheses[0].st_id == education_st_id
    assert education_syntheses[0].domain_type == DomainType.EDUCATION
    
    assert len(health_syntheses) == 1
    assert health_syntheses[0].st_id == health_st_id
    assert health_syntheses[0].domain_type == DomainType.HEALTH