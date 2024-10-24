from sqlmodel import Session, select
from ..models.models import Modelo

class ModeloRepository:

    def get_all(self, session: Session):
        sttm = select(Modelo)
        modelos = session.exec(sttm).all()
        return modelos


    def get_by_id(self, session: Session, id: str):
        sttm = select(Modelo).where(Modelo.id == id)
        modelo = session.exec(sttm).first()
        return modelo


    def create(self, session: Session, modelo: Modelo):
        session.add(modelo)
        session.commit()
        session.refresh(modelo)
        return modelo


    def update(self, session: Session, id: str, modelo: Modelo):
        existing_modelo = self.get_by_id(session, id)

        for key, value in vars(modelo).items():
            setattr(existing_modelo, key, value) if value else None

        updated_modelo = session.merge(existing_modelo)
        session.commit()
        session.refresh(updated_modelo)
        return updated_modelo


    def delete(self, session: Session, id: str):
        old_modelo = self.get_by_id(session, id)
        session.delete(old_modelo)
        session.commit()
        return old_modelo
