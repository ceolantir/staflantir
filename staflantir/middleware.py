from django.shortcuts import redirect


class Process:
    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request):
        return self._get_response(request)

    def process_exception(self, request, exception):
        if str(exception) == 'BadUserID':
            return redirect(f'/error/BadUserID')
        elif str(exception) == 'ProfileIsPrivate':
            return redirect(f'/error/ProfileIsPrivate')
        elif str(exception) == 'UserDeletedOrBanned':
            return redirect(f'/error/UserDeletedOrBanned')
        elif str(exception) == 'UnidentifiedError':
            return redirect(f'/error/UnidentifiedError')
