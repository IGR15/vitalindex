from rest_framework.views import exception_handler
from rest_framework.exceptions import NotAuthenticated, AuthenticationFailed
from rest_framework.response import Response
from rest_framework import status
def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, (NotAuthenticated, AuthenticationFailed)):
        return Response({
            "error": "Authentication required",
            "message": "You must provide valid authentication credentials to access this endpoint. Please log in or include a valid token in the Authorization header.",
            "status": 401
        }, status=status.HTTP_401_UNAUTHORIZED)

    return response