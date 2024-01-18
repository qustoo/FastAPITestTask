from dao.mongo_dao import MongoDAO


class MongoImagesDAO(MongoDAO):
    def __init__(self, collection, image_coll, fs_files, object_fs) -> None:
        super().__init__(collection, image_coll, fs_files, object_fs)

    async def create_user_with_image(self, user, image):
        new_obj = await self.object_collection.insert_one(
            {**user.model_dump(by_alias=True, exclude=["id"]), **image}
        )
        created_obj = await self.object_collection.find_one(
            {"_id": new_obj.inserted_id}
        )
        return created_obj

    async def upload_image(self, file_data: dict, data: bytes) -> dict:
        fs_chunks_files_id = await self._object_fs.upload_from_stream(
            file_data.filename, data
        )  # кладет в fs.chunks
        images_coll_id = await self._image_coll.insert_one(
            {"filename": file_data.filename, "fs_chunks_files_id": fs_chunks_files_id}
        )
        # Достаем из fs.files метаданные в словаре
        metadata_image = await self._fs_files.find_one({"_id": fs_chunks_files_id})
        return metadata_image

    async def get_information(self, file_id):
        return await self._image_coll.find_one({"_id": file_id})

    async def drop_all_values(self):
        await self._image_coll.delete_many({})
        await self._fs_files.delete_many({})
        await self.object_collection.delete_many({})
