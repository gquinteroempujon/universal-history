"""
Tests for the StateService.
"""
import pytest
from datetime import datetime

from universal_history.models.event_record import (
    EventRecord, DomainType, ContentType, SourceType, 
    InputMethod, ProcessingMethod, RawInput, Source, Creator
)

from universal_history.models.state_document import StateDocument, DomainState
from universal_history.services.state_service import StateService


def test_state_service_initialization(memory_repository):
    """Test initializing a StateService."""
    # Create a new StateService
    service = StateService(memory_repository)
    
    # Verify the service was created with the repository
    assert service.repository == memory_repository


def test_create_state_document(state_service, history_service, sample_subject_id):
    """Test creating a StateDocument with a StateService."""
    # Create a history
    history_service.create_history(sample_subject_id)
    
    # Create a state document
    de_id = state_service.create_state_document(sample_subject_id)
    
    # Verify the state document was created
    assert de_id is not None
    
    # Get the history
    history = history_service.get_history_by_subject(sample_subject_id)
    
    # Verify the state document was added to the history
    assert history.state_document is not None
    assert history.state_document.de_id == de_id
    assert history.state_document.subject_id == sample_subject_id

    assert history.state_document.domains == {}


def test_create_state_document_nonexistent_subject(state_service):
    """Test creating a StateDocument for a nonexistent subject with a StateService."""
    # Create a state document for a nonexistent subject
    with pytest.raises(ValueError) as excinfo:
        state_service.create_state_document("nonexistent-subject")
    
    # Verify the error message
    assert "No Universal History found" in str(excinfo.value)


def test_get_state_document(state_service, history_service, sample_subject_id):
    """Test getting a StateDocument with a StateService."""
    # Create a history
    history_service.create_history(sample_subject_id)
    
    # Create a state document
    de_id = state_service.create_state_document(sample_subject_id)
    
    # Get the state document
    state_document = state_service.get_state_document(sample_subject_id)
    
    # Verify the state document
    assert state_document is not None
    assert state_document.de_id == de_id
    assert state_document.subject_id == sample_subject_id


def test_get_nonexistent_state_document(state_service):
    """Test getting a StateDocument for a nonexistent subject with a StateService."""
    # Get a state document for a nonexistent subject
    state_document = state_service.get_state_document("nonexistent-subject")
    
    # Verify the result is None
    assert state_document is None


def test_update_domain_state(state_service, history_service, sample_subject_id):
    """Test updating a domain state with a StateService."""
    # Create a history
    history_service.create_history(sample_subject_id)
    
    # Create a state document
    state_service.create_state_document(sample_subject_id)
    
    # Update a domain state
    state_service.update_domain_state(
        subject_id=sample_subject_id,
        domain_type=DomainType.EDUCATION,
        properties={"key": "value"},
        summary="Test summary"
    )
    
    # Get the state document
    state_document = state_service.get_state_document(sample_subject_id)
    
    # Verify the domain state was updated

    assert DomainType.EDUCATION.value in state_document.domains
    domain_state = state_document.domains[DomainType.EDUCATION.value]
    assert domain_state.properties == {"key": "value"}
    assert domain_state.summary == "Test summary"


def test_update_domain_state_nonexistent_subject(state_service):
    """Test updating a domain state for a nonexistent subject with a StateService."""
    # Update a domain state for a nonexistent subject
    with pytest.raises(ValueError) as excinfo:
        state_service.update_domain_state(
            subject_id="nonexistent-subject",
            domain_type=DomainType.EDUCATION,
            properties={"key": "value"},
            summary="Test summary"
        )
    
    # Verify the error message
    assert "No State Document found" in str(excinfo.value)


def test_update_domain_state_nonexistent_state_document(state_service, history_service, sample_subject_id):
    """Test updating a domain state for a subject without a state document with a StateService."""
    # Create a history without a state document
    history_service.create_history(sample_subject_id)
    
    # Update a domain state
    with pytest.raises(ValueError) as excinfo:
        state_service.update_domain_state(
            subject_id=sample_subject_id,
            domain_type=DomainType.EDUCATION,
            properties={"key": "value"},
            summary="Test summary"
        )
    
    # Verify the error message
    assert "No State Document found" in str(excinfo.value)


