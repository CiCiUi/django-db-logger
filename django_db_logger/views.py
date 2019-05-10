import logging

from django.http import HttpResponse

logger = logging.getLogger('db')

def __gen_500_errors(request):
    try:
        1/0
    except Exception as e:
        logger.exception(e)

    return HttpResponse('Hello 500!')
