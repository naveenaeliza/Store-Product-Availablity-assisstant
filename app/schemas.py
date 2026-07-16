from pydantic import BaseModel, Field


class ProductAvailabilityRequest(BaseModel):
    query: str = Field(..., min_length=1)

    user_latitude: float = Field(..., ge=-90, le=90)

    user_longitude: float = Field(..., ge=-180, le=180)


class ProductAvailabilityResponse(BaseModel):
    status: str
    response: str