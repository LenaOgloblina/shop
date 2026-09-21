import shelve
from abc import ABC, abstractmethod

from src.shop.domains import User, Admin, Manager

class UsersRepository(ABC):
    @abstractmethod
    def get_user(self, username: str | None = None, password: str | None = None) -> list[User]:
        pass

class MemoryUsersRepository(UsersRepository):
    def __init__(self):
        self.users = [
            Admin(
                id = '12134-5678-9123-4567',
                username = 'admin',
                password = 'Admin_1234!',
            )
        ]

    def get_user(self, username: str | None = None, password: str | None = None) -> list[User]:
        if username is None:
            return self.users.values()
        return
