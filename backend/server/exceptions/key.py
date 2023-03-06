from fastapi import HTTPException, status


class KeyNotFound(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND, detail=[{"msg": "your is key not found", "loc": ["backend"]}]
        )
