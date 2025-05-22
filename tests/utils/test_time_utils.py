"""
Tests for the time_utils module.
"""
import pytest
from datetime import datetime, timedelta

from universal_history.utils.time_utils import (
    parse_iso_date, format_iso_date, date_range, group_by_period,
    calculate_time_difference, parse_duration, format_duration,
    get_time_periods_between
)


def test_parse_iso_date():
    """Test parsing an ISO format date string."""
    # Test with a valid ISO format date string
    date_str = "2023-01-01T12:30:45"
    dt = parse_iso_date(date_str)
    
    # Verify the result
    assert isinstance(dt, datetime)
    assert dt.year == 2023
    assert dt.month == 1
    assert dt.day == 1
    assert dt.hour == 12
    assert dt.minute == 30
    assert dt.second == 45


def test_parse_iso_date_invalid():
    """Test parsing an invalid ISO format date string."""
    # Test with an invalid ISO format date string
    date_str = "invalid-date"
    
    # Verify that an exception is raised
    with pytest.raises(ValueError):
        parse_iso_date(date_str)


def test_format_iso_date():
    """Test formatting a datetime as an ISO format string."""
    # Test with a datetime object
    dt = datetime(2023, 1, 1, 12, 30, 45)
    date_str = format_iso_date(dt)
    
    # Verify the result
    assert isinstance(date_str, str)
    assert date_str == "2023-01-01T12:30:45"


def test_date_range():
    """Test generating a list of dates within a range."""
    # Test with a range of dates
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 1, 5)
    dates = date_range(start_date, end_date)
    
    # Verify the result
    assert isinstance(dates, list)
    assert len(dates) == 5
    assert dates[0] == datetime(2023, 1, 1)
    assert dates[1] == datetime(2023, 1, 2)
    assert dates[2] == datetime(2023, 1, 3)
    assert dates[3] == datetime(2023, 1, 4)
    assert dates[4] == datetime(2023, 1, 5)


def test_date_range_with_interval():
    """Test generating a list of dates with a custom interval."""
    # Test with a range of dates and a custom interval
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 1, 10)
    dates = date_range(start_date, end_date, timedelta(days=2))
    
    # Verify the result
    assert isinstance(dates, list)
    assert len(dates) == 5
    assert dates[0] == datetime(2023, 1, 1)
    assert dates[1] == datetime(2023, 1, 3)
    assert dates[2] == datetime(2023, 1, 5)
    assert dates[3] == datetime(2023, 1, 7)
    assert dates[4] == datetime(2023, 1, 9)


def test_date_range_same_date():
    """Test generating a list of dates when start and end are the same."""
    # Test with the same start and end date
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 1, 1)
    dates = date_range(start_date, end_date)
    
    # Verify the result
    assert isinstance(dates, list)
    assert len(dates) == 1
    assert dates[0] == datetime(2023, 1, 1)


def test_group_by_period_day():
    """Test grouping items by day."""
    # Create test items
    items = [
        {"id": "1", "date": "2023-01-01T12:00:00", "value": 10},
        {"id": "2", "date": "2023-01-01T18:00:00", "value": 20},
        {"id": "3", "date": "2023-01-02T12:00:00", "value": 30},
        {"id": "4", "date": "2023-01-03T12:00:00", "value": 40}
    ]
    
    # Group by day
    result = group_by_period(items, "date", "day")
    
    # Verify the result
    assert isinstance(result, dict)
    assert len(result) == 3
    assert "2023-01-01" in result
    assert "2023-01-02" in result
    assert "2023-01-03" in result
    assert len(result["2023-01-01"]) == 2
    assert len(result["2023-01-02"]) == 1
    assert len(result["2023-01-03"]) == 1


def test_group_by_period_month():
    """Test grouping items by month."""
    # Create test items
    items = [
        {"id": "1", "date": "2023-01-15T12:00:00", "value": 10},
        {"id": "2", "date": "2023-01-20T18:00:00", "value": 20},
        {"id": "3", "date": "2023-02-15T12:00:00", "value": 30},
        {"id": "4", "date": "2023-03-15T12:00:00", "value": 40}
    ]
    
    # Group by month
    result = group_by_period(items, "date", "month")
    
    # Verify the result
    assert isinstance(result, dict)
    assert len(result) == 3
    assert "2023-01" in result
    assert "2023-02" in result
    assert "2023-03" in result
    assert len(result["2023-01"]) == 2
    assert len(result["2023-02"]) == 1
    assert len(result["2023-03"]) == 1


