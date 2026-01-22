from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import csv
import os

class ReadCSVFileInput(BaseModel):
    file_path: str = Field(..., description="Path to CSV file")

class ReadCSVFileTool(BaseTool):
    name: str = "read_csv_file"
    description: str = "Read a CSV file and return its full contents as text."
    args_schema: Type[BaseModel] = ReadCSVFileInput

    def _run(self, file_path: str) -> str:
        if not os.path.exists(file_path):
            return f"File not found: {file_path}"

        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

read_csv_file = ReadCSVFileTool()