# import os
# import subprocess
# from typing import Type, Dict, Any
# from pydantic import BaseModel, Field
# from crewai.tools import BaseTool

# class ProjectInitInput(BaseModel):
#     project_name: str
#     base_dir: str = Field(".", description="Directory to initialize the project in")

# class ProjectInitTool(BaseTool):
#     name: str = "ProjectInitTool"  # ✅ Must include type annotation
#     description: str = "Installs tools and clones project template; returns absolute project path"
#     args_schema: Type[BaseModel] = ProjectInitInput

#     def _run(self, project_name: str, base_dir: str = ".") -> Dict[str, Any]:
#         abs_base = os.path.abspath(base_dir)
#         errors = []

#         def run_cmd(cmd: str):
#             result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
#             if result.returncode != 0:
#                 errors.append(f"{cmd} failed: {result.stderr.strip()}")

#         run_cmd("wget -qO- https://astral.sh/uv/install.sh | sh")
#         run_cmd("uv tool install crewai")
#         clone_cmd = f"git clone https://github.com/mahadrehmann/crewai-folder-layout.git {project_name}"
#         run_cmd(clone_cmd)

#         project_path = os.path.join(abs_base, project_name)
#         success = len(errors) == 0
#         return {"project_path": project_path, "success": success, "errors": errors}

import os
import shutil
import subprocess
from typing import Type, Dict, Any
from pydantic import BaseModel, Field
from crewai.tools import BaseTool

class ProjectInitInput(BaseModel):
    project_name: str
    base_dir: str = Field(".", description="Base directory to create the project in")

class ProjectInitTool(BaseTool):
    name: str = "ProjectInitTool"
    description: str = (
        "Installs CLI tools, clones the project template, "
        "removes its .git folder, and returns the absolute project path"
    )
    args_schema: Type[BaseModel] = ProjectInitInput

    def _run(self, project_name: str, base_dir: str = ".") -> Dict[str, Any]:
        abs_base = os.path.abspath(base_dir)
        errors = []

        def run_cmd(cmd: str):
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode != 0:
                errors.append(f"{cmd} failed: {result.stderr.strip() or result.stdout.strip()}")

        # 1. Install uv
        run_cmd("wget -qO- https://astral.sh/uv/install.sh | sh")
        # 2. Install crewai CLI
        run_cmd("uv tool install crewai")
        # 3. Clone the template repo
        clone_cmd = (
            f"git clone https://github.com/mahadrehmann/crewai-folder-layout.git "
            f"{project_name}"
        )
        run_cmd(clone_cmd)

        # 4. Remove .git folder, if it exists
        project_path = os.path.join(abs_base, project_name)
        git_dir = os.path.join(project_path, ".git")
        if os.path.isdir(git_dir):
            try:
                shutil.rmtree(git_dir, ignore_errors=False)
            except Exception as e:
                errors.append(f"Failed to delete {git_dir}: {e}")

        success = len(errors) == 0
        return {
            "project_path": project_path,
            "success": success,
            "errors": errors,
        }
