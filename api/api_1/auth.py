from fastapi import APIRouter, Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordRequestForm
from typing import Any
from services.user_service import UserService
from core.security import create_access_token, create_refresh_token
from schemas.auth_schema import TokenSchema,TokenPayload
from schemas.user_schema import UserOut
from models.user_model import User
from .depends import get_current_user
from core.config import settings
from pydantic import ValidationError
from jose import jwt
from models.user_model import User
from uuid import UUID
import pymongo
from schemas.block_schema import BlockCreate
from models.blocktoken_model import Block
auth_router = APIRouter()

    # https://www.youtube.com/watch?v=e22635GdKlo
@auth_router.post('/login', summary="Create access and refresh tokens for user")

async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> Any:
    user = await UserService.authenticate(email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    # print(user.token)
    token=create_access_token(user.user_id)
    refresh_token= create_refresh_token(user.user_id)
    decoded_jwt = jwt.decode(token, settings.JWT_SECRET_KEY, settings.ALGORITHM)
    if user.token is None:
       
        update_token= await User.find_one(User.user_id==UUID(decoded_jwt['sub']))
        
        if not update_token:
            raise HTTPException(status_code=404, detail="Resource not found")

        update_token.token = token
        await update_token.save()
        # data_token= await User.find_one(User.user_id==UUID(decoded_jwt['sub']))
        return {
            "access_token": token,
            "refresh_token":refresh_token,
        }
    else:
        add=Block(token=user.token,user_id=decoded_jwt['sub'])
        await add.create()
       
        found_token= await User.find_one(User.user_id==UUID(decoded_jwt['sub']))
        if not found_token:
            raise HTTPException(status_code=404, detail="Resource not found")
        print(decoded_jwt['sub'],'ddddddd')
        found_token.token = token
        await found_token.save()
        all_token= await Block.find(Block.user_id==decoded_jwt['sub']).count()
        # print(all_token)
        if all_token>=5:
            delete_token=  await Block.find_one(Block.user_id==decoded_jwt['sub']).delete()
            # delete_token=  await Block.find_one(Block.user_id==decoded_jwt['sub']).sort(
            #     [(Block.created_at,pymongo.ASCENDING)]
            # ).limit(1).delete()
            
        return {
            "access_token": token,
            "refresh_token":refresh_token,
        }
        
    


@auth_router.post('/test-token', summary="Test if the access token is valid", response_model=UserOut)
async def test_token(user: User = Depends(get_current_user)):
    return user
# @auth_router.post('/login', summary="Create access and refresh tokens for user", response_model=TokenSchema)

# async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> Any:
#     user = await UserService.authenticate(email=form_data.username, password=form_data.password)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Incorrect email or password"
#         )
    
#     return {
#         "access_token": create_access_token(user.user_id),
#         "refresh_token": create_refresh_token(user.user_id),
#     }


# @auth_router.post('/test-token', summary="Test if the access token is valid", response_model=UserOut)
# async def test_token(user: User = Depends(get_current_user)):
#     return user


@auth_router.post('/refresh', summary="Refresh token", response_model=TokenSchema)
async def refresh_token(refresh_token: str = Body(...)):
    try:
        payload = jwt.decode(
            refresh_token, settings.JWT_REFRESH_SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = await UserService.get_user_by_id(token_data.sub)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid token for user",
        )
    return {
        "access_token": create_access_token(user.user_id),
        "refresh_token": create_refresh_token(user.user_id),
    }