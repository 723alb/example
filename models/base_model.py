from sqlalchemy import BigInteger
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class BaseModel(DeclarativeBase):
	id: Mapped[int] = mapped_column(BigInteger, primary_key=True)

	def to_dict(self, included_fields: list[str] = None, excluded_fields: list[str] = None) -> dict:
		result = {column.name: getattr(self, column.name) for column in self.__table__.columns}
		if included_fields:
			result = {k: v for k, v in result.items() if k in included_fields}
		if excluded_fields:
			result = {k: v for k, v in result.items() if k not in excluded_fields}
		return result