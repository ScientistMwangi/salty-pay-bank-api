from asyncio import exceptions
from rest_framework.views import exception_handler
import logging

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)
    try:
        logger.critical(exc.get_full_details())
    except:
        logger.critical("Exception unknown thrown")
    # Now add the HTTP status code to the response.
    if response is not None:
        response.data['status_code'] = response.status_code
    #print('MyCustom Exception handler', response)
    return response


""" def custom_exception_handler(exc, context):
    handlers = {
        'Http404': _handle_not_found,
        'NotAuthenticated': _handle_auth_error
    }
    response = exception_handler(exc, context)
    print('MyCustom Exception handler', response)
    exception_class = exc.__class__.__name__
    if exception_class in handlers:
        return handlers[exception_class](exc, context, response)
    return response """


def _handle_not_found(exc, context, response):
    response.data = {'error': 'this resource does not exist'}


def _handle_auth_error(exc, context, response):
    response.data = {'error': 'auth error this resource does not exist'}
