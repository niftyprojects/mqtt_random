import logging
import random
import time


class RandomSource:
    """Publishes random numbers to a MQTT broker at random intervals."""

    def __init__(self, client, topic="random/value"):
        """Create a source of random numbers.

        Arguments:
        client
          A connected paho MQTT client.

        topic
          The topic to publish random numbers to. 'random/value' by default.
        """
        self.client = client
        self.topic = topic

    def publish_value(self):
        """Generate a random value and publish it."""
        val = random.randint(1, 99)
        self.client.publish(self.topic, val)
        logging.info(f"Published {val}")

    def wait_interval(self):
        """Wait for a random interval."""
        val = random.randint(1, 29)
        logging.debug(f"Sleeping for {val} seconds.")
        time.sleep(val)


LOG_LEVEL = {
    "debug": logging.DEBUG,
    "warn": logging.WARN,
    "error": logging.ERROR,
    "info": logging.INFO,
}


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Publishes random numbers to MQTT broker."
    )
    parser.add_argument(
        "--log_level",
        help="Set the logging level. Default error",
        choices=LOG_LEVEL.keys(),
        default="warn",
    )
    args = parser.parse_args()

    logging.basicConfig(level=LOG_LEVEL[args.log_level])
