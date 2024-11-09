from fastapi import APIRouter, BackgroundTasks, Depends, status, Response, Header
from fastapi.responses import ORJSONResponse
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from app.Config import ENV_PROJECT
from loguru import logger
from pydantic import BaseModel
import app.http_exception as http_exception
from app.database.repositories.college import college_repo
from app.database.repositories.user import user_repo
# from app.database.repositories.sales import sales_repo
from app.schema.password import PasswordUpdate
from app.schema.token import TokenData
import app.http_exception as http_exception
from app.utils.hashing import verify_hash, hash_password
from app.oauth2 import get_current_user
from app.database.repositories.token import refresh_token_repo

# from app.database.connections.mongo import conn
from app.database import mongodb

# from app.database.repositories.token import refresh_token_repo
from app.oauth2 import (
    create_access_token,
    # create_forgot_password_access_token,
    # create_signup_access_token,
    get_new_access_token,
    # verify_forgot_password_access_token,
    # verify_signup_access_token,
    get_refresh_token,
    set_cookies,
)
from app.schema.token import TokenData
from app.schema.enums import Roles
from app.utils import hashing

# from app.utils.mailer_module import mail, template
from app.Config import ENV_PROJECT

# from app.schema.password import SetPassword
from typing import Optional

router = APIRouter()


class TenantID(BaseModel):
    tenant_id: Optional[str] = None
    tenant_email: Optional[str] = None


class Email_Body(BaseModel):
    email: str


@router.post("/login", response_class=ORJSONResponse, status_code=status.HTTP_200_OK)
async def login(
    response: Response,
    user_type: Roles = Roles.Student,
    creds: OAuth2PasswordRequestForm = Depends(),
):
    user = None
    if user_type == Roles.University and creds.username == ENV_PROJECT.ADMIN_EMAIL:
        print("Here")
        user = await user_repo.findOne(
                {"email": creds.username,"accountType":"University"},
                # {"_id", "password","email","username","profileID"},
            )
        print("user",user)
    elif user_type in [Roles.College, Roles.Student]:
        if user_type == Roles.College:
            print("Here")
            print(creds.username)
            print(Roles.College.value)
            user = await user_repo.findOne(
                {"email": creds.username,"accountType":Roles.College.value},
                {"_id", "password","email","username","profileID"},
            )
            print(user)
        elif user_type == Roles.Student:
            user = await user_repo.findOne(
                {"email": creds.username,"accountType":Roles.Student.value},
                {"_id", "password","email","username","profileID"},
            )
    if user is None:
        raise http_exception.ResourceNotFoundException()

    print(user["password"])
    print(creds.password)

    if hashing.verify_hash(creds.password, user["password"]):
        print("i am in hashing if statement")
        token_data = TokenData(
            user_id=user["_id"], user_type=user_type.value, scope="login",email=user["email"],profile_id = user["profileID"],username = user["username"]
        )
        token_generated = await create_access_token(token_data)
        set_cookies(response, token_generated.access_token, token_generated.refresh_token,user["profileID"])
        return {"ok": True}
    print("i am not in hashing if statement")

    raise http_exception.CredentialsInvalidException()


@router.post("/refresh", response_class=ORJSONResponse, status_code=status.HTTP_200_OK)
async def token_refresh(
    response: Response, refresh_token: str = Depends(get_refresh_token)
):
    token_generated,profile_id = await get_new_access_token(refresh_token)
    print(profile_id)
    set_cookies(response, token_generated.access_token, token_generated.refresh_token,profileID=profile_id)
    return {"ok": True}


