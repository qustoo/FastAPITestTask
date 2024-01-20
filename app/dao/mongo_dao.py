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
    
     # INC/DEC VOTE VALUE

    async def check_vote_value(self, id):
        vote_valud_dict: dict[str, str] = await self.object_collection.find_one(
            {"_id": id}, {"vote_value": 1}
        )
        return vote_valud_dict.get("vote_value", 0)

    async def vote_value(self, id, value):
        vote_counter = await self.check_vote_value(id)
        if (vote_counter <= 0 and value < 0) or (vote_counter >= 10 and value > 0):
            return False
        await self.object_collection.find_one_and_update(
            {"_id": id}, {"$inc": {"vote_value": value}}
        )
        return True
    
    
    # CLEAR COLLECTION
    async def clear_database(self):
        await self._image_coll.delete_many({})
        await self._fs_files.delete_many({})
        await self.object_collection.delete_many({})
