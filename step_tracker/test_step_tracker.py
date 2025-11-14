from datetime import date
import pytest

import step_tracker as sd

def test_validate_step_data():
    today_date = date.today()
    input_date = date(2025, 11, 10)
    assert input_date == sd.validate_step_date(input_date, today_date)

def test_sort_date_and_steps():
    sd.steps_count = [3000, 1000]
    sd.dates = [date(2025, 11, 11), date(2025, 11, 8)]
    sorted_dates, sorted_steps = sd.sort_date_and_steps()
    assert sorted_dates == ["08-11-2025", "11-11-2025"]
    assert sorted_steps == (1000, 3000)


def test_sort_date_and_steps_for_week():
    sd.steps_count = [3000, 1000, 7000]
    sd.dates = [date(2025, 11, 11), date(2025, 11, 8), date(2025, 11, 13)]
    sorted_dates, sorted_steps = sd.sort_date_and_steps()
    assert sorted_dates == ["08-11-2025", "11-11-2025","13-11-2025"]
    assert sorted_steps == (1000, 3000, 7000)