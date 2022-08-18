from sqlalchemy import Column, String

from infrastructure.postgres.model.dec_base import _base_


class VersionEntity(_base_):
    __tablename__ = "Version"
    version = Column(String, primary_key=True)
