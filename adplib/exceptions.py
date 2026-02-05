class RecoverableError(Exception):
    """Basis for errors that allow execution to continue"""
    pass

class RecoverableValueError(ValueError, RecoverableError):
    """ValueError that does not stop the program"""
    pass

class RecoverableFileNotFoundError(FileNotFoundError, RecoverableError):
    """Recoverable FileNotFoundError"""
    pass

class ConfigurationError(Exception):
    """Exception for errors in configuration files (YAML)"""
    pass