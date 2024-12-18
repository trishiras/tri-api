from uuid import uuid4
from beanie import Document
from datetime import datetime
from fastapi import HTTPException
from typing import Optional, List
from pydantic import Field, BaseModel
from tri_api.models.super.user import SuperUserLogin
from tri_api.support.enums import ResponseCode, ExceptionMessage


class ScannerTaskArguments(BaseModel):
    target: str
    target_type: str
    scanner_data: Optional[dict] = Field(default={})


class ScannerTaskBase(BaseModel):
    task_id: str
    status: Optional[str] = Field(default=None)
    result_url: Optional[str] = Field(default=None)
    status_message: Optional[str] = Field(default=None)
    synced: bool = Field(default=False)


class ScannerTask(Document):
    id: str = Field(default_factory=lambda: str(uuid4().hex))
    user: str
    target: str
    target_type: str
    scanner: str
    scanner_data: Optional[dict] = Field(default=dict)
    status: Optional[str] = Field(default=None)
    result_url: Optional[str] = Field(default=None)
    status_message: Optional[str] = Field(default=None)
    synced: bool = Field(default=False)
    date_time: datetime = Field(default=datetime.now())

    @classmethod
    async def update_task(
        cls,
        task: ScannerTaskBase,
    ) -> "ScannerTask":
        scanner_task = None

        # Find scanner task by ID
        if task.task_id:
            scanner_task = await cls.find_one(cls.id == task.task_id)
            if not scanner_task:
                raise HTTPException(
                    status_code=ResponseCode.not_found.value,
                    detail=ExceptionMessage.task_not_found_by_id.value,
                )
        else:
            raise HTTPException(
                status_code=ResponseCode.bad_request.value,
                detail=ExceptionMessage.task_id_needed.value,
            )

        scanner_task.status = task.status
        scanner_task.result_url = task.result_url
        scanner_task.status_message = task.status_message
        scanner_task.synced = task.synced

        await scanner_task.save()

        return scanner_task


class PaginatedScannerTaskResponse(BaseModel):
    total: int
    page_number: int
    data: List[ScannerTask]


class ScannerTaskUpdate(SuperUserLogin):
    task_id: str
    status: Optional[str] = Field(default=None)
    result_url: Optional[str] = Field(default=None)
    status_message: Optional[str] = Field(default=None)
    synced: bool = Field(default=False)
