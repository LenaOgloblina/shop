from fastapi import APIRouter, status, HTTPException

from src.onlineshop.domains import Admin, Manager, Product, Cart, Order
from src.onlineshop.schemas import (
    LoginModel,
    GetProductsModel,
    AddProductModel,
    GetCartModel,
    AddProductToCartModel,
    RemoveProductFromCartModel,
    CreateOrderModel,
    GetOrderModel,
    ErrorModel,
)
from src.onlineshop import services
from src.onlineshop.repositories import ShelveProductRepository, MemoryProductsRepository, MemoryCartsRepository, \
    MemoryOrdersRepository, MemoryUsersRepository

router = APIRouter()


@router.get("/articles", response_model=GetProductsModel)
def get_articles() -> GetProductsModel:
    products = services.get_products(products_repository=ShelveProductRepository())
    return GetProductsModel(
        items=[
            GetProductsModel(id=product.id, name=product.name, description=product.description, price=product.price)
            for product in products
        ]
    )


@router.post(
    "/products",
    response_model=GetProductsModel,
    status_code=status.HTTP_201_CREATED,
    responses={201: {"model": GetProductsModel}, 401: {"model": ErrorModel}, 403: {"model": ErrorModel}},
)
def add_product(product: AddProductModel,
                credentials: LoginModel):
    current_user = services.login(
        username=credentials.username,
        password=credentials.password,
        users_repository=MemoryUsersRepository(),
    )

    # Это аутентификация
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized user"
        )
    # а это авторизация
    if not isinstance(current_user, Admin):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden resource"
        )

    product = services.add_product(
        description=product.description,
        name=product.name,
        price=product.price,
        products_repository=ShelveProductRepository(),
    )

    return GetProductsModel(id=product.id, description=product.description, name=product.name, price=product.price)


@router.get("/cart", response_model=GetCartModel)
def get_cart(cart_id: str) -> GetCartModel:
    cart = services.get_cart(carts_repository=MemoryCartsRepository(), cart_id=cart_id)
    return GetCartModel(id=cart.id, products=[
        Product(id=product.id, name=product.name, description=product.description, price=product.price) for product in
        cart.products])


@router.post("/cart", response_model=GetCartModel)
def add_product_to_cart(cart_id: str, product: AddProductToCartModel) -> GetCartModel:
    services.add_product_to_cart(carts_repository=MemoryCartsRepository(), cart_id=cart_id, product=product)
    cart = services.get_cart(carts_repository=MemoryCartsRepository(), cart_id=cart_id)
    return GetCartModel(id=cart.id, products=[
        Product(id=product.id, name=product.name, description=product.description, price=product.price) for product in
        cart.products])


@router.delete("/cart", response_model=GetCartModel)
def remove_product_from_cart(cart_id: str, product_id: str) -> GetCartModel:
    services.remove_product_from_cart(carts_repository=MemoryCartsRepository(), cart_id=cart_id, product_id=product_id)
    cart = services.get_cart(carts_repository=MemoryCartsRepository(), cart_id=cart_id)
    return GetCartModel(id=cart.id, products=[
        Product(id=product.id, name=product.name, description=product.description, price=product.price) for product in
        cart.products])


@router.post("/order", response_model=GetOrderModel, status_code=status.HTTP_201_CREATED)
def create_order(order: CreateOrderModel) -> GetOrderModel:
    order = services.create_order(orders_repository=MemoryOrdersRepository(), order=order)
    return GetOrderModel(id=order.id, email=order.email, products=[
        Product(id=product.id, name=product.name, description=product.description, price=product.price) for product in
        order.products])
