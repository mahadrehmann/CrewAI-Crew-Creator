from typing import Type, Any, Dict
from pydantic import BaseModel, Field
from crewai.tools import BaseTool
import subprocess

class ShellInput(BaseModel):
    cmd: str = Field(..., description="Shell command to execute")

class ShellTool(BaseTool):
    name: str = "ShellTool"
    description: str = "Execute shell commands in the environment"
    args_schema: Type[BaseModel] = ShellInput

    def _run(self, cmd: str) -> Dict[str, Any]:
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
            return {"stdout": result.stdout.strip(), "stderr": result.stderr.strip(), "returncode": result.returncode}
        except subprocess.CalledProcessError as e:
            return {"stdout": e.stdout.strip(), "stderr": e.stderr.strip(), "returncode": e.returncode}
