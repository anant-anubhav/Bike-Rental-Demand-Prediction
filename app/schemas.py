from pydantic import BaseModel, Field
from typing import Optional


class PredictionInput(BaseModel):
    """Input schema for bike rental prediction"""
    season: int = Field(..., ge=1, le=4, description="Season: 1=Spring, 2=Summer, 3=Fall, 4=Winter")
    yr: int = Field(..., ge=0, le=1, description="Year: 0=2011, 1=2012")
    mnth: int = Field(..., ge=1, le=12, description="Month: 1-12")
    hr: int = Field(..., ge=0, le=23, description="Hour: 0-23")
    holiday: int = Field(..., ge=0, le=1, description="Holiday: 0=No, 1=Yes")
    weekday: int = Field(..., ge=0, le=6, description="Weekday: 0=Sunday to 6=Saturday")
    workingday: int = Field(..., ge=0, le=1, description="Working day: 0=No, 1=Yes")
    weathersit: int = Field(..., ge=1, le=4, description="Weather: 1=Clear, 2=Mist, 3=Light Rain, 4=Heavy Rain")
    temp: float = Field(..., ge=0, le=1, description="Normalized temperature (0-1)")
    atemp: float = Field(..., ge=0, le=1, description="Normalized feeling temperature (0-1)")
    hum: float = Field(..., ge=0, le=1, description="Normalized humidity (0-1)")
    windspeed: float = Field(..., ge=0, le=1, description="Normalized wind speed (0-1)")

    class Config:
        json_schema_extra = {
            "example": {
                "season": 3,
                "yr": 1,
                "mnth": 9,
                "hr": 17,
                "holiday": 0,
                "weekday": 4,
                "workingday": 1,
                "weathersit": 1,
                "temp": 0.76,
                "atemp": 0.72,
                "hum": 0.45,
                "windspeed": 0.15
            }
        }


class PredictionOutput(BaseModel):
    """Output schema for bike rental prediction"""
    prediction: int = Field(..., description="Predicted number of bike rentals")
    status: str = Field(default="success", description="Status of the prediction")
    message: Optional[str] = Field(default=None, description="Additional message")


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    model_loaded: bool
    version: str = "1.0.0"
