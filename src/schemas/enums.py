from enum import Enum, unique


class Platforms(Enum):
    JOYREACTOR = "Joyreactor"
    NINE_GAG = "9GAG"
    VK = "VK"
    INSTAGRAM = "Instagram"
    PIKABU = "Pikabu"

class Categories(Enum):
    VEHICLES = "Авто & Мото"
    CULTURE_ENTERTAINMENT = "Культура & Развлечения"  # Аниме, Музыка, Фильмы & Сериалы, Юмор
    BUSINESS_FINANCE = "Бизнес & Финансы"
    CREATORS_MEDIA = "Создатели & Медиа"  # Блогеры, Подкасты, Новости & СМИ
    TECHNOLOGY = "Технологии"  # Программирование, Наука, Мобильные приложения
    LIFESTYLE = "Лайфстайл"  # Здоровье, Кулинария, Мода, Путешествия
    EDUCATION_KNOWLEDGE = "Образование & Познавательное"
    POLITICS_LAW = "Политика & Право"
    NATURE_ECOLOGY = "Природа & Экология"
    SPORTS = "Спорт"
    RELIGION_SPIRITUALITY = "Религия & Духовность"
    PARENTING = "Родителям"
    ART_DESIGN = "Искусство & Дизайн"
    GAMING = "Игры"
    ADULT = "Для взрослых & 18+"
    OTHER = "Другое"

class MediaTypes(Enum):
    IMAGE = "image"
    VIDEO = "video"

class FileTypes(Enum):
    # photo
    JPG = "jpg"
    JPEG = "jpeg"
    PNG = "png"

    # video
    MP4 = "mp4"
    WEBM = "webm"

    OTHER = "other"