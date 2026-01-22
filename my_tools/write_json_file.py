from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import json
import os

class WriteJSONFileInput(BaseModel):
    file_path: str = Field(..., description="Output JSON file path")
    json_data: str = Field(..., description="Valid JSON string")

class WriteJSONFileTool(BaseTool):
    name: str = "write_json_file"
    description: str = "Write JSON string to a file."
    args_schema: Type[BaseModel] = WriteJSONFileInput

    def _run(self, file_path: str, json_data: str) -> str:
        try:
            parsed = json.loads(json_data)
        except json.JSONDecodeError as e:
            return f"Invalid JSON: {e}"

        os.makedirs(os.path.dirname(file_path) or ".", exist_ok=True)

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(parsed, f, indent=2, ensure_ascii=False)

        return f"JSON written to {file_path}"

write_json_file = WriteJSONFileTool()