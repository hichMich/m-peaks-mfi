###
    # welcome to exceptions.py, this file contain all type of exceptions, the common and the custom ones.
###

class ServiceException(Exception):
    def __init__(self, msg: str = None, code_status: int = None):
        self.msg = msg
        self.code_status = code_status


class ServiceTechnicalException(ServiceException):
    """
        This exception covers issues coming from the db or the API...
    """
    pass


class ServiceFunctionalException(ServiceException):
    """
        This exception covers issues originating from users (input/actions...)
    """
    pass