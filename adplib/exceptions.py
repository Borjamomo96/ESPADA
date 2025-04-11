class RecoverableError(Exception):
    """Base para errores que permiten continuar la ejecución"""
    pass

class RecoverableValueError(ValueError, RecoverableError):
    """ValueError que no detiene el programa"""
    pass

class RecoverableFileNotFoundError(FileNotFoundError, RecoverableError):
    """FileNotFoundError recuperable"""
    pass