"""
Fixtures for Universal History tests.
This file contains shared fixtures that can be used across all test modules.
"""
import pytest
from datetime import datetime
import uuid

from universal_history.models.event_record import (
    EventRecord, DomainType, ContentType, SourceType, 
    InputMethod, ProcessingMethod, RawInput, Source, Creator
)
from universal_history.models.universal_history import UniversalHistory
from universal_history.models.state_document import StateDocument
from universal_history.models.trajectory_synthesis import TrajectorySynthesis
from universal_history.models.domain_catalog import DomainCatalog, Organization
from universal_history.storage.memory_repository import MemoryHistoryRepository
from universal_history.services.event_service import EventService
from universal_history.services.history_service import HistoryService
from universal_history.services.state_service import StateService
from universal_history.services.synthesis_service import SynthesisService


@pytest.fixture
def memory_repository():
    """Create a memory repository for testing."""
    return MemoryHistoryRepository()


@pytest.fixture
def event_service(memory_repository):
    """Create an event service for testing."""
    return EventService(memory_repository)


@pytest.fixture
def history_service(memory_repository):
    """Create a history service for testing."""
    return HistoryService(memory_repository)


@pytest.fixture
def state_service(memory_repository):
    """Create a state service for testing."""
    return StateService(memory_repository)


@pytest.fixture
def synthesis_service(memory_repository):
    """Create a synthesis service for testing."""
    return SynthesisService(memory_repository)


@pytest.fixture
def sample_subject_id():
    """Create a sample subject ID for testing."""
    return f"subject-{uuid.uuid4()}"


@pytest.fixture
def sample_raw_input():
    """Create a sample raw input for testing."""
    return RawInput(
        type=ContentType.TEXT,
        content="This is a sample event content for testing.",
        context="Test context"
    )


@pytest.fixture
def sample_organization():
    """Create a sample organization for testing."""
    return Organization(
        id="org-123",
        name="Test Organization"
    )


@pytest.fixture
def sample_source():
    """Create a sample source for testing."""
    creator = Creator(
        id="creator-123",
        role="tester",
        name="Test Creator",
        qualifications=["Testing"]
    )
    
    return Source(
        type=SourceType.SYSTEM,
        id="source-123",
        name="Test Source",
        creator=creator,
        input_method=InputMethod.AUTOMATIC,
        processing_method=ProcessingMethod.AI_ANALYSIS
    )


@pytest.fixture
def sample_event_record(sample_subject_id, sample_raw_input, sample_source):
    """Create a sample event record for testing."""
    return EventRecord(
        subject_id=sample_subject_id,
        domain_type=DomainType.EDUCATION,
        event_type="test_event",
        raw_input=sample_raw_input,
        source=sample_source
    )


@pytest.fixture
def sample_universal_history(sample_subject_id):
    """Create a sample universal history for testing."""
    return UniversalHistory(
        subject_id=sample_subject_id,
        organization=sample_organization
    )


@pytest.fixture
def populated_history(sample_universal_history, sample_event_record):
    """Create a populated universal history with an event record."""
    history = sample_universal_history
    history.add_event_record(sample_event_record)
    return history


@pytest.fixture
def populated_repository(memory_repository, populated_history):
    """Create a populated repository with a universal history."""
    memory_repository.save_history(populated_history)
    return memory_repository