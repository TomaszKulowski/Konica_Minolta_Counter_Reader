"""
Unit Tests for the 'utils.message.py' module.
"""
from freezegun import freeze_time
import pytest

from utils.schedule import Schedule


@pytest.mark.parametrize(
    'period_of_time, expected_result', (
            ('day', 'day'),
            ('month', 'month'),
            ('year', 'year'),
    )
)
def test_successfully_set_call_every_attribute(period_of_time: str, expected_result: str):
    """
    Test whether the call_every method successfully sets the call interval attribute.

    Parameters:
        period_of_time (str): A string representing the period of time
            to set the call interval (e.g., 'day', 'month', 'year').
        expected_result (str): The expected result after setting the call interval,
            which should match the period_of_time parameter.
    """
    schedule = Schedule(1, 20)
    schedule.call_every(period_of_time)

    result = schedule.get_call_every()

    assert result == expected_result


@pytest.mark.parametrize(
    'wrong_period_of_time', (
            'days',
            'months',
            'years',
            'monday',
            'october',
    )
)
def test_unsuccessfully_set_call_every_attribute(wrong_period_of_time: str):
    """
    Test whether the call_every method raises a ValueError when an invalid period_of_time is provided.

    Parameters:
        wrong_period_of_time (str): A string representing an invalid period of time
            (e.g., 'days', 'months', 'years', 'monday', 'october').
    """
    schedule = Schedule(1, 20)

    with pytest.raises(ValueError) as error:
        schedule.call_every(wrong_period_of_time)

    assert error.type == ValueError


@pytest.mark.parametrize(
    'period_of_time, call, expected_result, next_call, interval', (
        ('day', 21, True, 23, 1),
        ('day', 21, True, 25, 3),
        ('day', 22, True, 23, 1),
        ('day', 23, False, 23, 1),
        ('month', 9, True, 11, 1),
        ('month', 9, True, 12, 2),
        ('month', 10, True, 11, 1),
        ('month', 11, False, 11, 1),
        ('year', 2021, True, 2023, 1),
        ('year', 2021, True, 2027, 5),
        ('year', 2022, True, 2023, 1),
        ('year', 2023, False, 2023, 1),
    )
)
@freeze_time('2022-10-22 19:46')
def test_check_time(period_of_time: str, call: int, expected_result: bool, next_call: int, interval: int):
    """
    Test whether the check_time method correctly determines if it's time to make a call based on the specified period of time and call time.

    Parameters:
        period_of_time (str): A string representing the period of time for scheduling (e.g., 'day', 'month', 'year').
        call (int): The call time to be scheduled.
        expected_result (bool): The expected result indicating whether it's time to make a call.
        next_call (int): The expected time for the next call.
        interval (int): The interval between calls.
    """
    schedule = Schedule(interval, call)
    schedule.call_every(period_of_time)

    result = schedule.check_time()

    assert result == expected_result
    assert schedule.next_call == next_call
