from enum import Enum, unique


class Platforms(Enum):
    NINE_GAG = "9GAG"
    VK = "VK"
    INSTAGRAM = "Instagram"

class Categories(Enum):
    FUN = "funny"
    CRIME = "crime"
    REAL = "real"

class MediaTypes(Enum):
    PHOTO = "photo"
    VIDEO = "video"

class FileTypes(Enum):
    # photo
    JPEG = "jpeg"
    PNG = "png"
    TIFF = "tiff"

    # video
    MP4 = "mp4"



