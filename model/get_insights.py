import requests
import json
from typing import Dict, Tuple, Optional
from langchain_core.messages.human import HumanMessage

class base_model:
    DEFAULT_CONFIG = {
        "model_endpoint": "http://localhost:11434/api/generate",
        "headers": {"Content-Type": "application/json"},
        "temperature": 0.0,
        "model": "llama3:instruct",
        "top_p": 0.85,
        "top_k": 50,
        "num_ctx": 8192,
        "num_predict": 4096,
        "repeat_penalty": 1.0,
        "frequency_penalty": 0.2,
        "seed": None
    }

    def __init__(self, **kwargs):
        self.config = self.DEFAULT_CONFIG.copy()
        self.config.update(kwargs)
        self.model_endpoint = self.config["model_endpoint"]
        self.headers = self.config["headers"]

    def _prepare_payload(self, messages: list, format_json: bool = False) -> Dict:
        if len(messages) < 2 or messages[0]["role"] != "system" or messages[1]["role"] != "user":
            raise ValueError("Expected at least two messages with 'system' and 'user' roles.")

        payload = {
            "model": self.config["model"],
            "prompt": messages[1]["content"],
            "system": messages[0]["content"],
            "stream": False,
            "temperature": self.config["temperature"],
            "top_p": self.config["top_p"],
            "top_k": self.config["top_k"],
            "num_ctx": self.config["num_ctx"],
        }

        if format_json:
            payload["format"] = "json"
            payload["num_predict"] = self.config["num_predict"]
            payload["repeat_penalty"] = self.config["repeat_penalty"]
        else:
            payload["frequency_penalty"] = self.config["frequency_penalty"]

        if self.config["seed"] is not None:
            payload["seed"] = self.config["seed"]

        return payload

    def invoke(self, messages: list, format_json: bool = False) -> HumanMessage:
        """Invoke the Ollama model with the provided messages."""
        try:
            payload = self._prepare_payload(messages, format_json)
            response = requests.post(
                self.model_endpoint,
                headers=self.headers,
                data=json.dumps(payload),
                timeout=30 
            )
            response.raise_for_status()  
            response_data = response.json()

            if format_json:
                result = json.loads(response_data.get("response", "{}"))
                content = json.dumps(result)
            else:
                content = str(response_data.get("response", ""))

            return HumanMessage(content=content)

        except (requests.RequestException, json.JSONDecodeError) as e:
            error_message = {"error": f"Failed to invoke model: {str(e)}"}
            return HumanMessage(content=json.dumps(error_message))

class llama_json_model(base_model):
   
    def invoke(self, messages: list) -> HumanMessage:
        return super().invoke(messages, format_json=True)

class llama_model(base_model):
    
    def invoke(self, messages: list) -> HumanMessage:
        return super().invoke(messages, format_json=False)

def calculate_compatibility(resume_text: str, job_description: str) -> Tuple[str, float]:
    
    model = llama_json_model()
    messages = [
        {
            "role": "system",
            "content": "You are an AI that evaluates resume compatibility with job requirements. "
                      "Provide a compatibility percentage (0-100%) in JSON format with 'percentage' "
                      "and 'analysis' fields. Be lenient in your evaluation."
        },
        {
            "role": "user",
            "content": f"Evaluate the compatibility of the following resume with the job requirements. "
                      f"Respond with a JSON object containing 'percentage' (0-100) and 'analysis' fields.\n\n"
                      f"Resume: {resume_text}\n\nJob Requirement: {job_description}"
        }
    ]

    response = model.invoke(messages)
    try:
        result = json.loads(response.content)
        percentage = float(result.get("percentage", 0))
        return ("yes" if percentage >= 70 else "no", percentage)
    except (json.JSONDecodeError, ValueError) as e:
        return "no", 0.0

def generate_summary(resume_text: str, job_description_text: str) -> str:
    
    model = llama_model()
    messages = [
        {
            "role": "system",
            "content": "You are an AI that compares resumes to job descriptions and provides a "
                      "summary of strengths and weaknesses."
        },
        {
            "role": "user",
            "content": f"Provide a concise summary of the strengths and weaknesses based on the "
                      f"following resume and job description:\n\nResume: {resume_text}\n\n"
                      f"Job Description: {job_description_text}"
        }
    ]

    response = model.invoke(messages)
    return response.content