from fastapi import HTTPException, status


class InvalidSignature(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=[{"msg": "your message signature is invalid", "loc": ["backend"]}],
        )
