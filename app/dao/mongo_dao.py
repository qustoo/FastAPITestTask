from dao.base_dao import NoSQLDAO


class MongoDAO(NoSQLDAO):
    def __init__(self, collection):
        super().__init__(collection)

    async def create_user_with_image(self, user, image):
        new_obj = await self.object_collection.insert_one(
            {**user.model_dump(by_alias=True, exclude=["id"]), **image}
        )
        created_obj = await self.object_collection.find_one(
            {"_id": new_obj.inserted_id}
        )
        return created_obj

    async def get_columns(self):
        return [key for key in await self.object_collection.find_one()]

    async def get_data(self):
        return [item async for item in self.object_collection.find()]

    async def sort_users(self, sorted_info: dict[tuple[str, int]]):
        return [
            user async for user in self.object_collection.find({}).sort(sorted_info)
        ]

    async def filter_users(self, name, surname):
        return [
            user
            async for user in self.object_collection.find(
                {
                    "$and": [
                        {"name": {"$regex": name, "$options": "i"}},
                        {"surname": {"$regex": surname, "$options": "i"}},
                    ]
                }
            )
        ]
