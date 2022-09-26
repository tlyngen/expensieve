import sys
import logging
import argparse
import yaml
import traceback

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
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(
        filename='app.log',
        format=log_format,
        datefmt=dateformat,
        level=logging.DEBUG)
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    console_format = '%(name)s - %(levelname)s - %(message)s'
    console_formatter = logging.Formatter(console_format)
    console.setFormatter(console_formatter)
    logging.getLogger('').addHandler(console)


def load_config():
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)


if __name__ == "__main__":
    app_description = """Expensieve - Expense sharing app for human beings"""
    parser = argparse.ArgumentParser(
        description=app_description,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    args = parser.parse_args()
    sys.exit(main(args))
