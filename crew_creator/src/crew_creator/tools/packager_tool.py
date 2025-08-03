# # src/<project_name>/tools/packager_tool.py
# import os
# import zipfile
# from typing import Type, Any, Dict, List
# from pydantic import BaseModel, Field
# from crewai.tools import BaseTool

# class PackagerInput(BaseModel):
#     project_path: str = Field(..., description="Absolute path to project folder")
#     zip_name: str = Field("crewai_project", description="Base name for the .zip output file")
#     base_dir: str = Field(".", description="Working directory for zip output (relative or absolute)")

# class ZipTool(BaseTool):
#     name: str = "ZipTool"
#     description: str = "Compress a project folder into a zip file and return the zip path"
#     args_schema: Type[BaseModel] = PackagerInput

#     def _run(self, project_path: str, zip_name: str = "crewai_project", base_dir: str = ".") -> Dict[str, Any]:
#         abs_project = os.path.abspath(project_path)
#         abs_base = os.path.abspath(base_dir)
#         zip_path = os.path.join(abs_base, zip_name.rstrip(".zip") + ".zip")
#         errors: List[str] = []

#         if not os.path.isdir(abs_project):
#             errors.append(f"Project path does not exist: {abs_project}")
#         else:
#             try:
#                 with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED, allowZip64=True) as zf:
#                     for root, _, files in os.walk(abs_project):
#                         for fn in files:
#                             abs_f = os.path.join(root, fn)
#                             rel_f = os.path.relpath(abs_f, os.path.dirname(abs_project))
#                             zf.write(abs_f, arcname=rel_f)
#                 created = [zip_path]
#             except Exception as e:
#                 errors.append(f"Zip error: {e}")
#                 created = []

#         success = (len(errors) == 0 and len(created) > 0)
#         return {"zip_path": zip_path if success else "", "created_files": created, "errors": errors}

# src/<your_project>/tools/packager_tool.py

import os, zipfile
from typing import Type, Any, Dict, List
from pydantic import BaseModel, Field
from crewai.tools import BaseTool

class PackagerInput(BaseModel):
    project_path: str
    zip_name: str | None = Field(
        None,
        description="Optional: base filename for the zip (if None, use project folder name)"
    )
    base_dir: str = Field(".", description="Directory to create the zip inside")

class ZipTool(BaseTool):
    name: str = "ZipTool"
    description: str = "Compress project into zip; filename defaults to project directory."
    args_schema: Type[BaseModel] = PackagerInput

    def _run(self, project_path: str, zip_name: str | None = None, base_dir: str = ".") -> Dict[str, Any]:
        abs_proj = os.path.abspath(project_path)
        abs_base = os.path.abspath(base_dir)

        # Use project directory name if zip_name not provided
        zip_base = zip_name.rstrip(".zip") if zip_name else os.path.basename(abs_proj)
        zip_path = os.path.join(abs_base, f"{zip_base}.zip")

        created_files: List[str] = []
        errors: List[str] = []

        if not os.path.isdir(abs_proj):
            errors.append(f"Project path does not exist: {abs_proj}")
        else:
            try:
                with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED, allowZip64=True) as zf:
                    src_root = os.path.dirname(abs_proj)
                    for root, dirs, files in os.walk(abs_proj):
                        for fn in files:
                            full = os.path.join(root, fn)
                            rel = os.path.relpath(full, start=src_root)
                            zf.write(full, arcname=rel)
                created_files = [zip_path]
            except Exception as e:
                errors.append(f"Zip failed: {e}")

        return {
            "zip_path": zip_path if created_files else "",
            "created_files": created_files,
            "errors": errors,
        }
