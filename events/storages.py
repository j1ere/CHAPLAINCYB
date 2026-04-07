# events/storages.py
from cloudinary_storage.storage import RawMediaCloudinaryStorage

class PublicRawCloudinaryStorage(RawMediaCloudinaryStorage):
    options = {
        "upload_preset": "raw_public" 
    }