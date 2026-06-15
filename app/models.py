from sqlalchemy import Column, Integer
from .database import Base

class Visitas(Base):
    __tablename__ = "visitas"
    
    id = Column(Integer, primary_key=True, index=True)
    contador = Column(Integer, default=0)