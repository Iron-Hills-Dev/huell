from sqlalchemy import Column, String
from sqlalchemy.orm import declarative_base

_base_ = declarative_base()


class VersionEntity(_base_):
    __tablename__ = "version"
    version = Column(String, primary_key=True)

    def create(self, engine):
        _base_.metadata.create_all(engine)

    def to_dict(self):
        return self.__dict__