def test_group_by_period_invalid_period():
    """Test grouping items with an invalid period."""
    # Create test items
    items = [
        {"id": "1", "date": "2023-01-01T12:00:00", "value": 10}
    ]
    
    # Verify that an exception is raised
    with pytest.raises(ValueError) as excinfo:
        group_by_period(items, "date", "invalid")
    
    # Verify the error message
    assert "Invalid period" in str(excinfo.value)


def test_group_by_period_missing_date():
    """Test grouping items with missing date values."""
    # Create test items with missing dates
    items = [
        {"id": "1", "date": "2023-01-01T12:00:00", "value": 10},
        {"id": "2", "value": 20},  # Missing date
        {"id": "3", "date": "2023-01-02T12:00:00", "value": 30}
    ]
    
    # Group by day
    result = group_by_period(items, "date", "day")
    
    # Verify the result
    assert isinstance(result, dict)
    assert len(result) == 2
    assert "2023-01-01" in result
    assert "2023-01-02" in result
    assert len(result["2023-01-01"]) == 1
    assert len(result["2023-01-02"]) == 1


def test_group_by_period_invalid_date():
    """Test grouping items with invalid date values."""
    # Create test items with invalid dates
    items = [
        {"id": "1", "date": "2023-01-01T12:00:00", "value": 10},
        {"id": "2", "date": "invalid-date", "value": 20},  # Invalid date
        {"id": "3", "date": "2023-01-02T12:00:00", "value": 30}
    ]
    
    # Group by day
    result = group_by_period(items, "date", "day")
    
    # Verify the result
    assert isinstance(result, dict)
    assert len(result) == 2
    assert "2023-01-01" in result
    assert "2023-01-02" in result
    assert len(result["2023-01-01"]) == 1
    assert len(result["2023-01-02"]) == 1


def test_calculate_time_difference_days():
    """Test calculating the time difference in days."""
    # Test with two dates
    start_date = "2023-01-01T12:00:00"
    end_date = "2023-01-05T12:00:00"
    diff = calculate_time_difference(start_date, end_date, "days")
    
    # Verify the result
    assert diff == 4.0


def test_calculate_time_difference_hours():
    """Test calculating the time difference in hours."""
    # Test with two dates
    start_date = "2023-01-01T12:00:00"
    end_date = "2023-01-01T16:00:00"
    diff = calculate_time_difference(start_date, end_date, "hours")
    
    # Verify the result
    assert diff == 4.0


def test_calculate_time_difference_with_datetime_objects():
    """Test calculating the time difference with datetime objects."""
    # Test with datetime objects
    start_date = datetime(2023, 1, 1, 12, 0, 0)
    end_date = datetime(2023, 1, 5, 12, 0, 0)
    diff = calculate_time_difference(start_date, end_date, "days")
    
    # Verify the result
    assert diff == 4.0


def test_calculate_time_difference_invalid_unit():
    """Test calculating the time difference with an invalid unit."""
    # Test with an invalid unit
    start_date = "2023-01-01T12:00:00"
    end_date = "2023-01-05T12:00:00"
    
    # Verify that an exception is raised
    with pytest.raises(ValueError) as excinfo:
        calculate_time_difference(start_date, end_date, "invalid")
    
    # Verify the error message
    assert "Invalid unit" in str(excinfo.value)


def test_parse_duration():
    """Test parsing an ISO 8601 duration string."""
    # Test with a valid duration string
    duration_str = "P1Y2M3DT4H5M6S"
    td = parse_duration(duration_str)
    
    # Verify the result
    assert isinstance(td, timedelta)
    assert td.days == 3 + 30*2 + 365*1  # 3 days + 2 months + 1 year
    assert td.seconds == 4*3600 + 5*60 + 6  # 4 hours + 5 minutes + 6 seconds


def test_parse_duration_days_only():
    """Test parsing a duration string with only days."""
    # Test with a duration string with only days
    duration_str = "P5D"
    td = parse_duration(duration_str)
    
    # Verify the result
    assert isinstance(td, timedelta)
    assert td.days == 5
    assert td.seconds == 0


