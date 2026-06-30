from sqlalchemy import Boolean,String,Column,Integer,ForeignKey,DECIMAL,Float,Numeric,NCHAR
from sqlalchemy.ext.declarative import declarative_base
from database import Base
from sqlalchemy.orm import relationship
from pydantic import BaseModel


class EmploiyesModel(Base):
    __tablename__ = "emploiyes"  # Table name

    NumCompte = Column(String, primary_key=True, index=True)
    Nom = Column(String, nullable=False)
    Grade = Column(String, nullable=False)
    Poste = Column(String, nullable=False)
    lieu_de_travail = Column(String, nullable=False)  # Adjust type as necessary
    residence_admin = Column(String, nullable=False)
    # Define relationship back to DemandeModel
    demandes = relationship("DemandeModel", back_populates="employee")

class DemandeModel(Base):
    __tablename__ = "demande"  # Table name

    demande_id = Column(Integer, primary_key=True,autoincrement=True) # Use Numeric for numeric type
    NumCompte = Column(NCHAR, ForeignKey("emploiyes.NumCompte"), nullable=False)  # Ensure correct type
    type_prestation = Column(String, nullable=False)  # Matching String type
    gestion = Column(String, nullable=False)  # Matching String type
    Période_Déduction = Column(String, nullable=False)  # Adjust according to your schema
    Début_Déduction = Column(String, nullable=False)  # Adjust according to your schema
    Fin_Déduction = Column(String, nullable=False)  # Adjust according to your schema
    montant = Column(DECIMAL(12, 2), nullable=False)
    demande_statut = Column(String, nullable=False)
    employee = relationship("EmploiyesModel", back_populates="demandes")
   