from rest_framework.views import exception_handler
from rest_framework.exceptions import NotAuthenticated, AuthenticationFailed
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, (NotAuthenticated, AuthenticationFailed)):
        return Response({
            "error": "Passwords do not match",
            "message": "The provided passwords do not match. Please ensure that both password fields are identical ",
            "status": 401
        }, status=status.HTTP_401_UNAUTHORIZED)

    return response