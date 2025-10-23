from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database.connection import get_db
from app.schemas.user import UserCreate, UserResponse
from app.models.user import User
from app.core.security import get_password_hash # Importa a função de hashing
from app.core.dependencies import require_permission

router = APIRouter(
    prefix="/users",
    tags=["Usuários (Cadastro e Gestão)"]
)

# Endpoint: POST /users/ - Cadastro de Usuário
@router.post(
    "/", 
    response_model=UserResponse, 
    status_code=status.HTTP_201_CREATED,
    summary="Cadastra um novo usuário (Paciente, Médico ou Admin)"
)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # 1. Verificar se o e-mail já está cadastrado
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O e-mail já está em uso."
        )

    # 2. Criptografar a senha
    hashed_password = get_password_hash(user.password)

    # 3. Criar a instância do modelo ORM com o hash da senha
    new_user = User(
        full_name=user.full_name,
        email=user.email,
        hashed_password=hashed_password,  # Armazena o hash, não a senha limpa!
        user_type=user.user_type,
        document=user.document
    )

    # 4. Salvar no banco de dados
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # 5. Retornar a resposta (sem a senha)
    return new_user

# Novo Endpoint Protegido: Apenas para Administradores
@router.get(
    "/",
    response_model=List[UserResponse], # Vamos precisar do List
    # Usa a dependência: o usuário deve ter o user_type == 'admin'
    dependencies=[Depends(require_permission('admin'))], 
    summary="Lista todos os usuários (Apenas para Admin)"
)
def list_users(db: Session = Depends(get_db)):
    """Retorna uma lista de todos os usuários cadastrados (Requer Admin)."""
    users = db.query(User).all()
    return users