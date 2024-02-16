import uuid

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Text, Column, Float, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID


Base = declarative_base()


class MontainPeak(Base):
    __tablename__ = 'montain_peak'
    __table_args__ = (
            UniqueConstraint('latitude', 'longitude', 'altitude', name='montain_uq',),
            UniqueConstraint('name', name='name_uq'),
        )

    uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    name = Column(Text, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    altitude = Column(Float, nullable=False)
