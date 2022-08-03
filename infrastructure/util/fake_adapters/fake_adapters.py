from uuid import UUID

from domain.config.config_port import ConfigPort
from domain.config.model.JWTConfig import JWTConfig
from domain.config.model.UserConfig import UserConfig
from domain.jwt.jwt_port import JWTPort
from domain.jwt.model.JWTDecodeCmd import JWTDecodeCmd
from domain.jwt.model.JWTPayload import JWTPayload
from domain.jwt.model.JWTSignCmd import JWTSignCmd
from domain.user.model.ChangePasswordCmd import ChangePasswordCmd
from domain.user.model.User import User
from domain.user.model.UserCreateCmd import UserCreateCmd
from domain.user.model.UserDeleteCmd import UserDeleteCmd
from domain.user.user_modify_port import UserModifyPort
from domain.user.user_query_port import UserQueryPort


# These are fake adapters only for tests' purposes.

class FakeUserModifyAdapter(UserModifyPort):
    def create_user(self, cmd: UserCreateCmd) -> UUID:
        pass

    def delete_user(self, cmd: UserDeleteCmd) -> None:
        pass

    def change_password(self, cmd: ChangePasswordCmd) -> None:
        pass


class FakeUserQueryAdapter(UserQueryPort):
    def find_user_by_id(self, _id: UUID) -> User:
        pass

    def find_user_by_username(self, username: str) -> User:
        pass


class FakeConfigAdapter(ConfigPort):
    def read_user_config(self) -> UserConfig:
        pass

    def read_jwt_config(self) -> JWTConfig:
        pass


class FakeJWTAdapter(JWTPort):
    def sign(self, cmd: JWTSignCmd) -> str:
        pass

    def decode(self, cmd: JWTDecodeCmd) -> JWTPayload:
        pass