def test_update_state_from_events(state_service, history_service, event_service, sample_subject_id, sample_raw_input, sample_source):
    """Test updating a state document from events with a StateService."""
    # Create a history
    history_service.create_history(sample_subject_id)
    
    # Create a state document
    state_service.create_state_document(sample_subject_id)
    
    # Create event records
    event_service.create_event_record(
        subject_id=sample_subject_id,
        domain_type=DomainType.EDUCATION,
        event_type="test_event",
        raw_input=sample_raw_input,
        source=sample_source,
        processed_data={
            "quantitative_metrics": {"score": 95},
            "qualitative_assessments": {"performance": "excellent"}
        }
    )
    
    event_service.create_event_record(
        subject_id=sample_subject_id,
        domain_type=DomainType.HEALTH,
        event_type="health_event",
        raw_input=sample_raw_input,
        source=sample_source,
        processed_data={
            "quantitative_metrics": {"weight": 70},
            "qualitative_assessments": {"condition": "good"}
        }
    )
    
    # Update the state from events
    state_service.update_state_from_events(
        subject_id=sample_subject_id,
        domain_processors={
            DomainType.EDUCATION.value: lambda events: {
                "properties": {"score": max(e.processed_data.quantitative_metrics.get("score", 0) for e in events)},
                "summary": "Education summary"
            },
            DomainType.HEALTH.value: lambda events: {
                "properties": {"weight": max(e.processed_data.quantitative_metrics.get("weight", 0) for e in events)},
                "summary": "Health summary"
            }
        }
    )
    
    # Get the state document
    state_document = state_service.get_state_document(sample_subject_id)
    
    # Verify the domains were updated
    assert DomainType.EDUCATION.value in state_document.domains
    assert DomainType.HEALTH.value in state_document.domains
    
    # Verify the education domain
    education_state = state_document.domains[DomainType.EDUCATION.value]
    assert education_state.properties.get("score") == 95
    assert education_state.summary == "Education summary"
    
    # Verify the health domain
    health_state = state_document.domains[DomainType.HEALTH.value]
    assert health_state.properties.get("weight") == 70
    assert health_state.summary == "Health summary"


def test_update_state_from_events_nonexistent_subject(state_service):
    """Test updating a state from events for a nonexistent subject with a StateService."""
    # Update state from events for a nonexistent subject
    with pytest.raises(ValueError) as excinfo:
        state_service.update_state_from_events(
            subject_id="nonexistent-subject",
            domain_processors={}
        )
    
    # Verify the error message
    assert "No Universal History found" in str(excinfo.value)


def test_update_state_from_events_nonexistent_state_document(state_service, history_service, sample_subject_id):
    """Test updating a state from events for a subject without a state document with a StateService."""
    # Create a history without a state document
    history_service.create_history(sample_subject_id)
    
    # Update state from events
    with pytest.raises(ValueError) as excinfo:
        state_service.update_state_from_events(
            subject_id=sample_subject_id,
            domain_processors={}
        )
    
    # Verify the error message
    assert "No State Document found" in str(excinfo.value)


def test_get_llm_optimized_summary(state_service, history_service, sample_subject_id):
    """Test getting an LLM-optimized summary with a StateService."""
    # Create a history
    history_service.create_history(sample_subject_id)
    
    # Create a state document
    state_service.create_state_document(sample_subject_id)
    
    # Update domain states
    state_service.update_domain_state(
        subject_id=sample_subject_id,
        domain_type=DomainType.EDUCATION,
        properties={"score": 95},
        summary="Excellent academic performance with high test scores."
    )
    
    state_service.update_domain_state(
        subject_id=sample_subject_id,
        domain_type=DomainType.HEALTH,
        properties={"weight": 70, "height": 175},
        summary="Good physical condition with normal weight and height."
    )
    
    # Get the LLM-optimized summary
    summary = state_service.get_llm_optimized_summary(
        subject_id=sample_subject_id,
        include_domains=[DomainType.EDUCATION, DomainType.HEALTH],
        format_template="{domain} - {summary}"
    )
    
    # Verify the summary
    assert "education - Excellent academic performance" in summary.lower()
    assert "health - Good physical condition" in summary.lower()


def test_get_llm_optimized_summary_with_selected_domains(state_service, history_service, sample_subject_id):
    """Test getting an LLM-optimized summary with selected domains with a StateService."""
    # Create a history
    history_service.create_history(sample_subject_id)
    
    # Create a state document
    state_service.create_state_document(sample_subject_id)
    
    # Update domain states
    state_service.update_domain_state(
        subject_id=sample_subject_id,
        domain_type=DomainType.EDUCATION,
        properties={"score": 95},
        summary="Excellent academic performance with high test scores."
    )
    
    state_service.update_domain_state(
        subject_id=sample_subject_id,
        domain_type=DomainType.HEALTH,
        properties={"weight": 70, "height": 175},
        summary="Good physical condition with normal weight and height."
    )
    
    # Get the LLM-optimized summary with only the education domain
    summary = state_service.get_llm_optimized_summary(
        subject_id=sample_subject_id,
        include_domains=[DomainType.EDUCATION],
        format_template="{domain} - {summary}"
    )
    
    # Verify the summary
    assert "education - Excellent academic performance" in summary.lower()
    assert "health - Good physical condition" not in summary.lower()


def test_get_llm_optimized_summary_nonexistent_subject(state_service):
    """Test getting an LLM-optimized summary for a nonexistent subject with a StateService."""
    # Get an LLM-optimized summary for a nonexistent subject
    summary = state_service.get_llm_optimized_summary(
        subject_id="nonexistent-subject"
    )
    
    # Verify the result is an empty string
    assert summary == ""


def test_get_llm_optimized_summary_nonexistent_state_document(state_service, history_service, sample_subject_id):
    """Test getting an LLM-optimized summary for a subject without a state document with a StateService."""
    # Create a history without a state document
    history_service.create_history(sample_subject_id)
    
    # Get an LLM-optimized summary
    summary = state_service.get_llm_optimized_summary(
        subject_id=sample_subject_id
    )
    
    # Verify the result is an empty string
    assert summary == ""