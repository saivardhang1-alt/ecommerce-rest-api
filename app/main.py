from fastapi import FastAPI

from app.routes import users, products, categories

app = FastAPI(
    title="E-Commerce REST API",
    description="A REST API for managing an online shopping platform",
    version="1.0.0"
)

app.include_router(users.router)
app.include_router(products.router)
app.include_router(categories.router)


@app.get("/")
def home():
    return {
        "message": "Welcome to E-Commerce REST API",
        "status": "Running successfully"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }
