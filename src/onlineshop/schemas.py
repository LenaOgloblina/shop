from pydantic import BaseModel


class GetProductModel(BaseModel):
    id: str
    description: str
    name: str
    price: str


class GetProductsModel(BaseModel):
    items: list[GetProductModel]


class CreateArticleModel(BaseModel):
    title: str
    content: str


class AddProductModel(BaseModel):
    name: str
    description: str
    price: float


class GetCartModel(BaseModel):
    id: str
    products: list[GetProductModel]


class AddProductToCartModel(BaseModel):
    id: str


class RemoveProductFromCartModel(BaseModel):
    id: str


class CreateOrderModel(BaseModel):
    email: str
    products: list[GetProductModel]


class GetOrderModel(BaseModel):
    id: str
    email: str
    products: list[GetProductModel]


class LoginModel(BaseModel):
    username: str
    password: str


class ErrorModel(BaseModel):
    detail: str
