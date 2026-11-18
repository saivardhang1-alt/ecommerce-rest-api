from fastapi import FastAPI

app = FastAPI(
    title="E-Commerce REST API",
    description="A REST API for managing an online shopping platform",
    version="1.0.0"
)

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
