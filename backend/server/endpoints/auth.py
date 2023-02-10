from fastapi import APIRouter, Depends, Response, status
from fastapi.responses import JSONResponse

from server.exceptions.user import UserExists
from server.schemas.signup import SignUpRequest
from server.usecase.registration import register_user


api = APIRouter(tags=["Auth"])


@api.post(
    "/auth/signup",
    status_code=status.HTTP_201_CREATED,
    response_class=Response,
)
async def signup(credentials: SignUpRequest = Depends(SignUpRequest.as_form)):
    try:
        await register_user(credentials)
    except UserExists as err:
        return JSONResponse({"message": str(err)}, status.HTTP_409_CONFLICT)
