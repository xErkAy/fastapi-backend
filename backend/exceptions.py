from starlette.responses import JSONResponse


def ExceptionWithMessage(message: str) -> JSONResponse:
    return JSONResponse(
        content={
            'message': message
        },
        status_code=400
    )


class ValidationException(Exception):
    pass
