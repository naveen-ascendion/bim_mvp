from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import json
import os

class ReadJSONFileInput(BaseModel):
    file_path: str = Field(..., description="Path to JSON file")

class ReadJSONFileTool(BaseTool):
    name: str = "read_json_file"
    description: str = "Read a JSON file and return formatted JSON text."
    args_schema: Type[BaseModel] = ReadJSONFileInput

    def _run(self, file_path: str) -> str:
        if not os.path.exists(file_path):
            return f"File not found: {file_path}"

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        return json.dumps(data, indent=2)
    
read_json_file = ReadJSONFileTool()
