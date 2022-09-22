import logging

from database.dao import Database


class Expensieve(object):
    VERSION = "0.1"

    def __init__(self, config):
        self.logger = logging.getLogger(__name__)
        self.config = config
        self.logger.info(f"Expensieve {self.VERSION}")
        self.logger.info(f"config {self.config['version']}")
        self.db = Database(self.config["database"])

    def run(self):
        self.logger.info("Expensieve app running")
        self.db_test()
        self.logger.info("Expensieve app exiting")

    def db_test(self):
        self.db.drop_tables()
        self.db.create_tables()
        self.logger.info("creating new user")
        self.db.create_user(username="tlyngen", password="hello123")
        password = self.db.get_user_password("tlyngen")
        self.logger.info(f"user password: {password}")
