A random number source that publishes to a MQTT broker

## Instalation

Clone the repository and run the following commands:

```bash
pipenv install --deploy
```

## Development Setup

```bash
pipenv install --dev
pipenv run pre-commit install
```

## Usage

```console
usage: mqtt_random.py [-h] [--log_level {debug,warn,error,info}] [broker]

Publishes random numbers to MQTT broker.

positional arguments:
  broker                MQTT broker URL, default mqtt://localhost

options:
  -h, --help            show this help message and exit
  --log_level {debug,warn,error,info}
                        Set the logging level. Default error
```
