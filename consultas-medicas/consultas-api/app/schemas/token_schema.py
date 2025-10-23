from typing import Optional
from pydantic import BaseModel

# Schema que o FastAPI usa para receber as credenciais do formulário de Login
class TokenData(BaseModel):
    email: Optional[str] = None

# Schema de Resposta: O que será enviado ao cliente após um Login bem-sucedido
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    # Opcional, mas útil para o frontend:
    user_type: str