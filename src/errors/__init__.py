class ValueWarning(Warning):
    """
    Warning raised when there is a possible
    value error.
    """
    pass


class ImproperConfig(Exception):
    """
    Exception raised when an object is improperly configured.
    """
    pass


class DuplicateIndex(Exception):
    """
    If an index needs to be unique.
    """
    pass


class DivisionError(Exception):
    pass


class ImproperType(Exception):
    """
    Exception raised when the wrong type is passed.
    """
    pass
