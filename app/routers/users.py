import asyncio
from typing import Optional

from bson import ObjectId
from fastapi import APIRouter, Body, Depends, File, UploadFile, status
from fastapi.responses import JSONResponse
from fastapi_cache.decorator import cache

from app.dao.grid_fs_mongo_dao import MongoImagesDAO
from app.database import get_mongo_database
from app.dependecies import validate_id
from app.exceptions import IncorrectVoteValueException, UserNotFoundException
from app.schemas import (
    SortUserModel,
    SortValues,
    UserCollection,
    UserModel,
    UserOutputModel,
    UserPartialUpdateModel,
    UserUpdateModel,
    UserWithImage,
)

router = APIRouter(prefix="/users", tags=["Users"])
LOCK = asyncio.Lock()


@router.get("/clear", response_description="Clear all data in collections")
async def clear_database(database: MongoImagesDAO = Depends(get_mongo_database)):
    await database.clear_database()


@router.get(
    "/filter",
    response_model=UserCollection,
    response_description="Filter users by name/surname",
)
@cache(expire=3600)
async def filter_users(
    name: Optional[str] = "",
    surname: Optional[str] = "",
    database: MongoImagesDAO = Depends(get_mongo_database),
):
    return UserCollection(users=await database.filter_users(name, surname))


@router.post(
    "/",
    response_description="Create new User",
    response_model=UserWithImage,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_user_with_image(
    database: MongoImagesDAO = Depends(get_mongo_database),
    user: UserModel = Body(...),
    file: UploadFile = File(...),
):
    uploaded_image = await database.upload_image(file, await file.read())
    user_with_image = await database.create_user_with_image(
        user, {"image": uploaded_image}
    )
    return user_with_image


@router.get(
    "/",
    response_description="Get all users",
    response_model=UserCollection,
    response_model_by_alias=False,
)
@cache(expire=3600)
async def get_users(
    database: MongoImagesDAO = Depends(get_mongo_database), limit: int = 100
):
    return UserCollection(users=await database.list_users(limit))


@router.get(
    "/{user_id}",
    response_description="Get user by id",
    response_model=UserOutputModel,
    response_model_by_alias=False,
)
async def show_user(
    database: MongoImagesDAO = Depends(get_mongo_database),
    user_id: ObjectId = Depends(validate_id),
):
    if user := await database.show_user_by_id(user_id):
        return user
    raise UserNotFoundException()


@router.put(
    "/{user_id}",
    response_description="Update user",
    response_model=UserOutputModel,
    response_model_by_alias=False,
)
async def update_user(
    user: UserUpdateModel,
    user_id: ObjectId = Depends(validate_id),
    database: MongoImagesDAO = Depends(get_mongo_database),
):
    new_user_data = {k: v for k, v in user.model_dump(exclude_none=False).items()}
    if update_user := await database.update_user(user_id, new_user_data):
        return update_user
    raise UserNotFoundException()


@router.patch(
    "/{user_id}",
    response_description="Partial update user",
    response_model=UserOutputModel,
    response_model_by_alias=False,
)
async def partial_update_user(
    partial_user: UserPartialUpdateModel,
    user_id: ObjectId = Depends(validate_id),
    database: MongoImagesDAO = Depends(get_mongo_database),
):
    new_user_data = {
        k: v for k, v in partial_user.model_dump(exclude_none=True).items()
    }
    if update_user := await database.update_user(user_id, new_user_data):
        return update_user
    raise UserNotFoundException


@router.delete("/{user_id}", response_description="Delete user")
async def delete_user(
    database: MongoImagesDAO = Depends(get_mongo_database),
    user_id: ObjectId = Depends(validate_id),
):
    if delete_user := await database.delete_user(user_id):
        return JSONResponse(content=f"User with id '{delete_user.inserted_id}' deleted")
    raise UserNotFoundException()


# Инкремент  счетчика
@router.post(
    "/inc_vote/{user_id}",
    response_model=UserOutputModel,
    response_description="Increment user vote value ",
)
async def inc_vote_value(
    database: MongoImagesDAO = Depends(get_mongo_database),
    user_id: ObjectId = Depends(validate_id),
):
    return await vote_value(user_id, database, 1)


# Декремент счетчика
@router.post(
    "/dec_vote/{user_id}",
    response_model=UserOutputModel,
    response_description="Decrement user vote value ",
)
async def dec_vote_value(
    database: MongoImagesDAO = Depends(get_mongo_database),
    user_id: ObjectId = Depends(validate_id),
):
    return await vote_value(user_id, database, -1)


async def vote_value(user_id: str, database: MongoImagesDAO, value: int):
    async with LOCK:
        if not await database.vote_value(user_id, value):
            raise IncorrectVoteValueException()
        user = await database.show_user_by_id(user_id)
    return user


@router.post(
    "/sort",
    response_model=UserCollection,
    response_description="Sort users by ASC/DESC parameters",
)
@cache(expire=3600)
async def sort_users(
    sorted_info: SortUserModel,
    database: MongoImagesDAO = Depends(get_mongo_database),
):
    sorted_info = {
        k: 1 if v is SortValues.ASC else -1 for k, v in sorted_info.model_dump().items()
    }
    result = await database.sort_users(sorted_info)
    return UserCollection(users=result)
