import logging

from sqlalchemy.orm import sessionmaker


class Session:
    def __init__(self, engine):
        self.logger = logging.getLogger(__name__)
        self.logger.debug("creating session")
        Session = sessionmaker()
        Session.configure(bind=engine)
        self.session = Session()

    def __enter__(self):
        return self.session

    def __exit__(self, type, value, traceback):
        self.session.commit()
        self.session.close()
        self.logger.debug("closed session")
