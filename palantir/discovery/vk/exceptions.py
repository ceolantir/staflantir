class BadUserID(Exception):
    pass


class ProfileIsPrivate(Exception):
    pass


class UserDeletedOrBanned(Exception):
    pass


class UnidentifiedError(Exception):
    pass
