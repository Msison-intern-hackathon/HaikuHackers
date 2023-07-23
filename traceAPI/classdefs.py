from pydantic import BaseModel, Field
from typing import List, Optional

class Geometry(BaseModel):
    x: float
    y: float
    spatialReference: dict

class LayerInfo(BaseModel):
    id: int
    name: str

class FeatureAttributes(BaseModel):
    esrignss_positionsourcetype: int
    esrignss_receiver: Optional[None]
    esrignss_h_rms: Optional[None]
    esrignss_v_rms: Optional[None]
    esrignss_latitude: float
    esrignss_longitude: float
    esrignss_altitude: Optional[None]
    esrignss_fixdatetime: int
    globalid: str

class Result(BaseModel):
    globalId: str
    objectId: int
    success: bool
    uniqueId: int

class Feature(BaseModel):
    attributes: FeatureAttributes
    geometry: Geometry
    result: Result
    layerInfo: LayerInfo

class Photo(BaseModel):
    id: int
    globalId: str
    name: str
    contentType: str
    keywords: str
    exifInfo: Optional[None]
    url: str
    parentObjectId: int

class AttachmentInfo(BaseModel):
    photo: List[Photo]

class AddResults(BaseModel):
    globalId: str
    objectId: int
    success: bool
    uniqueId: int

class Attachments(BaseModel):
    addResults: List[AddResults]

class Response(BaseModel):
    addResults: List[AddResults]
    attachments: Attachments
    id: int

class PortalInfo(BaseModel):
    url: str
    token: str

class UserInfo(BaseModel):
    username: str
    firstName: str
    lastName: str
    fullName: str
    email: str

class ProjectInfo(BaseModel):
    projectItemId: str
    projectTitle: str
    serviceItemId: str
    serviceUrl: str

class ResponseItem(BaseModel):
    feature: Feature
    attachmentInfo: AttachmentInfo
    response: Response
    portalInfo: PortalInfo
    userInfo: UserInfo
    projectInfo: ProjectInfo

class Root(BaseModel):
    root: List[ResponseItem]
