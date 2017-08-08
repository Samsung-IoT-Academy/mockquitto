class CreationException(Exception):
    """
    Exception raised in creation of objects
    """
    def __init__(self, msg=None):
        self.message = msg


class DeviceCreationError(CreationException):
    """
    Exception raised if was error in creating device
    """
    def __init__(self, msg="Error while creating device"):
        super().__init__(msg)

class GeneratorCreationError(CreationException):
    """
    Exception raised if was error in creating device
    """
    def __init__(self, msg="Error while creating generator"):
        super().__init__(msg)

class LawCreationError(CreationException):
    """
    Exception raised when creating distribution law class
    """
    def __init__(self, msg="Error while creating distribution law"):
        super().__init__(msg)
