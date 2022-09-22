import sys
import logging
import argparse
import yaml
import traceback
#import os

from expensieve import ExpensieveApp


def main(args):
    try:
        configure_logging()
        logger = logging.getLogger("main")
        config = load_config()
        ExpensieveApp(config).run()
    except Exception as e:
        logger.error(f"Exception: {e}")
        logger.error(traceback.format_exc())


def configure_logging():
    dateformat = '%Y-%m-%d %H:%M:%S %p'
    logformat = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(
        filename='app.log',
        format=logformat,
        datefmt=dateformat,
        level=logging.DEBUG)
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    console_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    console.setFormatter(console_format)
    logging.getLogger('').addHandler(console)


def load_config():
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)


if __name__ == "__main__":
    app_description = """Expensieve - An expense sharing app for human beings"""
    parser = argparse.ArgumentParser(
        description=app_description,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    args = parser.parse_args()
    sys.exit(main(args))
