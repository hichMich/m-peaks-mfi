from pydantic import Field
from api.schemas.common import ApiBaseModel
from typing import Optional
from uuid import UUID


class MountainPeaks(ApiBaseModel):
    """
        This class define a MountainPeak object
    """
    name: Optional[str] = Field(title='The name of the mountain peak')
    longitude: Optional[float] = Field(title='The longitude of the mountain peak')
    latitude: Optional[float] = Field(title='The latitude of the mountain peak')
    altitude: Optional[float] = Field(title='The altitude of the mountain peak')


class MountainPeakOnCreateResponse(ApiBaseModel):
    """
        This class define the mountain peak response on create
    """
    uuid: UUID = Field(title='The uuid following a creation of a mountain peak')
