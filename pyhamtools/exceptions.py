# !/usr/bin/python
# Filename: exceptions.py

class LookupError(KeyError):
    """ Error while accessing the class """
    pass

class NoResult(KeyError):
    """ No matching result found """
    pass

class APIKeyMissingError(AttributeError):
    """ API Key is Missing """
    pass