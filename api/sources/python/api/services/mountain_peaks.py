from api.dao.mountain_peaks import create_mountain_peak
from api.schemas.mountain_peaks import MountainPeaks
from api.services import utils
from api import context as ctx
from api.exceptions import ServiceFunctionalException, ServiceTechnicalException
from api.dao.mountain_peaks import retrieve_mountain_peaks_by_criteria
from fastapi import status as http_status
import logging
from typing import List, Tuple, Optional, Dict
from sqlalchemy.orm import Session
from uuid import UUID


logger = logging.getLogger('services.mountain_peaks')

def retrieve_mountain_peaks(data: MountainPeaks, db: Session) -> List[MountainPeaks]:
    pass

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
    try:
        validated_data = utils.all_attrs_are_valid(data)
        if not validated_data:
            raise ServiceFunctionalException(
                msg=f"Error ! Please check the requestBody object {data}",
                code_status=http_status.HTTP_422_UNPROCESSABLE_ENTITY
            ) 
        mountain_peak_uuid = create_mountain_peak(data, db)
        return mountain_peak_uuid
    except Exception as ex:
        logger.error("Mountain peak is not created, root cause: {ex}")
