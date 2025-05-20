from sqlalchemy import JSON, BigInteger, UUID
from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column

from map_parser.models import BaseModel


class MapsInfo(BaseModel):
    __tablename__ = 'maps_info'

    filename: Mapped[str] = mapped_column(nullable=False)
    data =  mapped_column(type_=JSON, nullable=False)
    description = mapped_column(type_=JSON, nullable=True)
    session_uuid: Mapped[str] = mapped_column(type_=UUID, nullable=False)
    uncertainty_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
