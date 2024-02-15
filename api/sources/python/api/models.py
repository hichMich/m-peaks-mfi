import uuid

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Text, Column, Float, UniqueConstraint
from sqlalchemy.orm import validates
from sqlalchemy.dialects.postgresql import UUID


Base = declarative_base()


class MontainPeak(Base):
    __tablename__ = 'montain_peak'
    __table_args__ = (
            UniqueConstraint('latitude', 'longitude', 'altitude',), name='montain_uq',
            UniqueConstraint('name', name='name_uq'),
        )

    uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    name = Column(Text, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    altitude = Column(Float, nullable=False)  

    @validates('rating')
    def validate_integer(self, key, field):
        if not field:
            return None
        if not field.isnumeric():
            raise ValueError(f"bad type, {key} must be integer")
        return field
