import requests
import json
from langchain_core.messages.human import HumanMessage

class OllamaJSONModel:
    def __init__(self, temperature=0, model="llama3:instruct"):
        self.headers = {"Content-Type": "application/json"}
        self.model_endpoint = "http://localhost:11434/api/generate"
        self.temperature = temperature
        self.model = model 
        self.top_p = 0.85
        self.top_k = 50
        self.num_ctx = 8192
        self.repeat_penalty = 0.9
        self.num_predict = 4096          
        self.seed = None

    def invoke(self, messages):
        system = messages[0]["content"]
        user = messages[1]["content"]

        payload = {
            "model": self.model,
            "prompt": user,
            "format": "json",
            "system": system,
            "stream": False,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "top_k": self.top_k,
            "num_ctx": self.num_ctx,
            "num_predict": self.num_predict,          
            "repeat_penalty": self.repeat_penalty,
        }
        
        if self.seed is not None:
            payload["seed"] = self.seed

        try:
            request_response = requests.post(
                self.model_endpoint, 
                headers=self.headers, 
                data=json.dumps(payload)
            )
            request_response_json = request_response.json()
            response = json.loads(request_response_json['response'])
            response = json.dumps(response)
            response_formatted = HumanMessage(content=response)
            return response_formatted

        except requests.RequestException as e:
            response = {"error": f"Error in invoking model! {str(e)}"}
            response_formatted = HumanMessage(content=response)
            return response_formatted

class OllamaModel:
    def __init__(self, temperature=0, model="llama3:instruct", top_p=0.2, top_k=10, num_ctx=8192, frequency_penalty=0.2, seed=None):
        self.headers = {"Content-Type": "application/json"}
        self.model_endpoint = "http://localhost:11434/api/generate"
        self.temperature = temperature
        self.model = model
        self.top_p = top_p
        self.top_k = top_k
        self.num_ctx = num_ctx
        self.frequency_penalty = frequency_penalty
        self.seed = seed

    def invoke(self, messages):
        system = messages[0]["content"]
        user = messages[1]["content"]

        payload = {
            "model": self.model,
            "prompt": user,
            "system": system,
            "stream": False,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "top_k": self.top_k,
            "num_ctx": self.num_ctx,
            "frequency_penalty": self.frequency_penalty,
        }
        
        if self.seed is not None:
            payload["seed"] = self.seed

        try:
            request_response = requests.post(
                self.model_endpoint, 
                headers=self.headers, 
                data=json.dumps(payload)
            )
            request_response_json = request_response.json().get('response')
            response = str(request_response_json)
            response_formatted = HumanMessage(content=response)
            return response_formatted

        except requests.RequestException as e:
            response = {"error": f"Error in invoking model! {str(e)}"}
            response_formatted = HumanMessage(content=response)
            return response_formatted
        
def calculate_compatibility(resume_text, job_description):
    
    model = OllamaJSONModel(temperature=0, model="llama3:instruct")
    messages = [
        {"role": "system", "content": "You are an AI that determines whether a resume meets a job requirement. Be lenient and provide a compatibility percentage (0-100%) in JSON format with a 'percentage' field."},
        {"role": "user", "content": f"Does the following resume meet the job requirement described below? Respond with a JSON object containing a 'percentage' field (0-100) and a 'analysis' field with a brief compatibility analysis.\n\nResume: {resume_text}\n\nJob Requirement: {job_description}"}
    ]

    response = model.invoke(messages)
    try:
        result = json.loads(response.content)
        percentage = float(result.get('percentage', 0))
        if percentage < 70:
            return "no", percentage
        else:
            return "yes", percentage
    except (json.JSONDecodeError, ValueError) as e:
        return "no", 0
    
def generate_summary(resume_text, job_description_text):
   
    model = OllamaModel(temperature=0, model="llama3:instruct")
    messages = [
        {"role": "system", "content": "You are an AI that compares resumes to job descriptions and provides a strengths and weaknesses summary."},
        {"role": "user", "content": f"Given the following resume and job description, provide a brief summary of the positives and negatives:\n\nResume: {resume_text}\n\nJob Description: {job_description_text}"}
    ]

    response = model.invoke(messages)
    return response.content