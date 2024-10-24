from sqlmodel import Session, select
from models.models import Montadora
from models.forms import InputMontadora

class MontadoraRepository:

    def get_all(self, session: Session):
        sttm = select(Montadora)
        montadoras = session.exec(sttm).all()
        return montadoras


    def get_by_id(self, session: Session, id: str):
        sttm = select(Montadora).where(Montadora.id == id)
        montadora = session.exec(sttm).first()
        return montadora


    def create(self, session: Session, montadora: Montadora):
        session.add(montadora)
        session.commit()
        session.refresh(montadora)
        return montadora


    def update(self, session: Session, id: str, montadora: Montadora):
        existing_montadora = self.get_by_id(session, id)

        for key, value in vars(montadora).items():
            setattr(existing_montadora, key, value) if value else None

        updated_montadora = session.merge(existing_montadora)
        session.commit()
        session.refresh(updated_montadora)
        return updated_montadora


    def delete(self, session: Session, id: str):
        old_montadora = self.get_by_id(session, id)
        session.delete(old_montadora)
        session.commit()
        return old_montadora
