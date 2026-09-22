from dataclasses import dataclass


@dataclass
class User:
    """Обычный пользователь"""
    id: str


@dataclass
class Admin(User):
    """Пользователь, наделенный правами администратора"""
    username: str
    password: str


@dataclass
class Manager(User):
    """Пользователь, наделенный правами менеджера"""
    username: str
    password: str


@dataclass
class Product:
    """Сущность товар"""
    id: str
    description: str
    name: str
    price: str


@dataclass
class Cart:
    """Сущность корзина"""
    id: str
    products: list[Product]


@dataclass
class Order:
    id: str
    email: str
    products: list[Product]
