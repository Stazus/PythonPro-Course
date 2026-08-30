from pydantic import BaseModel, ConfigDict


class AuthorCreate(BaseModel):
    name: str


class AuthorResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class BookCreate(BaseModel):
    title: str
    price: float
    author_id: int


class BookResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    price: float
    author_id: int