def test_parse_duration_time_only():
    """Test parsing a duration string with only time components."""
    # Test with a duration string with only time components
    duration_str = "PT6H7M8S"
    td = parse_duration(duration_str)
    
    # Verify the result
    assert isinstance(td, timedelta)
    assert td.days == 0
    assert td.seconds == 6*3600 + 7*60 + 8  # 6 hours + 7 minutes + 8 seconds


def test_parse_duration_invalid():
    """Test parsing an invalid duration string."""
    # Test with an invalid duration string
    duration_str = "invalid-duration"
    
    # Verify that an exception is raised
    with pytest.raises(ValueError) as excinfo:
        parse_duration(duration_str)
    
    # Verify the error message
    assert "Invalid ISO 8601 duration" in str(excinfo.value)


def test_format_duration():
    """Test formatting a timedelta as an ISO 8601 duration string."""
    # Test with a timedelta object
    td = timedelta(days=5, hours=6, minutes=7, seconds=8)
    duration_str = format_duration(td)
    
    # Verify the result
    assert isinstance(duration_str, str)
    assert duration_str == "P5DT6H7M8S"


def test_format_duration_days_only():
    """Test formatting a timedelta with only days."""
    # Test with a timedelta object with only days
    td = timedelta(days=5)
    duration_str = format_duration(td)
    
    # Verify the result
    assert isinstance(duration_str, str)
    assert duration_str == "P5D"


def test_format_duration_time_only():
    """Test formatting a timedelta with only time components."""
    # Test with a timedelta object with only time components
    td = timedelta(hours=6, minutes=7, seconds=8)
    duration_str = format_duration(td)
    
    # Verify the result
    assert isinstance(duration_str, str)
    assert duration_str == "PT6H7M8S"


def test_format_duration_zero():
    """Test formatting a zero timedelta."""
    # Test with a zero timedelta
    td = timedelta(0)
    duration_str = format_duration(td)
    
    # Verify the result
    assert isinstance(duration_str, str)
    assert duration_str == "PT0S"


def test_get_time_periods_between_days():
    """Test getting time periods between two dates by day."""
    # Test with a range of dates
    start_date = "2023-01-01T00:00:00"
    end_date = "2023-01-03T23:59:59"
    periods = get_time_periods_between(start_date, end_date, "day")
    
    # Verify the result
    assert isinstance(periods, list)
    assert len(periods) == 3
    
    # Check the first period
    assert periods[0][0] == datetime(2023, 1, 1, 0, 0, 0)
    assert periods[0][1] == datetime(2023, 1, 1, 23, 59, 59)
    
    # Check the second period
    assert periods[1][0] == datetime(2023, 1, 2, 0, 0, 0)
    assert periods[1][1] == datetime(2023, 1, 2, 23, 59, 59)
    
    # Check the third period
    assert periods[2][0] == datetime(2023, 1, 3, 0, 0, 0)
    assert periods[2][1] == datetime(2023, 1, 3, 23, 59, 59)


def test_get_time_periods_between_months():
    """Test getting time periods between two dates by month."""
    # Test with a range of dates
    start_date = "2023-01-15T00:00:00"
    end_date = "2023-03-15T00:00:00"
    periods = get_time_periods_between(start_date, end_date, "month")
    
    # Verify the result
    assert isinstance(periods, list)
    assert len(periods) == 3
    
    # Check the first period
    assert periods[0][0] == datetime(2023, 1, 15, 0, 0, 0)
    assert periods[0][1] == datetime(2023, 1, 31, 23, 59, 59)
    
    # Check the second period
    assert periods[1][0] == datetime(2023, 2, 1, 0, 0, 0)
    assert periods[1][1] == datetime(2023, 2, 28, 23, 59, 59)
    
    # Check the third period
    assert periods[2][0] == datetime(2023, 3, 1, 0, 0, 0)
    assert periods[2][1] == datetime(2023, 3, 15, 0, 0, 0)


def test_get_time_periods_between_invalid_period():
    """Test getting time periods with an invalid period."""
    # Test with an invalid period
    start_date = "2023-01-01T00:00:00"
    end_date = "2023-01-31T23:59:59"
    
    # Verify that an exception is raised
    with pytest.raises(ValueError) as excinfo:
        get_time_periods_between(start_date, end_date, "invalid")
    
    # Verify the error message
    assert "Invalid period" in str(excinfo.value)