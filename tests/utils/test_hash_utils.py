"""
Tests for the hash_utils module.
"""
import pytest
from datetime import datetime

from universal_history.utils.hash_utils import (
    calculate_hash, verify_hash, verify_hash_chain, create_hash_chain
)


def test_calculate_hash():
    """Test calculating a hash from a dictionary."""
    # Create a test dictionary
    data = {
        "id": "test-id",
        "name": "Test Name",
        "value": 123,
        "timestamp": datetime.now()
    }
    
    # Calculate the hash
    hash_value = calculate_hash(data)
    
    # Verify the result is a non-empty string
    assert hash_value is not None
    assert isinstance(hash_value, str)
    assert len(hash_value) > 0


def test_calculate_hash_deterministic():
    """Test that hash calculation is deterministic for the same input."""
    # Create a test dictionary with a fixed timestamp
    data = {
        "id": "test-id",
        "name": "Test Name",
        "value": 123,
        "timestamp": "2023-01-01T00:00:00"
    }
    
    # Calculate the hash twice
    hash1 = calculate_hash(data)
    hash2 = calculate_hash(data)
    
    # Verify both hashes are the same
    assert hash1 == hash2


def test_calculate_hash_different_inputs():
    """Test that hash calculation gives different results for different inputs."""
    # Create two test dictionaries with different values
    data1 = {
        "id": "test-id-1",
        "name": "Test Name 1",
        "value": 123
    }
    
    data2 = {
        "id": "test-id-2",
        "name": "Test Name 2",
        "value": 456
    }
    
    # Calculate the hashes
    hash1 = calculate_hash(data1)
    hash2 = calculate_hash(data2)
    
    # Verify the hashes are different
    assert hash1 != hash2


def test_verify_hash():
    """Test verifying a hash against a dictionary."""
    # Create a test dictionary
    data = {
        "id": "test-id",
        "name": "Test Name",
        "value": 123,
        "timestamp": "2023-01-01T00:00:00"
    }
    
    # Calculate the hash
    hash_value = calculate_hash(data)
    
    # Verify the hash
    assert verify_hash(data, hash_value)
    
    # Modify the data
    modified_data = data.copy()
    modified_data["value"] = 456
    
    # Verify the hash fails
    assert not verify_hash(modified_data, hash_value)


def test_verify_hash_chain_empty():
    """Test verifying an empty hash chain."""
    # Verify an empty chain
    assert verify_hash_chain(
        [],
        lambda item: item["current_hash"],
        lambda item: item["previous_hash"]
    )


def test_verify_hash_chain_valid():
    """Test verifying a valid hash chain."""
    # Create a test chain
    items = [
        {"id": "item-1", "current_hash": "hash1", "previous_hash": None},
        {"id": "item-2", "current_hash": "hash2", "previous_hash": "hash1"},
        {"id": "item-3", "current_hash": "hash3", "previous_hash": "hash2"}
    ]
    
    # Verify the chain
    assert verify_hash_chain(
        items,
        lambda item: item["current_hash"],
        lambda item: item["previous_hash"]
    )


def test_verify_hash_chain_invalid_first_item():
    """Test verifying a hash chain with an invalid first item."""
    # Create a test chain with an invalid first item
    items = [
        {"id": "item-1", "current_hash": "hash1", "previous_hash": "invalid"},  # First item should have no previous hash
        {"id": "item-2", "current_hash": "hash2", "previous_hash": "hash1"},
        {"id": "item-3", "current_hash": "hash3", "previous_hash": "hash2"}
    ]
    
    # Verify the chain fails
    assert not verify_hash_chain(
        items,
        lambda item: item["current_hash"],
        lambda item: item["previous_hash"]
    )


def test_verify_hash_chain_invalid_link():
    """Test verifying a hash chain with an invalid link."""
    # Create a test chain with an invalid link
    items = [
        {"id": "item-1", "current_hash": "hash1", "previous_hash": None},
        {"id": "item-2", "current_hash": "hash2", "previous_hash": "hash1"},
        {"id": "item-3", "current_hash": "hash3", "previous_hash": "invalid"}  # Should be hash2
    ]
    
    # Verify the chain fails
    assert not verify_hash_chain(
        items,
        lambda item: item["current_hash"],
        lambda item: item["previous_hash"]
    )


def test_create_hash_chain():
    """Test creating a hash chain from a list of items."""
    # Create a list of items
    items = [
        {"id": "item-1", "data": "data1", "current_hash": None, "previous_hash": None},
        {"id": "item-2", "data": "data2", "current_hash": None, "previous_hash": None},
        {"id": "item-3", "data": "data3", "current_hash": None, "previous_hash": None}
    ]
    
    # Define hash generator and setter functions
    def hash_generator(item):
        return f"hash-{item['id']}"
    
    def previous_hash_setter(item, prev_hash):
        item["previous_hash"] = prev_hash
    
    # Create the hash chain
    create_hash_chain(items, hash_generator, previous_hash_setter)
    
    # Verify the chain was created correctly
    assert items[0]["previous_hash"] is None
    assert items[1]["previous_hash"] == "hash-item-1"
    assert items[2]["previous_hash"] == "hash-item-2"


def test_create_hash_chain_empty():
    """Test creating a hash chain from an empty list."""
    # Create an empty list of items
    items = []
    
    # Define hash generator and setter functions
    def hash_generator(item):
        return f"hash-{item['id']}"
    
    def previous_hash_setter(item, prev_hash):
        item["previous_hash"] = prev_hash
    
    # Create the hash chain (should not raise an exception)
    create_hash_chain(items, hash_generator, previous_hash_setter)
    
    # Verify the empty list is unchanged
    assert items == []