class NoAFRException(Exception):
    """
    Represents when an Annual Financial Report is not found
    """
    pass


class InvalidOptionException(Exception):
    """
    Represents when an option is not valid
    """
    pass


class EntryExistsException(Exception):
    """
    Represents when an entry already exists
    """
    pass