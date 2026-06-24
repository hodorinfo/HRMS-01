from typing import Optional
from pydantic import BaseModel, ConfigDict
from horilla_common.schemas import HorillaSchemaBase

class EmployeeShiftScheduleBase(BaseModel):
    day_id: int
    shift_id: int
    minimum_working_hour: str = "08:15"
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    is_night_shift: bool = False
    is_auto_punch_out_enabled: bool = False
    auto_punch_out_time: Optional[str] = None

class EmployeeShiftScheduleCreate(EmployeeShiftScheduleBase):
    pass

class EmployeeShiftScheduleUpdate(BaseModel):
    day_id: Optional[int] = None
    shift_id: Optional[int] = None
    minimum_working_hour: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    is_night_shift: Optional[bool] = None
    is_auto_punch_out_enabled: Optional[bool] = None
    auto_punch_out_time: Optional[str] = None

class EmployeeShiftScheduleRead(HorillaSchemaBase, EmployeeShiftScheduleBase):
    id: int
