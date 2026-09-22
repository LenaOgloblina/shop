from uuid import uuid4

from src.onlineshop.domains import Product, Cart, Order, User
from src.onlineshop.repositories import ProductsRepository, UsersRepository, CartsRepository, OrdersRepository


def get_products(products_repository: ProductsRepository) -> list[Product]:
    return products_repository.get_products()


def add_product(products_repository: ProductsRepository, product: Product):
    products_repository.add_product(product)


def get_cart(carts_repository: CartsRepository, cart_id: str) -> Cart:
    return carts_repository.get_cart(cart_id)


def add_product_to_cart(carts_repository: CartsRepository, cart_id: str, product: Product):
    carts_repository.add_product_to_cart(cart_id, product)


def remove_product_from_cart(carts_repository: CartsRepository, cart_id: str, product_id: str):
    carts_repository.remove_product_from_cart(cart_id, product_id)


def create_order(orders_repository: OrdersRepository, order: Order):
    orders_repository.create_order(order)


def login(
        username: str, password: str, users_repository: UsersRepository
) -> User | None:
    users = users_repository.get_users(username=username, password=password)
    if users:
        return users[0]
