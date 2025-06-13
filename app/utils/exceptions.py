class ResourceNotFoundError(Exception):
    """Raised when a requested resource is not found"""
    pass

class DuplicateResourceError(Exception):
    """Raised when attempting to create a resource that already exists"""
    pass

class ValidationError(Exception):
    """Raised when input validation fails"""
    pass

class AuthenticationError(Exception):
    """Raised when authentication fails"""
    pass

class AuthorizationError(Exception):
    """Raised when user doesn't have permission to access a resource"""
    pass