from typing import Annotated
from fastapi import FastAPI, Depends, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlmodel import SQLModel, Session, select, inspect
from fastapi.templating import Jinja2Templates
from sqlalchemy.exc import SQLAlchemyError

from models.models import Montadora
from models.forms import InputMontadora
from repository.montadora_repository import MontadoraRepository
from persistence.database import get_engine, get_session

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

SQLModel.metadata.create_all(get_engine())

SessionDB = Annotated[Session, Depends(get_session)]

montadora_repository = MontadoraRepository()


# Rota para a lista de montadoras
@app.get("/montadora_list")
def montadora_list(request: Request, session: SessionDB):
    montadoras = montadora_repository.get_all(session)
    return templates.TemplateResponse("montadora_list.html", {"request": request, "montadoras": montadoras})


# Rota para página de adição de montadora
@app.get("/montadora_add")
def montadora_add(request: Request):
    return templates.TemplateResponse("montadora_add.html", {"request": request})


# Rota para adicionar montadora
@app.post("/montadora_add")
def montadora_add(session: SessionDB, montadora: Annotated[InputMontadora, Form()]):
    new_montadora = Montadora(**montadora.dict())
    montadora_repository.create(session, new_montadora)
    return RedirectResponse("/montadora_list", status_code=303)


# Rota para ver detalhes da montadora
@app.get("/montadora_details/{id}")
def montadora_detail(request: Request, session: SessionDB, id: str):
    montadora = montadora_repository.get_by_id(session, id)
    return templates.TemplateResponse("montadora_details.html", {"request": request, "montadora": montadora})


# Rota para página de edição de montadora
@app.get("/montadora_update/{id}")
def montadora_update(request: Request, session: SessionDB, id: str):
    montadora = montadora_repository.get_by_id(session, id)
    return templates.TemplateResponse("montadora_update.html", {"request": request, "montadora": montadora})


# Rota para editar montadora
@app.post("/montadora_update/{id}")
def montadora_update(session: SessionDB, id: str, montadora: Annotated[InputMontadora, Form()]):
    montadora_repository.update(session, id, montadora)
    return RedirectResponse("/montadora_list", status_code=303)


# Rota para excluir montadora
@app.post("/montadora_delete/{id}")
def montadora_delete(session: SessionDB, id: str):
    montadora_repository.delete(session, id)
    return RedirectResponse("/montadora_list", status_code=303)


























@app.get("/test-connection/")
def test_db_connection(session: SessionDB):
    try:
        # buscar tabela e suas colunas e tipos

        result = session.exec(select(Montadora)).all()
        inspector = inspect(session.bind)
        tables = inspector.get_table_names()
        for table in tables:
            columns = inspector.get_columns(table)
            print(f"Table: {table}")
            for column in columns:
                print(f"Column: {column['name']} Type: {column['type']}")

        return {"message": "Conexão estabelecida!", "registros": len(result), "tabelas": tables}
    except SQLAlchemyError as e:
        return {"error": f"Erro ao conectar ao banco de dados: {e}"}
