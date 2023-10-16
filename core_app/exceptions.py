# from rest_framework.exceptions import APIException
# from rest_framework import status
#
# from .utils import _get_error_details
#
#
# class APIExceptionResponseFormatMixin:
#     def __init__(self, detail=None, code=None):
#         if detail is None:
#             detail = self.default_detail
#         if code is None:
#             code = self.default_code
#         if not isinstance(detail, dict) and not isinstance(detail, list):
#             detail = [detail]
#
#         self.detail = _get_error_details(detail, code)
#
#
# class AuthenticationFailed(APIExceptionResponseFormatMixin, APIException):
#     status_code = status.HTTP_401_UNAUTHORIZED
#     default_detail = {"success": False, "message": "Unauthorized",
#                       'status_code': status.HTTP_401_UNAUTHORIZED}
#
#
# class PermissionDenied(APIExceptionResponseFormatMixin, APIException):
#     status_code = status.HTTP_403_FORBIDDEN
#     default_detail = {"success": False, "message": "You do not have permission to perform this action",
#                       'status_code': status.HTTP_403_FORBIDDEN}
#
#
# class InvalidTokenSupplied(APIExceptionResponseFormatMixin, APIException):
#     status_code = status.HTTP_401_UNAUTHORIZED
#     default_detail = {"success": False, "message": "Invalid token supplied",
#                       'status_code': status.HTTP_401_UNAUTHORIZED}
#
#
# class AuthenticationRequired(APIExceptionResponseFormatMixin, APIException):
#     status_code = status.HTTP_401_UNAUTHORIZED
#     default_detail = {"success": False, "message": "Authentication Required",
#                       'status_code': status.HTTP_401_UNAUTHORIZED}
#
#
# class UserInactiveOrDeleted(APIExceptionResponseFormatMixin, APIException):
#     status_code = status.HTTP_400_BAD_REQUEST
#     default_detail = {"success": False, "message": "User Inactive or Deleted",
#                       'status_code': status.HTTP_400_BAD_REQUEST}
#
#
# class TokenExpired(APIExceptionResponseFormatMixin, APIException):
#     status_code = status.HTTP_401_UNAUTHORIZED
#     default_detail = {"success": False, "message": "Token has expired",
#                       'status_code': status.HTTP_401_UNAUTHORIZED}
#
#
# class InternalServerError(APIExceptionResponseFormatMixin, APIException):
#     status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
#     default_detail = {"success": False, "message": "Something went wrong",
#                       'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR}
#
#
# class MethodNotAllowed(APIExceptionResponseFormatMixin, APIException):
#     status_code = status.HTTP_405_METHOD_NOT_ALLOWED
#     default_detail = {"success": False, "message": "This method is not allowed",
#                       'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR}
#
#
# class SuperUserCreationDenied(PermissionDenied):
#     default_detail = {"success": False, "message": "You do not have permission create another Super User",
#                       'status_code': status.HTTP_403_FORBIDDEN}
#
#
# class SiteAdminCreationDenied(PermissionDenied):
#     default_detail = {"success": False, "message": "You do not have permission create another Site Administrator",
#                       'status_code': status.HTTP_403_FORBIDDEN}
#
#
# class SupervisorCreationDenied(PermissionDenied):
#     default_detail = {"success": False, "message": "You do not have permission create another Supervisor",
#                       'status_code': status.HTTP_403_FORBIDDEN}
#
#
# __all__ = [
#     "AuthenticationFailed",
#     "PermissionDenied",
#     "TokenExpired",
#     "UserInactiveOrDeleted",
#     "InvalidTokenSupplied",
#     "InternalServerError",
#     "AuthenticationRequired",
#     "SupervisorCreationDenied",
#     "SiteAdminCreationDenied",
#     "SupervisorCreationDenied",
#     "MethodNotAllowed"
# ]
