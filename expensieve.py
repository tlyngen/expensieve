import logging


class ExpensieveApp(object):
    VERSION = "0.1"

    def __init__(self, config):
        self.logger = logging.getLogger(__name__)
        self.config = config
        self.logger.info(f"Expensieve {self.VERSION}")
        self.logger.info(f"config {self.config['version']}")

    def run(self):
        self.logger.info("Expensieve app running")
        self.logger.info("Expensieve app exiting")
