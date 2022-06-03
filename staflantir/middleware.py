from django.shortcuts import redirect


error_tuple = (
    'BadUserID',
    'ProfileIsPrivate',
    'UserDeletedOrBanned',
    'UnidentifiedError',
    'PhoneError',
)


class Process:
    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request):
        return self._get_response(request)

    def process_exception(self, request, exception):
        if str(exception) in error_tuple:
            return redirect(f'/error/{str(exception)}')
