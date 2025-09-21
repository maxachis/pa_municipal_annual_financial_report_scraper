from pydantic import BaseModel


class ReportFileInsert(BaseModel):
    report_id: int
    file_name: str