import logging
from api.schemas.mountain_peaks import (
    MountainPeaks,
    MountainPeaksEntire,
    Location,
)
from api.exceptions import ServiceTechnicalException
from api.models import MountainPeak
from geoalchemy2.shape import from_shape
from shapely.geometry import Point
from fastapi import status as http_status
from typing import List, Dict
from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete
from uuid import UUID


logger = logging.getLogger('dao.mountain_peaks')


def retrieve_mountain_peak_by_uuid(uuid: UUID, db: Session) -> MountainPeaksEntire:
    try:
        mountain_peak = db.execute(select(MountainPeak).where(MountainPeak.uuid == uuid))
        return MountainPeaksEntire.model_validate(mountain_peak)
    except Exception as ex:
        raise ServiceTechnicalException(
            msg=f"Can't retrieve the mountain peak by uuid {uuid}, root cause: {ex}",
            code_status=http_status.HTTP_500_INTERNAL_SERVER_ERROR
        )


def retrieve_mountain_peak_by_name(name: str, db: Session) -> MountainPeaksEntire:
    try:
        mountain_peak = db.execute(select(MountainPeak).where(MountainPeak.name == name))
        return MountainPeaksEntire.model_validate(mountain_peak)
    except Exception as ex:
        raise ServiceTechnicalException(
            msg=f"Can't retrieve the mountain peak by name {name}, root cause: {ex}",
            code_status=http_status.HTTP_500_INTERNAL_SERVER_ERROR
        )


def retrieve_mountain_peak_by_location(location: Location, db: Session) -> MountainPeaksEntire:
    try:
        mountain_peak = db.execute(select(MountainPeak).where(
            MountainPeak.longitude == location.longitude,
            MountainPeak.latitude == location.latitude,
            MountainPeak.altitude == location.altitude
        )).one_or_none()
        if mountain_peak is None:
            return
        m_peak = mountain_peak._asdict()
        mountain_peak_obj = MountainPeaksEntire(
            uuid=m_peak['MountainPeak'].uuid,
            name=m_peak['MountainPeak'].name,
            location=Location(
                longitude=m_peak['MountainPeak'].longitude,
                latitude=m_peak['MountainPeak'].latitude,
                altitude=m_peak['MountainPeak'].altitude
            )
        )
        return mountain_peak_obj
    except Exception as ex:
        raise ServiceTechnicalException(
            msg=f"Can't retrieve the mountain peak by location {location}, root cause: {ex}",
            code_status=http_status.HTTP_500_INTERNAL_SERVER_ERROR
        )



def retrieve_mountain_peaks_by_all(db: Session) -> List[MountainPeaks]:
    """
        find mountain peaks by all (name, longitude, latitude, altitude)
        params:
        data: MountainPeaks
        db: sql session
    """

    try:
        return db.query(MountainPeak).all()
    except Exception as ex:
        msg = f"Can't retrieve all mountains peaks, root cause: {ex}"
        raise ServiceTechnicalException(msg)


def create_mountain_peak(data: MountainPeaks, db: Session) -> UUID:
    try:
        data_dict = data.model_dump()
        data_dict['latitude'] = data_dict['location']['latitude']
        data_dict['longitude'] = data_dict['location']['longitude']
        data_dict['altitude'] = data_dict['location']['altitude']
        data_dict.update({
            'location': from_shape(
                Point(data_dict['longitude'], data_dict['latitude'], data_dict['altitude']),
                srid=4326
            ),
        })
        mountain_peak = MountainPeak(**data_dict)
        db.add(mountain_peak)
        db.commit()
        return mountain_peak.uuid
    except Exception as ex:
        raise ServiceTechnicalException(
            msg=f"Can't create the mountain peak, root cause: {ex}",
            code_status=http_status.HTTP_500_INTERNAL_SERVER_ERROR
        )


def select_all_mountains_peaks(db: Session) -> List[MountainPeak]:
    try:
        mountain_peaks = db.execute(select(MountainPeak)).scalars().all()
        return mountain_peaks
    except Exception as ex:
        raise ServiceTechnicalException(
            msg=f"Can't get all mountain peaks, root cause: {ex}",
            code_status=http_status.HTTP_500_INTERNAL_SERVER_ERROR
        )


def init_mountains_peaks(data: List[Dict], db: Session):
    try:
        m_peaks: List[MountainPeak] = list()
        for m_peak in data:
            m_peak['latitude'] = m_peak['location']['latitude']
            m_peak['longitude'] = m_peak['location']['longitude']
            m_peak['altitude'] = m_peak['location']['altitude']
            m_peak.update({
                'location': from_shape(
                    Point(m_peak['longitude'], m_peak['latitude'], m_peak['altitude']),
                    srid=4326
                ),
            })
            m_peaks.append(MountainPeak(**m_peak))
        db.add_all(m_peaks)
        db.commit()
    except Exception as ex:
        raise ServiceTechnicalException(
            msg=f"Can't create all mountain peaks, root cause: {ex}",
            code_status=http_status.HTTP_500_INTERNAL_SERVER_ERROR
        )


def update_m_peak(uuid: UUID, data: Dict, db: Session):
    try:
        data['latitude'] = data['location']['latitude']
        data['longitude'] = data['location']['longitude']
        data['altitude'] = data['location']['altitude']
        data.update({
            'location': from_shape(
                Point(data['longitude'], data['latitude'], data['altitude']),
                srid=4326
            ),
        })
        db.execute(update(MountainPeak).where(MountainPeak.uuid == uuid).values(**data))
        db.commit()
    except Exception as ex:
        raise ServiceTechnicalException(
            msg=f"Can't delete the mountain peak by uuid {uuid}, root cause: {ex}",
            code_status=http_status.HTTP_500_INTERNAL_SERVER_ERROR
        )


def delete_mountain_peak_by_uuid(uuid: UUID, db: Session):
    try:
        db.execute(delete(MountainPeak).where(MountainPeak.uuid == uuid))
        db.commit()
    except Exception as ex:
        raise ServiceTechnicalException(
            msg=f"Can't delete the mountain peak by uuid {uuid}, root cause: {ex}",
            code_status=http_status.HTTP_500_INTERNAL_SERVER_ERROR
        )


def delete_mountain_peak_by_name(name: str, db: Session):
    try:
        db.execute(delete(MountainPeak).where(MountainPeak.name == name))
        db.commit()
    except Exception as ex:
        raise ServiceTechnicalException(
            msg=f"Can't delete the mountain peak by name {name}, root cause: {ex}",
            code_status=http_status.HTTP_500_INTERNAL_SERVER_ERROR
        )


def delete_mountain_peak_by_location(location: Location, db: Session):
    try:
        db.execute(delete(MountainPeak).where(
            MountainPeak.longitude == location.longitude,
            MountainPeak.latitude == location.latitude,
            MountainPeak.altitude == location.altitude
        ))
        db.commit()
    except Exception as ex:
        raise ServiceTechnicalException(
            msg=f"Can't delete the mountain peak by location {location}, root cause: {ex}",
            code_status=http_status.HTTP_500_INTERNAL_SERVER_ERROR
        )
