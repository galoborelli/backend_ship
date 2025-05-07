from rest_framework import status

def standard_response(data=None, error=None, http_code_success=status.HTTP_200_OK, http_code_error=status.HTTP_400_BAD_REQUEST):
    if error:
        return {
            "http_code": http_code_error,
            "status": "error",
            "error": error,
        }
    return {
        "http_code": http_code_success,
        "status": "success",
        "data": data,
    }