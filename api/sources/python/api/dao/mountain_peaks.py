import logging
from api.schemas.mountain_peaks import MountainPeaks
from api.exceptions import ServiceTechnicalException
from api.models import MountainPeak
from fastapi import status as http_status
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import select, update, tuple_, or_, and_
from uuid import UUID


logger = logging.getLogger('dao.mountain_peaks')


def retrieve_mountain_peaks_by_criteria(data: MountainPeaks, db: Session) -> List[MountainPeaks]:
    """
        find mountain peaks by criteria (name, longitude, latitude, altitude)
        params:
        data: MountainPeaks
        db: sql session  
    """

    try:
        mountain_peak = db.query(MountainPeak).where(data)
        return MountainPeaks.model_validate(mountain_peak)
    except Exception as ex:
        msg = f"Can't retrieve mountain peak, root cause: {ex}"
        logger.error(msg)
        raise ServiceTechnicalException(msg)


def retrieve_mountain_peaks_by_all(db: Session) -> MountainPeaks:
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