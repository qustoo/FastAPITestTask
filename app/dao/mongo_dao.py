from dao.base_dao import NoSQLDAO


class MongoDAO(NoSQLDAO):
    def __init__(self, collection, image_coll, fs_files, object_fs) -> None:
        super().__init__(collection)
        self._image_coll = image_coll  # "Image"
        self._fs_files = fs_files  # fs.files
        self._object_fs = object_fs  # gridfs

    async def get_columns(self):
        return [key for key in await self.object_collection.find_one()]

    async def get_data(self):
        return [item async for item in self.object_collection.find()]
