from sqlmodel import Session, select
from ..models.models import Veiculo

class VeiculoRepository:

    def get_all(self, session: Session):
        sttm = select(Veiculo)
        veiculos = session.exec(sttm).all()
        return veiculos


    def get_by_id(self, session: Session, id: str):
        sttm = select(Veiculo).where(Veiculo.id == id)
        veiculo = session.exec(sttm).first()
        return veiculo


    def create(self, session: Session, veiculo: Veiculo):
        session.add(veiculo)
        session.commit()
        session.refresh(veiculo)
        return veiculo


    def update(self, session: Session, id: str, veiculo: Veiculo):
        existing_veiculo = self.get_by_id(session, id)

        for key, value in vars(veiculo).items():
            setattr(existing_veiculo, key, value) if value else None

        updated_veiculo = session.merge(existing_veiculo)
        session.commit()
        session.refresh(updated_veiculo)
        return updated_veiculo


    def delete(self, session: Session, id: str):
        old_veiculo = self.get_by_id(session, id)
        session.delete(old_veiculo)
        session.commit()
        return old_veiculo
