from dao.mongo_dao import MongoDAO


class MongoImagesDAO(MongoDAO):
    def __init__(self, collection, image_coll, fs_files, object_fs) -> None:
        super().__init__(collection)
        self._image_coll = image_coll  # "Image"
        self._fs_files = fs_files  # fs.files
        self._object_fs = object_fs  # gridfs

    # CLEAR COLLECTION WITH IMAGES
    async def clear_database(self):
        await self._image_coll.delete_many({})
        await self._fs_files.delete_many({})
        await self.object_collection.delete_many({})

    # GRIDFS, UPLOAD/DOWNLOAD IMAGES

    async def upload_image(self, file_data: dict, data: bytes) -> dict:
        fs_chunks_files_id = await self._object_fs.upload_from_stream(
            file_data.filename, data
        )  # кладет в fs.chunks
        await self._image_coll.insert_one(
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
