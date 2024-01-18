from fastapi import APIRouter, Body, Depends, File, Path, UploadFile, status
from fastapi.responses import JSONResponse
from schemas import UserModel, UserCollection, UserUpdateModel, UserWithImage
from dao.grid_fs_mongo_dao import MongoImagesDAO
from database import collection, image_collection, fs, image_information_collect

from exceptions import UserNotFoundException, ValidateBsonID

router = APIRouter(prefix="/users")


async def get_mongo_database():
    return MongoImagesDAO(collection, image_collection, image_information_collect, fs)


@router.get("/delete")
async def delete_all(database: MongoImagesDAO = Depends(get_mongo_database)):
    await database.drop_all_values()


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
async def get_users(
    database: MongoImagesDAO = Depends(get_mongo_database), limit: int = 100
):
    return UserCollection(users=await database.list_users(limit))


@router.get(
    "/{user_id}",
    response_description="Get user by id",
    response_model=UserModel,
    response_model_by_alias=False,
)
async def show_user(
    database: MongoImagesDAO = Depends(get_mongo_database), user_id: str = Path(...)
):
    user_id = ValidateBsonID(user_id)
    user = await database.show_user_by_id(user_id)
    if user:
        return user
    raise UserNotFoundException()


@router.put(
    "/{user_id}",
    response_description="Update user",
    response_model=UserModel,
    response_model_by_alias=False,
)
async def update_user(
    user: UserUpdateModel,
    user_id: str = Path(...),
    database: MongoImagesDAO = Depends(get_mongo_database),
):
    user_id = ValidateBsonID(user_id)

    new_user = {k: v for k, v in user.model_dump().items() if k is not None}
    update_user = await database.update_user(user_id, new_user)
    if update_user:
        return update_user
    raise UserNotFoundException()


@router.delete("/{user_id}", response_description="Delete user")
async def delete_user(
    database: MongoImagesDAO = Depends(get_mongo_database), user_id: str = Path(...)
):
    user_id = ValidateBsonID(user_id)
    delete_user = await database.delete_user(user_id)
    if delete_user:
        return JSONResponse(content=f"User with id {user_id} deleted")
    raise UserNotFoundException()
