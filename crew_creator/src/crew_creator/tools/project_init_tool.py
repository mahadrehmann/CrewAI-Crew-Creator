import os
import subprocess
from typing import Type, Dict, Any
from pydantic import BaseModel, Field
from crewai.tools import BaseTool

class ProjectInitInput(BaseModel):
    project_name: str
    base_dir: str = Field(".", description="Directory to initialize the project in")

class ProjectInitTool(BaseTool):
    name: str = "ProjectInitTool"  # ✅ Must include type annotation
    description: str = "Installs tools and clones project template; returns absolute project path"
    args_schema: Type[BaseModel] = ProjectInitInput

    def _run(self, project_name: str, base_dir: str = ".") -> Dict[str, Any]:
        abs_base = os.path.abspath(base_dir)
        errors = []

        def run_cmd(cmd: str):
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode != 0:
                errors.append(f"{cmd} failed: {result.stderr.strip()}")

        run_cmd("wget -qO- https://astral.sh/uv/install.sh | sh")
        run_cmd("uv tool install crewai")
        clone_cmd = f"git clone https://github.com/mahadrehmann/crewai-folder-layout.git {project_name}"
        run_cmd(clone_cmd)

        project_path = os.path.join(abs_base, project_name)
        success = len(errors) == 0
        return {"project_path": project_path, "success": success, "errors": errors}
