# from flask import Flask, request, send_from_directory, render_template, redirect, url_for
# import os
# import shutil
# import sys
# from datetime import datetime

# # Add src directory to Python path
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

# from crew_creator.main import CrewCreator
# from crew_creator.main import run

# app = Flask(__name__)
# UPLOAD_FOLDER = "./output"
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# @app.route("/", methods=["GET", "POST"])
# def index():
#     if request.method == "POST":
#         # Get inputs from the form
#         prompt = request.form.get("prompt")
#         project_name = request.form.get("project_name")

#         # Run the crew with the inputs
#         inputs = {
#             'goal': prompt,
#             'syntax': '',  # Add syntax if needed
#             'base_dir': app.config['UPLOAD_FOLDER'],
#             'project_name': project_name,
#             'current_year': str(datetime.now().year)
#         }
#         try:
#             run(inputs=inputs)
#         except Exception as e:
#             return f"Error: {e}"

#         # Redirect to download page
#         return redirect(url_for("download", project_name=project_name))

#     return render_template("index.html")

# @app.route("/download/<project_name>")
# def download(project_name):
#     zip_filename = f"{project_name}.zip"
#     zip_path = os.path.join(app.config['UPLOAD_FOLDER'], zip_filename)

#     if os.path.exists(zip_path):
#         print(f"Download triggered for {zip_path}")
#         return send_from_directory(
#             directory=app.config['UPLOAD_FOLDER'],
#             path=zip_filename,
#             as_attachment=True,
#             download_name=zip_filename
#         )

#     return "File not found", 404

# @app.route("/cleanup/<project_name>")
# def cleanup(project_name):
#     zip_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{project_name}.zip")
#     if os.path.exists(zip_path):
#         os.remove(zip_path)
#     return redirect(url_for("index"))

# if __name__ == "__main__":
#     os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
#     app.run(debug=True)

# filepath: /home/mahad/Desktop/Agentic/CrewAI-Creator/crew_creator/app.py

from flask import (
    Flask,
    request,
    send_from_directory,
    render_template,
    redirect,
    url_for,
)
import os
import shutil
import sys
from datetime import datetime

# If Python NOS (e.g. waitress, gunicorn) performance matters, consider using pathlib.
UPLOAD_FOLDER = "./output"

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Make sure src (crewai agent code) is importable
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

from crew_creator.main import run  # noqa: E402

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        prompt = request.form.get("prompt")
        project_name = request.form.get("project_name")

        inputs = {
            'goal': prompt,
            'syntax': '',
            'base_dir': app.config['UPLOAD_FOLDER'],
            'project_name': project_name,
            'current_year': str(datetime.now().year)
        }

        try:
            run(inputs=inputs)
        except Exception as e:
            return render_template("index.html", error=str(e))

        return redirect(url_for("download", project_name=project_name))

    return render_template("index.html")

@app.route("/download/<project_name>")
def download(project_name):
    zip_filename = f"{project_name}.zip"
    zip_path = os.path.join(app.config['UPLOAD_FOLDER'], zip_filename)

    project_dir = os.path.join(app.config['UPLOAD_FOLDER'], project_name)

    if not os.path.exists(zip_path):
        return "File not found", 404

    response = send_from_directory(
        directory=app.config['UPLOAD_FOLDER'],
        path=zip_filename,
        as_attachment=True,
        download_name=zip_filename,
        mimetype="application/zip",
    )

    def cleanup():
        try:
            os.remove(zip_path)
        except Exception:
            pass

        if os.path.isdir(project_dir):
            try:
                shutil.rmtree(project_dir)
            except Exception:
                pass

    response.call_on_close(cleanup)
    return response

if __name__ == "__main__":
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
