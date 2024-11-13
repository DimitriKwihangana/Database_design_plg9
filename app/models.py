from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ChemicalProperties(Base):
    __tablename__ = 'chemical_properties'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ph = Column(Float, nullable=False)
    chloramines = Column(Float, nullable=False)
    sulfate = Column(Float, nullable=False)
    conductivity = Column(Float, nullable=False)
    organic_carbon = Column(Float, nullable=False)
    trihalomethanes = Column(Float, nullable=False)
    water_quality = relationship("WaterQuality", back_populates="chemical_properties")

class PhysicalProperties(Base):
    __tablename__ = 'physical_properties'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    hardness = Column(Float, nullable=False)
    solids = Column(Float, nullable=False)
    turbidity = Column(Float, nullable=False)
    water_quality = relationship("WaterQuality", back_populates="physical_properties")

class WaterQuality(Base):
    __tablename__ = 'water_quality'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    potability = Column(Integer, nullable=False)
    chemical_properties_id = Column(Integer, ForeignKey('chemical_properties.id'), nullable=False)
    physical_properties_id = Column(Integer, ForeignKey('physical_properties.id'), nullable=False)
    chemical_properties = relationship("ChemicalProperties", back_populates="water_quality")
    physical_properties = relationship("PhysicalProperties", back_populates="water_quality")
