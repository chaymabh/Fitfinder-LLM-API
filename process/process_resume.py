import pdfplumber
import re
from io import BytesIO

def clean_extracted_text(text):
    
    if not text:
        return ""

    text = re.sub(r'\n{2,}', '\n', text) 
    text = re.sub(r'\s{2,}', ' ', text)  
    text = text.strip()
    text = re.sub(r'(\w)-\s+(\w)', r'\1\2', text)  
    text = re.sub(r'(\w)\s*\n\s*(\w)', r'\1 \2', text) 
    text = re.sub(r'(?<=\n)([A-Z\s]+)(?=\n)', r'\n\n\1\n', text)  
    text = re.sub(r'•\s+', '- ', text)  
    text = re.sub(r'●\s+', '- ', text)  
    text = re.sub(r'[^\x20-\x7E]', '', text)  

    return text

def process_resume(file):
    
    try:
        
        with pdfplumber.open(BytesIO(file.read())) as pdf:
            extracted_text = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())

        cleaned_resume = clean_extracted_text(extracted_text)

        return cleaned_resume

    except Exception as e:
        print(f"Error processing resume: {e}")
        return None
