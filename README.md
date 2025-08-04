# CrewAI Crew Creator

**Generate fully functional [CrewAI](https://docs.crewai.com/) multi-agent systems with just one prompt.**  
This project automates the design and creation of Crews, Agents, and Tasks for you - so you can focus on *what* you want, not *how* to implement it.

---

## 🚀 What It Does

The **CrewAI Crew Creator** is a Flask-based tool that:

- Takes a single high-level prompt and a project name from the user.
- Automatically decides:
  - Number of agents
  - Agent roles and tools
  - Required tasks
  - Logical task-agent mapping
- Generates:
  - A complete `main.py` to run the crew
  - A complete `crew.py` for the crew
  - Individual `agents.yaml` and `tasks.yaml` files
  - A zipped folder ready for download and execution

You don’t need to:
- Design agent prompts
- Figure out roles or responsibilities
- Set up a CrewAI project from scratch

Just describe your goal and we’ll create the scaffolding and logic for you.

---

## 🛠 How to Use

### 1. Run Locally

```bash
git clone https://github.com/mahadrehmann/CrewAI-Crew-Creator.git
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
cd crew_creator
python app.py
```

Visit `http://localhost:5000` in your browser.

### 2. Enter Details

- **Prompt**: Describe what you want the AI agents to achieve.
- **Project Name**: A name for your crew (used in file naming).

Hit submit, download the zip, and you're done.

---

## 💡 Example Use Case

> Prompt: "Build an AI system that performs market research on tech startups and summarizes key trends"

🧠 **What Happens Automatically:**

- 3 agents created:
  - Market Research Analyst
  - Trend Extractor
  - Report Generator
- Tasks mapped intelligently.
- Execution logic is added to `main.py`.
- Entire project zipped for you to run or edit.

---

## 📁 Project Structure (Generated)

```
<project_name>/
├── .gitignore
├── knowledge/
├── pyproject.toml
├── README.md
├── .env
└── src/
    └── <project_name>/
        ├── __init__.py
        ├── main.py
        ├── crew.py
        └── config/
            ├── agents.yaml
            └── tasks.yaml

```

---

## 📦 Technologies

- 🧠 [CrewAI](https://github.com/joaomdmoura/crewai)
- 🧰 Flask (UI & ZIP delivery)

---

## 🤖 Why This Tool?

Most CrewAI tutorials and setups ask you to:
- Design prompts for each agent manually
- Map tasks by hand
- Experiment with different agent counts

With **Crew Creator**, you skip all of that.  
Just define your goal — the tool handles the rest intelligently.

---
