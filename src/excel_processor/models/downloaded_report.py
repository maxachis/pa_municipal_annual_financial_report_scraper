from pydantic import BaseModel, Field, field_validator


class DownloadedReportMetadata(BaseModel):
    report_id: int
    xlsx_file: str = Field(..., description="An .xlsx filename")

    @field_validator('xlsx_file')
    def validate_xlsx_file(cls, value: str):
        if not value.lower().endswith('.xlsx'):
            raise ValueError("String must end with '.xlsx'")

        return value