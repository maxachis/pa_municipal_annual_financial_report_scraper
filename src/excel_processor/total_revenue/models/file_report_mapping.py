from pydantic import BaseModel


class FileReportMapping(BaseModel):
    report_id: int
    filename: str