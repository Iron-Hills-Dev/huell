import logging

from domain.user.model.User import User
from infrastructure.postgres.model.user_entity import UserEntity


def user_to_entity(_user: User) -> UserEntity:
    logging.debug("Changing User object to UserEntity")
    _entity = UserEntity(_user.id, _user.username, _user.password)
    return _entity


def entity_to_user(_entity: UserEntity) -> User:
    logging.debug("Changing UserEntity object to User")
    _user = User(_entity.id, _entity.username, _entity.password)
    return _user
