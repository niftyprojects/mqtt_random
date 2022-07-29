import random
import time
from unittest.mock import MagicMock

from rand_source import RandomSource


class MockClient:
    def __init__(self):
        self.publish = MagicMock()


def test_pubval_generates_random_number_in_correct_range(monkeypatch):
    """The generated random number must be >=1 and < 100."""
    rnd_mock = MagicMock(return_value=1)
    monkeypatch.setattr(random, "randint", rnd_mock)

    rs = RandomSource(MockClient())
    rs.publish_value()

    rnd_mock.assert_called_with(1, 99)


def test_pubval_publishes_the_provided_number(monkeypatch):
    """The random number has to be pushed to the random/value topic."""
    rnd_mock = MagicMock(return_value=42)
    monkeypatch.setattr(random, "randint", rnd_mock)

    cli_mock = MockClient()
    rs = RandomSource(client=cli_mock)
    rs.publish_value()

    cli_mock.publish.assert_called_with("random/value", 42)


def test_pubval_publishes_to_a_user_provided_topic(monkeypatch):
    """The random number has to be pushed to a user provided topic."""
    rnd_mock = MagicMock(return_value=83)
    monkeypatch.setattr(random, "randint", rnd_mock)

    cli_mock = MockClient()
    rs = RandomSource(client=cli_mock, topic="new/topic")
    rs.publish_value()

    cli_mock.publish.assert_called_with("new/topic", 83)


def test_wait_interval_gets_random_time_in_correct_range(monkeypatch):
    """The wait interval must be a random interval in the range >=1 and < 30."""
    rnd_mock = MagicMock(return_value=0)
    monkeypatch.setattr(random, "randint", rnd_mock)

    rs = RandomSource(MockClient())
    rs.wait_interval()

    rnd_mock.assert_called_with(1, 29)


def test_wait_interval_sleeps_for_the_time_period(monkeypatch):
    """The random interval should be waited on."""
    rnd_mock = MagicMock(return_value=17)
    monkeypatch.setattr(random, "randint", rnd_mock)

    sleep_mock = MagicMock()
    monkeypatch.setattr(time, "sleep", sleep_mock)

    rs = RandomSource(MockClient())
    rs.wait_interval()

    sleep_mock.assert_called_with(17)
