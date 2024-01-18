from abc import ABC, abstractmethod


class NoSQLInterface(ABC):
    @abstractmethod
    async def create_user(self):
        pass

    @abstractmethod
    async def list_users(limit):
        pass

    @abstractmethod
    async def update_user(id, updated_user):
        pass

    @abstractmethod
    async def delete_user(id):
        pass

    @abstractmethod
    async def show_user_by_id(id):
        pass


class NoSQLDAO(NoSQLInterface):
    def __init__(self, collection) -> None:
        self.object_collection = collection

    # CRUD OPERATIONS

    async def create_user(self, user):
        new_user = await self.object_collection.insert_one(
            user.model_dump(by_alias=True, exclude=["id"])
        )
        created_user = await self.object_collection.find_one(
            {"_id": new_user.inserted_id}
        )
        return created_user

    async def list_users(self, limit):
        return await self.object_collection.find({}).to_list(limit)

    async def update_user(self, id, updated_user):
        return await self.object_collection.find_one_and_update(
            {"_id": id}, {"$set": updated_user}
        )

    async def delete_user(self, id):
        return await self.object_collection.delete_one({"_id": id})

    async def show_user_by_id(self, id):
        return await self.object_collection.find_one({"_id": id})
