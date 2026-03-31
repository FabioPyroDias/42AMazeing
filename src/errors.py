class InvalidParameterError(Exception):
    """
    Exception raised when an unknown or unsupported parameter is found
    in the configuration file.
    """
    pass


class InvalidConfigurationError(Exception):
    """
    Exception raised when the configuration file structure is invalid,
    such as missing required keys or duplicated parameters.
    """
    pass


class InvalidValueError(Exception):
    """
    Exception raised when a configuration parameter has an invalid value
    or does not meet the expected format or constraints.
    """
    pass
