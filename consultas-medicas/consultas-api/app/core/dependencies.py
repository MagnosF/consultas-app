from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import Optional, List, Union
from jose import jwt, JWTError
from typing import Optional, List
import os

from app.database.connection import get_db
from app.models.user import User, USER_TYPES # Importa o modelo e os tipos
from app.schemas.token_schema import TokenData

# Esquema de autenticação: Define onde o FastAPI deve procurar pelo token (Bearer scheme)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token") # tokenUrl aponta para a rota de login

# Variáveis do .env
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

def get_current_user(
    db: Session = Depends(get_db), 
    token: str = Depends(oauth2_scheme)
) -> User:
    """
    Decodifica o token JWT e retorna o objeto User correspondente.
    Usado como dependência para rotas protegidas.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # 1. Decodificar o token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # 2. Extrair o 'subject' (email)
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
            
        token_data = TokenData(email=email)
        
    except JWTError:
        # Lança exceção se o token for inválido ou expirado
        raise credentials_exception
        
    # 3. Buscar o usuário no banco de dados
    user = db.query(User).filter(User.email == token_data.email).first()
    
    if user is None:
        raise credentials_exception
        
    return user


def require_permission(allowed_roles: Union[str, List[str]]):
    """
    Função wrapper para criar dependências de autorização baseadas no tipo de usuário.
    allowed_roles pode ser uma string ('admin') ou uma lista (['medico', 'admin']).
    """
    if isinstance(allowed_roles, str):
        allowed_roles = [allowed_roles]

    def role_checker(current_user: User = Depends(get_current_user)):
        """
        Verifica se o user_type do usuário logado está na lista de allowed_roles.
        """
        if current_user.user_type not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Acesso negado. Apenas usuários com perfil {', '.join(allowed_roles)} podem acessar este recurso."
            )
        return current_user

    return role_checker