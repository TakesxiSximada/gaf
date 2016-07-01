class GafError(Exception):
    pass


class AuthTokenCreationError(GafError):
    pass


class NoRepositoryError(GafError):
    pass


class DuplicateReealseError(GafError):
    pass
