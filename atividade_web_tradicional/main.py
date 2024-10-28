from typing import Annotated
from fastapi import FastAPI, Depends, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlmodel import SQLModel, Session, select, inspect
from fastapi.templating import Jinja2Templates
from sqlalchemy.exc import SQLAlchemyError

from persistence.database import get_engine, get_session

from repository.montadora_repository import MontadoraRepository
from repository.modelo_repository import ModeloRepository
from repository.veiculo_repository import VeiculoRepository

from models.models import Montadora, Modelo, Veiculo
from models.forms import InputMontadora, InputModelo, InputVeiculo

app = FastAPI()

app.mount("/static/", StaticFiles(directory="static/"), name="static")

templates = Jinja2Templates(directory="templates")

SQLModel.metadata.create_all(get_engine())

SessionDB = Annotated[Session, Depends(get_session)]

montadora_repository = MontadoraRepository()
modelo_repository = ModeloRepository()
veiculo_repository = VeiculoRepository()



#################################### Rotas para Montadora ####################################


# Rota para a lista de montadoras
@app.get("/montadoras")
def listar_montadoras(request: Request, session: SessionDB):
    montadoras = montadora_repository.get_all(session)

    return templates.TemplateResponse(
        "montadora/listar_montadoras.html", {"request": request, "montadoras": montadoras}
    )


# Rota para página de adição de montadora
@app.get("/montadoras/novo")
def adicionar_montadora(request: Request):

    return templates.TemplateResponse(
        "montadora/adicionar_montadora.html", {"request": request}
    )


# Rota para adicionar montadora
@app.post("/montadoras/novo")
def adicionar_montadora(session: SessionDB, montadora: Annotated[InputMontadora, Form()]):
    new_montadora = Montadora(**montadora.dict())
    montadora_repository.create(session, new_montadora)

    return RedirectResponse("/montadoras", status_code=303)


# Rota para ver detalhes da montadora
@app.get("/montadoras/{id}")
def detalhar_montadora(request: Request, session: SessionDB, id: str):
    montadora = montadora_repository.get_by_id(session, id)

    return templates.TemplateResponse(
        "montadora/detalhar_montadora.html", {"request": request, "montadora": montadora}
    )


# Rota para página de edição de montadora
@app.get("/montadoras/{id}/editar")
def editar_montadora(request: Request, session: SessionDB, id: str):
    montadora = montadora_repository.get_by_id(session, id)

    return templates.TemplateResponse(
        "montadora/editar_montadora.html", {"request": request, "montadora": montadora}
    )


# Rota para editar montadora
@app.post("/montadoras/{id}/editar")
def editar_montadora(session: SessionDB, id: str, montadora: Annotated[InputMontadora, Form()]):
    montadora_repository.update(session, id, montadora)

    return RedirectResponse("/montadoras", status_code=303)


# Rota para excluir montadora
@app.post("/montadoras/{id}/deletar")
def deletar_montadora(session: SessionDB, id: str):
    montadora_repository.delete(session, id)

    return RedirectResponse("/montadoras", status_code=303)



#################################### Rotas para Modelo ####################################


# Rotas para listar modelos
@app.get("/modelos")
def listar_modelos(request: Request, session: SessionDB):
    modelos = modelo_repository.get_all(session)

    return templates.TemplateResponse(
        "modelo/listar_modelos.html", {"request": request, "modelos": modelos}
    )


# Rota para página de adição de modelo
@app.get("/modelos/novo")
def adicionar_modelo(request: Request, session: SessionDB):
    montadoras = montadora_repository.get_all(session)

    return templates.TemplateResponse(
        "modelo/adicionar_modelo.html", {"request": request, "montadoras": montadoras}
    )


# Rota para adicionar modelo
@app.post("/modelos/novo")
def adicionar_modelo(session: SessionDB, modelo: Annotated[InputModelo, Form()]):
    new_modelo = Modelo(**modelo.dict())
    modelo_repository.create(session, new_modelo)

    return RedirectResponse("/modelos", status_code=303)


