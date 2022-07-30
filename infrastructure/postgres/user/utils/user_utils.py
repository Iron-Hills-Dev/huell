import logging
from uuid import UUID

from sqlalchemy.orm import Session

from domain.user.exceptions import UserNotFound
from domain.user.model.User import User
from infrastructure.postgres.model.UserEntity import UserEntity


def user_to_entity(user: User) -> UserEntity:
    _entity = UserEntity(id=user.id, username=user.username, password=user.password)
    return _entity


def entity_to_user(entity: UserEntity) -> User:
    _user = User(entity.id, entity.username, entity.password)
    return _user


def get_user_entity(session: Session, _id: UUID) -> UserEntity:
    _user_entity = session \
        .query(UserEntity) \
        .get(_id)
    if _user_entity is None:
        logging.error(f"Given ID does not match any user in database: id={_id}")
        raise UserNotFound(f"User with ID {_id} does not exist")
    return _user_entity
