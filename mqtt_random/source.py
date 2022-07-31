import logging
import random
import time

import paho.mqtt.client as mqtt


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
        res = self.client.publish(self.topic, val)
        if res.rc != mqtt.MQTT_ERR_SUCCESS:
            logging.error(f"Message {res.mid} not sent: {mqtt.error_string(res.rc)}")
        else:
            logging.info(f"Published {val} with id {res.mid}")

    def wait_interval(self):
        """Wait for a random interval."""
        val = random.randint(1, 29)
        logging.debug(f"Sleeping for {val} seconds.")
        time.sleep(val)

    def run(self):
        """Publish values until interrupted.

        KeyboardInterrupt or SIGINT will break out of the loop."""
        try:
            logging.info("RandomSource started.")
            while True:
                self.publish_value()
                self.wait_interval()
        except KeyboardInterrupt:
            logging.info("RandomSource stopped.")
