from uuid import uuid4

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

_base_ = declarative_base()


class UserEntity(_base_):
    __tablename__ = "user"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4())
    username = Column(String(16), unique=True, nullable=False)
    password = Column(String(150), nullable=False)

    def create(self, engine):
        _base_.metadata.create_all(engine)
