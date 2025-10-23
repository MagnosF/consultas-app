from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from datetime import datetime, timezone

from app.database.connection import SessionLocal
from app.models.user import User
from app.core.config import settings

# ---------------------- DEPENDÊNCIAS BÁSICAS ----------------------

# 1. Dependência para obter a sessão do banco de dados (get_db)
def get_db():
    """Retorna uma sessão de banco de dados para a rota e a fecha após o uso."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 2. Esquema de autenticação OAuth2 (Header: Authorization: Bearer <token>)
# tokenUrl="users/login" aponta para a rota que gera o token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

# ---------------------- FUNÇÕES DE AUTORIZAÇÃO ----------------------

def decode_access_token(token: str):
    """Decodifica o token de acesso e retorna o payload."""
    try:
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado.",
            headers={"WWW-Authenticate": "Bearer"},
        )

# 3. Dependência para obter o usuário logado
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Decodifica o token e retorna o objeto User correspondente."""
    payload = decode_access_token(token)
    
    user_email = payload.get("sub")
    
    if user_email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Verifica se o token tem a informação 'role' (adicionada na rota de login)
    user_role = payload.get("role")
    user_id = payload.get("id")

    # 4. Busca o usuário no DB
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado.",
        )
    
    # Validação extra: verifica se o médico está ativo e aprovado
    if user.role == 'doctor' and not user.is_approved:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Conta de médico pendente de aprovação do administrador.",
        )

    return user

# 5. Dependência para obter o administrador logado (apenas para rotas administrativas)
def get_current_admin(current_user: User = Depends(get_current_user)):
    """Verifica se o usuário atual é um administrador."""
    if current_user.role != 'admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado. Requer permissão de administrador.",
        )
    return current_user
