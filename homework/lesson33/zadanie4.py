from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()


class Product(BaseModel):
    name: str
    price: float
    quantity: int


@app.post("/products")
async def create_product(product: Product):
    total_price = product.price * product.quantity

    return {
        "name": product.name,
        "price": product.price,
        "quantity": product.quantity,
        "total_price": total_price,
    }
