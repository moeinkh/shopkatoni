from .models import IpAddress


def saveIpAddress_middleware(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        try:
            ip_address = IpAddress.objects.get(ip_address=ip)
        except IpAddress.DoesNotExist:
            ip_address = IpAddress(ip_address=ip)
            ip_address.save()

        request.user.ip_address = ip_address

        response = get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    return middleware