from pydantic import BaseModel, EmailStr, Field
from typing import Optional

# Definição dos tipos de usuário (igual ao modelo)
USER_TYPES = ('paciente', 'medico', 'admin')

# --- Schema de ENTRADA (Input) ---
# Usado para validar os dados recebidos no POST /users/
class UserCreate(BaseModel):
    full_name: str = Field(..., min_length=3, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6)
    user_type: Optional[str] = Field('paciente', description="Pode ser 'paciente', 'medico', ou 'admin'")
    document: Optional[str] = None # CPF ou CRM

# --- Schema de SAÍDA (Output) ---
# Usado para formatar a resposta enviada ao cliente após o cadastro
class UserResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    user_type: str
    document: Optional[str] = None
    is_active: bool
    is_verified: bool

    class Config:
        # Permite que o Pydantic leia dados de objetos ORM (como o objeto User do SQLAlchemy)
        from_attributes = True