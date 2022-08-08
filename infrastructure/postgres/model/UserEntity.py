from uuid import uuid4

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID

from infrastructure.postgres.model.dec_base import _base_


class UserEntity(_base_):
    __tablename__ = "User"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4())
    username = Column(String(), unique=True, nullable=False)
    password = Column(String(), nullable=False)
