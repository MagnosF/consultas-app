from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm # Para receber username/password
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.models.user import User
from app.core.security import verify_password, create_access_token
from app.schemas.token_schema import Token # O schema de resposta

router = APIRouter(
    tags=["Autenticação (Login)"]
)

@router.post(
    "/token", 
    response_model=Token,
    summary="Login de Usuário e Geração de Token JWT"
)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
):
    # 1. Buscar usuário pelo email (username no OAuth2PasswordRequestForm é o email)
    user = db.query(User).filter(User.email == form_data.username).first()
    
    # 2. Verificar se o usuário existe e se a senha está correta
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas. Verifique o email e a senha.",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    # 3. Gerar o Token JWT
    access_token = create_access_token(subject=user.email)
    
    # 4. Retornar o Token e o tipo de usuário (para o frontend saber qual dashboard carregar)
    return Token(
        access_token=access_token, 
        user_type=user.user_type
    )