from enum import Enum, unique


class Platforms(Enum):
    NINE_GAG = "9GAG"
    VK = "VK"
    INSTAGRAM = "Instagram"
    PIKABU = "Пикабу"

class Categories(Enum):
    NOT_SET = "not set"
    FUN = "funny"
    CRIME = "crime"
    REAL = "real"
    OTHER = "other"

class MediaTypes(Enum):
    IMAGE = "image"
    VIDEO = "video"

class FileTypes(Enum):
    # photo
    JPG = "jpg"
    PNG = "png"

    # video
    MP4 = "mp4"
    WEBM = "webm"

    OTHER = ".other"

