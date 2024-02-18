import uuid

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Text, Column, Float, UniqueConstraint, Index
from sqlalchemy.dialects.postgresql import UUID
from geoalchemy2.types import Geometry 

Base = declarative_base()


class MountainPeak(Base):
    __tablename__ = 'mountain_peak'
    __table_args__ = (
            Index('idx_mountain_peak_name', 'name'),
            UniqueConstraint('latitude', 'longitude', 'altitude', name='mountain_uq',),
            UniqueConstraint('name', name='name_uq'),
        )

    uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    name = Column(Text, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    altitude = Column(Float, nullable=False)
    location = Column(Geometry('POINTZ'), nullable=False)
    
