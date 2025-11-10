from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from typing import Any, Union, Optional
import os
from dotenv import load_dotenv
from jose import JWTError, jwt

# Carrega as variáveis de ambiente (necessário aqui para JWT)
load_dotenv()

# --- Configuração de Senha (Passlib) ---

# ⚠️ ALTERAÇÃO PRINCIPAL: MUDANÇA PARA ARGON2
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se a senha em texto plano corresponde ao hash."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Retorna o hash de uma senha em texto plano."""
    # ⚠️ REMOÇÃO DA LÓGICA DE TRUNCAMENTO (Argon2 não tem o limite de 72 bytes)
    return pwd_context.hash(password)

# --- Configuração de JWT (Python-JOSE) ---

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

def create_access_token(
    subject: Union[str, Any], expires_delta: Optional[timedelta] = None
) -> str:
    """Gera o token JWT."""
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        # Usa o tempo de expiração do .env
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Payload com o 'subject' (geralmente o ID ou e-mail do usuário) e a data de expiração
    to_encode = {"exp": expire, "sub": str(subject)}
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Nota: A decodificação (verificação do token) será feita pelo FastAPI com OAuth2PasswordBearer.