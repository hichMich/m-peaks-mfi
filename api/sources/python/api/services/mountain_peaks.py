from api.dao.mountain_peaks import create_mountain_peak, select_all_mountains_peaks, retrieve_mountain_peaks_by_criteria
from api.schemas.mountain_peaks import MountainPeaks
from api.services import utils
from api import context as ctx
from api.exceptions import ServiceFunctionalException, ServiceTechnicalException
from fastapi import status as http_status
import logging
from typing import List
from sqlalchemy.orm import Session
from uuid import UUID


logger = logging.getLogger('services.mountain_peaks')

def get_mountain_peaks_by_all(db: Session) -> List[MountainPeaks]:
    """
        Get all moutain peaks

        Parameters: 
        - db: SqlAlchemy session

        Returns:
        - List[MountainPeaks]: The list of mountain peaks
    """
    try:
        m_peaks = select_all_mountains_peaks(db)
        mountains_peaks = [ 
                MountainPeaks(
                    name=m_peak.name,
                    longitude=m_peak.longitude,
                    latitude=m_peak.latitude,
                    altitude=m_peak.altitude
                ) for m_peak in m_peaks
            ]
        return mountains_peaks
    except ServiceTechnicalException as ex:
        raise ex


def add_mountain_peak(data: MountainPeaks, db: Session) -> UUID:
    """
        Create a moutain peak
        Attention ! The triplet (longitude, latitude, altitude) is unique

        Parameters: 
        - data: MountainPeaks
        - db: SqlAlchemy session

        Returns:
        - UUID: The uuid of the created montain peak
    """
    validated_data = utils.all_attrs_are_valid(data)
    if not validated_data:
        raise ServiceFunctionalException(
            msg=f"Error ! Please check the requestBody object {data}",
            code_status=http_status.HTTP_400_BAD_REQUEST
        ) 
    try:
        mountain_peak_uuid = create_mountain_peak(data, db)
        return mountain_peak_uuid
    except ServiceTechnicalException as ex:
        raise ex

    