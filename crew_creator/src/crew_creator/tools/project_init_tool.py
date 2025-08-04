import os
import subprocess
import shutil
from typing import Type, Dict, Any, List
from pydantic import BaseModel, Field
from crewai.tools import BaseTool

class ProjectInitInput(BaseModel):
    project_name: str
    base_dir: str = Field(".", description="Directory in which to clone project")

class ProjectInitTool(BaseTool):
    name: str = "ProjectInitTool"
    description: str = '''
        Run the uv CLI scripts exactly, clone a template repo into the folder, 
        delete its `.git`, and return the absolute path.'''
    args_schema: Type[BaseModel] = ProjectInitInput

    def _run(self, project_name: str, base_dir: str = ".") -> Dict[str, Any]:
        abs_base = os.path.abspath(base_dir)
        errors: List[str] = []
        project_path = os.path.join(abs_base, project_name)

        def run_cmd(cmd: str):
            print(f"[ProjectInitTool] Running: {cmd}", flush=True)
            res = subprocess.run(cmd, shell=True, text=True,
                                 capture_output=True, check=False, timeout=90)
            if res.returncode != 0:
                stderr = res.stderr.strip() or res.stdout.strip()
                errors.append(f"Command failed ({cmd}): {stderr}")

        
        # 1. uv install script
        # run_cmd("wget -qO- https://astral.sh/uv/install.sh | sh")
        # 2. update shell PATH for uv tools
        #    (just in case uv bin dir needs refreshing)
        # run_cmd("uv tool update-shell")
        # 3. install crewai CLI
        # run_cmd("uv tool install crewai")
        # 4. clone scaffold from GitHub
        clone = f"git clone https://github.com/mahadrehmann/crewai-folder-layout.git \"{project_name}\""
        run_cmd(f"cd \"{abs_base}\" && {clone}")

        # 5. delete .git inside cloned folder
        gitdir = os.path.join(project_path, ".git")
        if os.path.isdir(gitdir):
            try:
                shutil.rmtree(gitdir)
            except Exception as e:
                errors.append(f"Removing .git folder failed: {e}")

        success = not errors
        return {"project_path": project_path, "success": success, "errors": errors}
