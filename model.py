from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class WaterQuality(Base):
    __tablename__ = 'water_quality'
    sample_id = Column(Integer, primary_key=True, autoincrement=True)
    potability = Column(Boolean)
    chemical_properties = relationship("ChemicalProperties", back_populates="water_quality")
    physical_properties = relationship("PhysicalProperties", back_populates="water_quality")


class ChemicalProperties(Base):
    __tablename__ = 'chemical_properties'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    sample_id = Column(Integer, ForeignKey('water_quality.sample_id'))
    ph = Column(Float)
    chloramines = Column(Float)
    sulfate = Column(Float)
    conductivity = Column(Float)
    organic_carbon = Column(Float)
    trihalomethanes = Column(Float)
    water_quality = relationship("WaterQuality", back_populates="chemical_properties")


class PhysicalProperties(Base):
    __tablename__ = 'physical_properties'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    sample_id = Column(Integer, ForeignKey('water_quality.sample_id'))
    hardness = Column(Float)
    solids = Column(Float)
    turbidity = Column(Float)
    water_quality = relationship("WaterQuality", back_populates="physical_properties")