# @router.post(
#     "/tenant/forgot-password",
#     response_class=ORJSONResponse,
#     status_code=status.HTTP_200_OK,
# )
# async def tenant_forgot_password(
#     email_body: Email_Body, background_tasks: BackgroundTasks
# ):
#     tenant_res = await tenant_repo.findOne(
#         {"tenant_email": email_body.email}, {"onboarded", "_id", "tenant_name"}
#     )
#     if tenant_res is None:
#         raise http_exception.ACCOUNT_NOT_FOUND
#     if not tenant_res["onboarded"]:
#         raise http_exception.CustomHTTPException(
#             message="Please verify your email first to reset your password.",
#             status_code=status.HTTP_403_FORBIDDEN,
#         )
#     access_token = await create_forgot_password_access_token(
#         TokenData(id=tenant_res["_id"], type="tenant", scope="forgot_password")
#     )
#     # ! CHANGE URL TO VERIFY RESET PASSWORD ACCESS TOKEN
#     content = template.Recovery(
#         "http://localhost:8009/api/v1/auth/tenant/forgot-password/verify?token="
#         + access_token,
#         agenda="forgot",
#     )
#     background_tasks.add_task(
#         mail.send,
#         "Assitant App reset password",
#         email_body.email,
#         content,
#     )
#     return {"message": "Password Reset Email sent successfully."}


# @router.get(
#     "/tenant/forgot-password/verify",
#     response_class=ORJSONResponse,
#     status_code=status.HTTP_200_OK,
# )
# async def reset_password_verify_token(token: str = Header()):
#     await verify_forgot_password_access_token(token)
#     # payload.scope = "login"
#     # res = await refresh_token_repo.deleteAll({"tenant_id": payload.id})
#     # logger.info(
#     #     f"[Reset Password] Deleted {res} refresh tokens for tenant_id : {payload.id}"
#     # )
#     # token_generated = create_access_token(payload)
#     # set_cookies(response, token_generated.access_token, token_generated.refresh_token)
#     return {"ok": True}


# @router.post(
#     "/tenant/forgot-password/set-password",
#     response_class=ORJSONResponse,
#     status_code=status.HTTP_200_OK,
# )
# async def reset_password_set_password(
#     set_password: SetPassword, response: Response, token: str = Header()
# ):

#     data = await verify_forgot_password_access_token(token)
#     res = await tenant_repo.findOneById(data.id)

#     if verify_hash(set_password.new_password, res["password"]):
#         raise http_exception.OLD_PASSWORD_SAME_EXCEPTION

#     new_password_hash = hash_password(set_password.new_password)
#     await tenant_repo.update_one(
#         {"_id": data.id}, {"$set": {"password": new_password_hash}}
#     )
#     count = await refresh_token_repo.deleteAll({"tenant_id": data.id})
#     logger.info(
#         f"[Updated Password] Deleted: {count}, refresh tokens for tenant_id: {data.id}"
#     )
#     token_generated = await create_access_token(
#         TokenData(id=data.id, type="tenant", scope="login")
#     )
#     set_cookies(response, token_generated.access_token, token_generated.refresh_token)
#     return {"ok": True}


@router.post(
    "/updatePassword", response_class=ORJSONResponse, status_code=status.HTTP_200_OK
)
async def update_password(
    response: Response,
    password_details: PasswordUpdate,
    current_user: TokenData = Depends(get_current_user),
):
    user_type = current_user.user_type

    user_data = await user_repo.findOne(
        {"_id": current_user.user_id}, {"_id": 1, "name": 1, "email": 1, "password": 1}
    )
    print(user_data)
    if not verify_hash(password_details.old_password, user_data["password"]):
        raise http_exception.ForbiddenException()

    if user_data["_id"] == current_user.user_id:
        new_password = hash_password(password_details.new_password)
        await user_repo.update_one(
            {"_id": current_user.user_id}, {"$set": {"password": new_password}}
        )
    count = await refresh_token_repo.deleteAll({"user_id": current_user.user_id})
    logger.info(f"[Updated Password] Deleted: {count}, refresh tokens for : {user_type}")

    token_data = TokenData(
        user_id=current_user.user_id, user_type=user_type, scope="login",username=current_user.username,
        profile_id = current_user.profile_id, email = current_user.email
    )
    token_generated = await create_access_token(token_data)
    set_cookies(response, token_generated.access_token, token_generated.refresh_token)

    return {"status": "Password Updated Successfully"}

