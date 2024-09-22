import logging


class SessionIDFilter(logging.Filter):
    def __init__(self, name=""):
        super().__init__(name)
        self.session_id = None

    def set_session_id(self, session_id):
        self.session_id = session_id

    def filter(self, record):
        record.session_id = self.session_id
        return True
