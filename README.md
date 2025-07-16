# Fitfinder LLM API

Fitfinder-LLM-API is a Flask-based application that evaluates the compatibility between resumes and job descriptions using a locally hosted large language model. It operates entirely offline via Ollama and supports two key features: compatibility scoring and resume insights.

## Features

- Accepts a resume in PDF format and a job description via POST request.
- Supports two task modes:
  - `compatibility`: Returns a compatibility score from 0–100%. A score of 70% or higher indicates a match.
  - `insights`: Provides a summary of the strengths and weaknesses of the resume relative to the job description.
- Powered by the `llama3:instruct` model running locally through Ollama.
- API access is protected via a configurable API key.

## Installation

### Clone the Repository

```bash
git clone https://github.com/chaymabh/Fitfinder-LLM-API.git
cd Fitfinder-LLM-API
```

### Python Environment Setup

- Python 3.8+ is required.
- It is recommended to use a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

- Install dependencies:

```bash
pip install -r requirements.txt
```

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## Testing

The `test.py` script sends sample requests to both task endpoints:

```bash
python test.py
```

Expected sample output:

```
Testing Compatibility Task...
Task: compatibility
Response Code: 200
Response JSON: {'status': 'success', 'compatibility_score': '85.00%', 'meets_criteria': 'yes'}
--------------------------------------------------
Testing Insights Task...
Task: insights
Response Code: 200
Response JSON: {'status': 'success', ...}
```
