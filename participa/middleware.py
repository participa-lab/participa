# middleware.py
from django.utils.deprecation import MiddlewareMixin
from participa.logging_filters import SessionIDFilter
import logging


class SessionIDMiddleware(MiddlewareMixin):
    def process_request(self, request):
        session_id = request.session.session_key
        if not session_id:
            request.session.create()
            session_id = request.session.session_key

        # Set the session ID in the logging filter
        for handler in logging.getLogger().handlers:
            for filter in handler.filters:
                if isinstance(filter, SessionIDFilter):
                    filter.set_session_id(session_id)