# Rota para ver detalhes do modelo
@app.get("/modelos/{id}")
def detalhar_modelo(request: Request, session: SessionDB, id: str):
    modelo = modelo_repository.get_by_id(session, id)

    return templates.TemplateResponse(
        "modelo/detalhar_modelo.html", {"request": request, "modelo": modelo}
    )


# Rota para página de edição de modelo
@app.get("/modelos/{id}/editar")
def editar_modelo(request: Request, session: SessionDB, id: str):
    modelo = modelo_repository.get_by_id(session, id)
    montadoras = montadora_repository.get_all(session)

    return templates.TemplateResponse(
        "modelo/editar_modelo.html", {"request": request, "modelo": modelo, "montadoras": montadoras}
    )


# Rota para editar modelo
@app.post("/modelos/{id}/editar")
def editar_modelo(session: SessionDB, id: str, modelo: Annotated[InputModelo, Form()]):
    modelo_repository.update(session, id, modelo)

    return RedirectResponse("/modelos", status_code=303)


# Rota para excluir modelo
@app.post("/modelos/{id}/deletar")
def deletar_modelo(session: SessionDB, id: str):
    modelo_repository.delete(session, id)

    return RedirectResponse("/modelos", status_code=303)



#################################### Rotas para Veiculo ####################################


# Rotas para listar veiculos
@app.get("/veiculos")
def listar_veiculos(request: Request, session: SessionDB):
    veiculos = veiculo_repository.get_all(session)

    return templates.TemplateResponse(
        "veiculo/listar_veiculos.html", {"request": request, "veiculos": veiculos}
    )


# Rota para página de adição de veiculo
@app.get("/veiculos/novo")
def adicionar_veiculo(request: Request, session: SessionDB):
    modelos = modelo_repository.get_all(session)

    return templates.TemplateResponse(
        "veiculo/adicionar_veiculo.html", {"request": request, "modelos": modelos}
    )


# Rota para adicionar veiculo
@app.post("/veiculos/novo")
def adicionar_veiculo(session: SessionDB, veiculo: Annotated[InputVeiculo, Form()]):
    new_veiculo = Veiculo(**veiculo.dict())
    veiculo_repository.create(session, new_veiculo)

    return RedirectResponse("/veiculos", status_code=303)


# Rota para ver detalhes do veiculo
@app.get("/veiculos/{id}")
def detalhar_veiculo(request: Request, session: SessionDB, id: str):
    veiculo = veiculo_repository.get_by_id(session, id)

    return templates.TemplateResponse(
        "veiculo/detalhar_veiculo.html", {"request": request, "veiculo": veiculo}
    )


# Rota para página de edição de veiculo
@app.get("/veiculos/{id}/editar")
def editar_veiculo(request: Request, session: SessionDB, id: str):
    veiculo = veiculo_repository.get_by_id(session, id)
    modelos = modelo_repository.get_all(session)

    return templates.TemplateResponse(
        "veiculo/editar_veiculo.html", {"request": request, "veiculo": veiculo, "modelos": modelos}
    )


# Rota para editar veiculo
@app.post("/veiculos/{id}/editar")
def editar_veiculo(session: SessionDB, id: str, veiculo: Annotated[InputVeiculo, Form()]):
    veiculo_repository.update(session, id, veiculo)

    return RedirectResponse("/veiculos", status_code=303)


# Rota para excluir veiculo
@app.post("/veiculos/{id}/deletar")
def deletar_veiculo(session: SessionDB, id: str):
    veiculo_repository.delete(session, id)

    return RedirectResponse("/veiculos", status_code=303)



#################################### Teste de Conexão ####################################


# Rota para teste de conexão com o banco de dados
@app.get("/test-connection/")
def test_db_connection(session: SessionDB):
    try:
        result = session.exec(select(Montadora)).all()
        inspector = inspect(session.bind)
        tables = inspector.get_table_names()
        for table in tables:
            columns = inspector.get_columns(table)
            print(f"Table: {table}")
            for column in columns:
                print(f"Coluna: {column['name']} Tipo: {column['type']}")

        return {"message": "Conexão estabelecida!", "registros": len(result), "tabelas": tables}
    except SQLAlchemyError as e:
        return {"error": f"Erro ao conectar ao banco de dados: {e}"}
