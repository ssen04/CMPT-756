from fastapi import FastAPI
from routes import router

app = FastAPI(title="Catalog Microservice")

app.include_router(router)

@app.get("/")
def root():
    return {"service": "catalog-service"}