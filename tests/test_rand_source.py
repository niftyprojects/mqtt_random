import logging
import random
import time
from unittest.mock import MagicMock

import paho.mqtt.client as mqtt

from mqtt_random import RandomSource


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


def test_pubval_logs_error_on_publish_failure(monkeypatch):
    """If a value fails to be published, a message should be logged."""
    rnd_mock = MagicMock(return_value=11)
    monkeypatch.setattr(random, "randint", rnd_mock)

    log_mock = MagicMock()
    monkeypatch.setattr(logging, "error", log_mock)

    cli_mock = MockClient()
    res = mqtt.MQTTMessageInfo(1234)
    res.rc = mqtt.MQTT_ERR_CONN_LOST
    cli_mock.publish.return_value = res

    rs = RandomSource(client=cli_mock)
    rs.publish_value()

    log_mock.assert_called_with("Message 1234 not sent: The connection was lost.")


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


def test_run_publishes_and_waits_until_keyboard_error():
    """Run should call publish_value and wait_interval repeatiatly until KeyboardError
    is received."""

    rs = RandomSource(MockClient())
    rs.publish_value = MagicMock()
    rs.wait_interval = MagicMock(side_effect=[None, None, KeyboardInterrupt()])

    rs.run()

    assert rs.publish_value.call_count == 3
    assert rs.wait_interval.call_count == 3
