from fastapi import APIRouter, Depends, Response, status
from fastapi.responses import JSONResponse

from server.exceptions.user import InvalidCredentials, UserExists, UserNotFound
from server.schemas.signin import CodeRequest, CodeResponse, SignInRequest
from server.schemas.signup import SignUpRequest
from server.tools.hash import get_hash
from server.usecase.authentication import auth_by_code
from server.usecase.code_generation import get_code
from server.usecase.registration import register_user


api = APIRouter(tags=["Auth"], prefix="/auth")


@api.post(
    "/signup",
    status_code=status.HTTP_201_CREATED,
    response_class=Response,
)
async def signup(credentials: SignUpRequest = Depends(SignUpRequest.as_form)):
    try:
        await register_user(credentials)
    except UserExists as err:
        return JSONResponse({"message": str(err)}, status.HTTP_409_CONFLICT)


@api.post(
    "/signin",
    status_code=status.HTTP_202_ACCEPTED,
    response_class=Response,
)
async def singin(credentials: SignInRequest):
    try:
        await auth_by_code(credentials)
    except UserNotFound as err:
        return JSONResponse({"message": str(err)}, status.HTTP_404_NOT_FOUND)
    except InvalidCredentials as err:
        return JSONResponse({"message": str(err)}, status.HTTP_401_UNAUTHORIZED)


@api.post(
    "/code",
    status_code=status.HTTP_200_OK,
    response_model=CodeResponse,
)
async def code(credentials: CodeRequest):
    try:
        code = await get_code(credentials.username)
    except UserNotFound as err:
        return JSONResponse({"message": str(err)}, status.HTTP_404_NOT_FOUND)
    return CodeResponse(code=get_hash(str(code)))
