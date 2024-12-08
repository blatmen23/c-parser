from sqlalchemy.orm import mapped_column

from typing import Annotated

intpk = Annotated[int, mapped_column(primary_key=True)]

str_32 = Annotated[str, 32]
str_64 = Annotated[str, 64]
str_128 = Annotated[str, 128]
str_256 = Annotated[str, 256]
str_512 = Annotated[str, 512]