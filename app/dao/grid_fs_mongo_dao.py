from dao.mongo_dao import MongoDAO


class MongoImagesDAO(MongoDAO):
    def __init__(self, collection, image_coll, fs_files, object_fs) -> None:
        super().__init__(collection)
        self._image_coll = image_coll  # "Image"
        self._fs_files = fs_files  # fs.files
        self._object_fs = object_fs  # gridfs

    # CLEAR COLLECTION
    async def clear_database(self):
        await self._image_coll.delete_many({})
        await self._fs_files.delete_many({})
        await self.object_collection.delete_many({})

    # GRIDFS, UPLOAD/DOWNLOAD IMAGES

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

    async def get_file_information(self, id):
        return await self._fs_files.find_one({"_id": id})

    async def get_file_object(self, id):
        return await self._fs_files.find_one({"_id": id})

    # open_download_stream up to stream
    async def download_stream(self, file_id):
        grid_out = await self._object_fs.open_download_stream(file_id)
        contents = await grid_out.read()
        yield contents

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
