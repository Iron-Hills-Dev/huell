import logging
from uuid import UUID

from sqlalchemy.orm import Session

from domain.user.exceptions import UserNotFound
from domain.user.model.User import User
from infrastructure.postgres.model.UserEntity import UserEntity


def user_to_entity(_user: User) -> UserEntity:
    _entity = UserEntity(id=_user.id, username=_user.username, password=_user.password)
    return _entity


def entity_to_user(_entity: UserEntity) -> User:
    _user = User(_entity.id, _entity.username, _entity.password)
    return _user


def get_user_entity(_session: Session, _id: UUID) -> UserEntity:
    _user_entity = _session \
        .query(UserEntity) \
        .get(_id)
    if _user_entity is None:
        logging.error(f"Given ID does not match any user in database: id={_id}")
        raise UserNotFound(f"User with ID {_id} does not exist")
    return _user_entity
