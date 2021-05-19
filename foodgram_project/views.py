from django.shortcuts import render


def page_not_found(request, exception):
    response = render(request, '404.html')
    response.status_code = 404
    return response


def forbidden(request, exception):
    response = render(request, '404.html')
    response.status_code = 403
    return response


def bed_request(request, exception):
    response = render(request, '404.html')
    response.status_code = 400
    return response


def interall_error(request):
    response = render(request, '500.html')
    response.status_code = 500
    return response
