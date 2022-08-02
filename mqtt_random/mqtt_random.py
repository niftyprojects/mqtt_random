import argparse
import logging

from mqtt_random.connection import mqtt_client
from mqtt_random.source import RandomSource

LOG_LEVEL = {
    "debug": logging.DEBUG,
    "warn": logging.WARN,
    "error": logging.ERROR,
    "info": logging.INFO,
}


def run_random(broker: str = "mqtt://localhost"):
    client = mqtt_client(broker)
    rand_source = RandomSource(client)
    client.loop_start()
    rand_source.run()
    client.loop_stop()


def main():
    parser = argparse.ArgumentParser(
        description="Publishes random numbers to MQTT broker."
    )
    parser.add_argument(
        "--log_level",
        help="Set the logging level. Default error",
        choices=LOG_LEVEL.keys(),
        default="warn",
    )
    parser.add_argument(
        "broker",
        default="mqtt://localhost",
        help="MQTT broker URL, default mqtt://localhost",
        nargs="?",
    )
    args = parser.parse_args()

    logging.basicConfig(level=LOG_LEVEL[args.log_level])

    run_random(broker=args.broker)


if __name__ == "__main__":
    main()
