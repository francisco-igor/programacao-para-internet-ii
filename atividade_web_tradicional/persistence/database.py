from dotenv import load_dotenv
from sqlmodel import create_engine, Session
import os

# Carrega as variáveis de ambiente
load_dotenv()

db_connection = os.getenv("DB_CONNECTION")

# Cria uma engine para conexão com o banco de dados
def get_engine():
    engine = create_engine(db_connection)
    return engine

# Cria uma sessão com o banco de dados
def get_session():
    engine = get_engine()
    with Session(engine) as session:
        yield session
