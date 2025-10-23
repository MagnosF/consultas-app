from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente (do seu .env)
load_dotenv()

# --- Configuração do Banco de Dados ---
# Usa o driver 'mysqlclient'
DB_URL = (
    f"mysql+pymysql://{os.getenv('DB_USER')}:"  # Garante o PyMySQL
    f"{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}/"
    f"{os.getenv('DB_NAME')}"
    # Opcional: Adicione o charset para compatibilidade, o que pode ajudar
    "?charset=utf8mb4" 
)
# Cria o engine (motor) de conexão com o MySQL
# O 'echo=False' é ideal para produção, mas pode ser 'True' para ver o SQL gerado
engine = create_engine(DB_URL, echo=False)

# Cria a classe de sessão para interagir com o banco
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para os modelos (classes que representam as tabelas)
Base = declarative_base()

# Função de dependência para obter a sessão do banco
def get_db():
    """Fornece uma sessão do banco de dados e garante que ela seja fechada após o uso."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()