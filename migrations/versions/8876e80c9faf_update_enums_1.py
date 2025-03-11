"""update enums 1

Revision ID: 8876e80c9faf
Revises: 978c79c3a401
Create Date: 2025-03-06 09:26:34.857545

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '8876e80c9faf'
down_revision: Union[str, None] = '978c79c3a401'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.alter_column('media_contents', 'media_type',
                    existing_type=mysql.ENUM('IMAGE', 'VIDEO'),
                    type_=sa.Enum('image', 'video', name='mediatypes'),
                    existing_nullable=False)
    # далее name специально не передаю
    op.alter_column('media_contents', 'file_type',
                    existing_type=mysql.ENUM('JPEG', 'PNG', 'TIFF', 'MP4'),
                    type_=sa.Enum('jpg', 'jpeg', 'png', 'mp4', 'webm', 'other', name='mediatypes'),
                    existing_nullable=False)

    op.alter_column('posts', 'category',
                    existing_type=mysql.ENUM('FUN', 'CRIME', 'REAL'),
                    type_=sa.Enum('Авто & Мото', 'Культура & Развлечения', 'Бизнес & Финансы', 'Создатели & Медиа', 'Технологии', 'Лайфстайл', 'Образование & Познавательное', 'Политика & Право', 'Природа & Экология', 'Спорт', 'Религия & Духовность', 'Родителям', 'Искусство & Дизайн', 'Игры', 'Для взрослых & 18+', 'Другое', name='mediatypes'),
                    existing_nullable=False)

    op.alter_column('sources', 'platform',
                    existing_type=mysql.ENUM('NINE_GAG', 'VK', 'INSTAGRAM'),
                    type_=sa.Enum('Joyreactor', '9GAG', 'VK', 'Instagram', 'Pikabu'),
                    existing_nullable=False)


def downgrade():
    op.alter_column('media_contents', 'media_type',
                    existing_type=sa.Enum('image', 'video', name='mediatypes'),
                    type_=mysql.ENUM('IMAGE', 'VIDEO'),
                    existing_nullable=False)
    # далее name специально не передаю
    op.alter_column('media_contents', 'file_type',
                    existing_type=mysql.ENUM('jpg', 'jpeg', 'png', 'mp4', 'webm', 'other'),
                    type_=sa.Enum('JPEG', 'PNG', 'TIFF', 'MP4', name='mediatypes'),
                    existing_nullable=False)

    op.alter_column('media_contents', 'category',
                    existing_type=mysql.ENUM('Авто & Мото', 'Культура & Развлечения', 'Бизнес & Финансы', 'Создатели & Медиа', 'Технологии', 'Лайфстайл', 'Образование & Познавательное', 'Политика & Право', 'Природа & Экология', 'Спорт', 'Религия & Духовность', 'Родителям', 'Искусство & Дизайн', 'Игры', 'Для взрослых & 18+', 'Другое'),
                    type_=sa.Enum('FUN', 'CRIME', 'REAL', name='mediatypes'),
                    existing_nullable=False)

    op.alter_column('sources', 'platform',
                    existing_type=mysql.ENUM('Joyreactor', '9GAG', 'VK', 'Instagram', 'Pikabu'),
                    type_=sa.Enum('NINE_GAG', 'VK', 'INSTAGRAM'),
                    existing_nullable=False)
