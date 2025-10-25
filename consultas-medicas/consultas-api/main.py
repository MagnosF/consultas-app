from fastapi import FastAPI
from app.database.connection import engine, Base
from app.models import user
from app.models import appointment_model 
from app.routes import user_routes 
from app.routes import auth_routes 
from app.routes import appointment_routes 

# Função para criar a tabela 'users' e 'appointments'
#def create_db_tables():
    # Isso cria TODAS as tabelas que herdam de Base, incluindo a nova 'appointments'
    #Base.metadata.create_all(bind=engine)

#create_db_tables() 

app = FastAPI(title="Consultas Médicas API")

# --- Inclui os roteadores ---
app.include_router(auth_routes.router)
app.include_router(user_routes.router)
app.include_router(appointment_routes.router) # <-- Inclui as rotas de agendamento

@app.get("/")
def read_root():
    return {"message": "API de Consultas Médicas está no ar!"}