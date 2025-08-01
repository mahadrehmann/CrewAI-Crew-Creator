# src/<project>/tools/file_writer_tool.py
from pydantic import BaseModel, Field
from typing import Type, Any, Dict, List
from crewai.tools import BaseTool

class FileWriteInput(BaseModel):
    content: str = Field(..., description="Planner output containing file:<path> code blocks")
    base_dir: str = Field(".", description="Root directory into which files should be written")

class FileWriteTool(BaseTool):
    name: str = "FileWriteTool"
    description: str = "Writes files from structured code blocks"
    args_schema: Type[BaseModel] = FileWriteInput

    def _run(self, content: str, base_dir: str = ".") -> Dict[str, Any]:
        import os, re
        created: List[str] = []
        errors: List[str] = []
        # Regex to match ```file:path\ncontent```
        blocks = re.findall(r"```file:(.*?)\n(.*?)```", content, re.DOTALL)
        for path, block in blocks:
            try:
                file_path = os.path.join(base_dir, path.strip())
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(block)
                created.append(file_path)
            except Exception as e:
                errors.append(f"{path.strip()} -> {e}")
        return {"created_files": created, "errors": errors}
