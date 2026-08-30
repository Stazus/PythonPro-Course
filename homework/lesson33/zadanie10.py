from fastapi import Depends, FastAPI, Header, HTTPException


app = FastAPI()

API_KEY = "secret123"


async def verify_api_key(x_api_key: str = Header()):
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid API key",
        )

    return x_api_key


@app.get("/books")
async def get_books(api_key: str = Depends(verify_api_key)):
    return {"message": "Books endpoint"}


@app.get("/authors")
async def get_authors(api_key: str = Depends(verify_api_key)):
    return {"message": "Authors endpoint"}


@app.get("/users")
async def get_users(api_key: str = Depends(verify_api_key)):
    return {"message": "Users endpoint"}
