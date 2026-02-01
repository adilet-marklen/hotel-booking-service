from rest_framework.exceptions import APIException


class ServiceError(APIException):
    status_code = 400
    default_detail = "Service error"
    default_code = "service_error"

    def __init__(self, message: str, status_code: int):
        self.status_code = status_code
        super().__init__(detail={"error": message})


class RoomServiceError(ServiceError):
    pass


class BookingServiceError(ServiceError):
    pass
