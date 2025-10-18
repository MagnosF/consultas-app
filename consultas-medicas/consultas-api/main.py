from fastapi import FastAPI
from app.database.connection import Base, engine
from app.models import user
from app.routes import user_routes

app = FastAPI(title="Consultas Médicas API")

Base.metadata.create_all(bind=engine)
app.include_router(user_routes.router)

@app.get("/")
def home():
    return {"message": "API Consultas Médicas está online 🚀"}
