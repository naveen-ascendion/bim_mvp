from crewai.tools import BaseTool
from typing import Type, List
from pydantic import BaseModel, Field
import csv
import os

class WriteCSVColumnInput(BaseModel):
    input_csv_path: str = Field(..., description="Source CSV file path")
    output_csv_path: str = Field(..., description="Destination CSV file path")
    column_name: str = Field(..., description="New column name")
    column_values: List[str] = Field(..., description="List of values (one per row)")

class WriteCSVColumnTool(BaseTool):
    name: str = "write_csv_with_column"
    description: str = "Create a new CSV with an added or updated column, preserving the input file."
    args_schema: Type[BaseModel] = WriteCSVColumnInput

    def _run(
        self,
        input_csv_path: str,
        output_csv_path: str,
        column_name: str,
        column_values: List[str],
    ) -> str:
        if not os.path.exists(input_csv_path):
            return f"File not found: {input_csv_path}"

        with open(input_csv_path, "r", encoding="utf-8") as f:
            reader = list(csv.DictReader(f))

        if len(reader) != len(column_values):
            return "Row count mismatch between CSV and provided values."

        fieldnames = list(reader[0].keys())
        if column_name not in fieldnames:
            fieldnames.append(column_name)

        for row, value in zip(reader, column_values):
            row[column_name] = value

        os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)

        with open(output_csv_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(reader)

        return f"New file created at {output_csv_path}"

write_csv_with_column = WriteCSVColumnTool()