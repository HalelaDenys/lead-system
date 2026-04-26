class NotFoundError(Exception):
    detail = "Not found"


class AlreadyExistsError(Exception):
    detail = "Already exists"


class UnauthorizedException(Exception):
    detail = "Unauthorized"


class TokenExpiredException(Exception):
    detail = "Token expired"


class InvalidTokenException(Exception):
    detail = "Invalid token"
