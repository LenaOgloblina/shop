import shelve
from abc import ABC, abstractmethod
from uuid import uuid4

from src.onlineshop.domains import User, Admin, Product, Cart, Order


class UsersRepository(ABC):
    @abstractmethod
    def get_user(self, username: str | None = None, password: str | None = None) -> list[User]:
        pass


class MemoryUsersRepository(UsersRepository):
    def __init__(self):
        self.users = [
            Admin(
                id='12134-5678-9123-4567',
                username='admin',
                password='Admin_1234!',
            )
        ]

    def get_user(self, username: str | None = None, password: str | None = None) -> list[User]:
        filtered_users = []
        for user in self.users:
            if username is not None and user.username != username:
                continue
            if password is not None and user.password != password:
                continue
            filtered_users.append(user)
        return filtered_users


class ProductsRepository(ABC):
    @abstractmethod
    def get_products(self) -> list[Product]:
        pass

    @abstractmethod
    def add_product_to_cart(self, product: Product):
        pass


class MemoryProductsRepository(ProductsRepository):
    def __init__(self):
        self.products = [
            Product(id=str(uuid4()), name="Product 1", description="Description 1", price=10.99),
            Product(id=str(uuid4()), name="Product 2", description="Description 2", price=9.99),
        ]

    def get_products(self) -> list[Product]:
        return self.products

    def add_product(self, product: Product):
        self.products.append(product)


class CartsRepository(ABC):
    @abstractmethod
    def get_cart(self, cart_id: str) -> Cart:
        pass

    @abstractmethod
    def add_product_to_cart(self, cart_id: str, product: Product):
        pass

    @abstractmethod
    def remove_product_from_cart(self, cart_id: str, product_id: str):
        pass


class MemoryCartsRepository(CartsRepository):
    def __init__(self):
        self.carts = {}

    def get_cart(self, cart_id: str) -> Cart:
        return self.carts.get(cart_id)

    def add_product_to_cart(self, cart_id: str, product: Product):
        if cart_id not in self.carts:
            self.carts[cart_id] = Cart(id=cart_id, products=[])
        self.carts[cart_id].products.append(product)

    def remove_product_from_cart(self, cart_id: str, product_id: str):
        if cart_id in self.carts:
            self.carts[cart_id].products = [product for product in self.carts[cart_id].products if
                                            product.id != product_id]


class OrdersRepository(ABC):
    @abstractmethod
    def get_order(self, order_id: str) -> Order:
        pass

    @abstractmethod
    def create_order(self, order: Order):
        pass


class MemoryOrdersRepository(OrdersRepository):
    def __init__(self):
        self.orders = {}

    def get_order(self, order_id: str) -> Order:
        return self.orders.get(order_id)

    def create_order(self, order: Order):
        self.orders[order.id] = order


class ShelveProductRepository(ProductsRepository):
    def __init__(self):
        self.db_name = 'products'

    def get_products(self) -> list[Product]:
        with shelve.open(self.db_name) as db:
            return list(db.values())
