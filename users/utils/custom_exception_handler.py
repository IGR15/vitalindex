from rest_framework.exceptions import NotAuthenticated, AuthenticationFailed
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if isinstance(exc, (InvalidToken, TokenError)):
        return Response({
            "error": "Token expired",
            "message": "Your session has expired. Please re-login.",
            "status": 401
        }, status=status.HTTP_401_UNAUTHORIZED)

    if isinstance(exc, (NotAuthenticated, AuthenticationFailed)):
        return Response({
            "error": "Authentication failed",
            "message": "Passwords do not match or authentication failed.",
            "status": 401
        }, status=status.HTTP_401_UNAUTHORIZED)

    return response
