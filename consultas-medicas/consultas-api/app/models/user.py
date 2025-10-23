from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.sql import func
from app.database.connection import Base # Importação da Base

# Definição dos tipos de usuário (perfis diferenciados - Requisito US 5)
USER_TYPES = ('paciente', 'medico', 'admin')

# Tabela de Usuários (Model ORM)
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), index=True) 
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(255)) # Senha criptografada (Requisito US 3)
    
    # Campo para perfis diferenciados
    user_type = Column(Enum(*USER_TYPES), default='paciente') 
    
    # Campos de controle/validação (para médico/admin)
    is_active = Column(Boolean, default=True) 
    is_verified = Column(Boolean, default=False)
    
    # Ex: CPF (para paciente) ou CRM (para médico)
    document = Column(String(50), unique=True, nullable=True) 
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', type='{self.user_type}')>"