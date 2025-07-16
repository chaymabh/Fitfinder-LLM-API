import requests

API_URL = "http://127.0.0.1:5000/upload_resume"  

JOB_DESCRIPTION = """Job Overview:
We are looking for a skilled Data Scientist to join our team. The ideal candidate will have a strong foundation in machine learning, AI, and data science, with experience in developing, deploying, and optimizing AI models. You will be responsible for fine-tuning and deploying models, implementing advanced algorithms, and collaborating closely with cross-functional teams to drive impactful business outcomes.

Key Responsibilities:

Design and implement AI models, including graph-augmented retrieval systems, anomaly detection, and predictive models.
Fine-tune large language models (LLMs) using TensorFlow and PyTorch, focusing on project-specific tasks.
Work with graph neural networks (GNNs), knowledge graphs, and advanced NLP techniques to enhance AI model performance.
Develop machine learning models using a variety of tools and frameworks (e.g., TensorFlow, PyTorch, Keras, and Hugging Face).
Deploy machine learning models as APIs using Flask and FastAPI for real-time predictions and seamless integration into web applications.
Implement advanced web scraping solutions using BeautifulSoup for collecting and preprocessing large datasets.
Optimize AI-driven solutions for cloud deployment, leveraging platforms like AWS and OVH to accelerate training and inference.
Collaborate with engineering and data science teams to integrate AI solutions into existing systems.
Build interactive dashboards and visualizations to communicate data insights effectively.
Research and implement state-of-the-art methods for feature extraction, anomaly detection, and data preprocessing.
Conduct thorough data analysis to uncover insights and enhance decision-making processes.
Stay updated on the latest AI, machine learning, and data science trends, continuously refining your skill set.
Required Qualifications:

Master's or Bachelor's Degree in Data Science, Computer Science, or a related field.
Proven experience in machine learning, deep learning, and data science applications.
Strong proficiency in programming languages such as Python, R, Java, C++, and MATLAB.
Hands-on experience with TensorFlow, PyTorch, Keras, Hugging Face, and other ML frameworks.
Experience working with graph neural networks (GNNs) and knowledge graphs.
Solid understanding of natural language processing (NLP) techniques and tools like SpaCy, NLTK, TextBlob, and Gensim.
Proficiency in web development frameworks like Flask, FastAPI, Angular, and Node.js.
Experience with cloud platforms (AWS, OVH) for model deployment and optimization.
Knowledge of databases such as Elasticsearch, Neo4j, MongoDB, and PostgreSQL.
Ability to work in Agile and Scrum methodologies.
Strong problem-solving skills and ability to work independently or in a team.
Preferred Qualifications:

Certifications in machine learning or data science (e.g., IBM AI Analyst, Big Data Engineer, etc.).
Experience with real-time data streaming from IoT devices and sensor data analysis.
Familiarity with advanced machine learning techniques such as unsupervised learning and reinforcement learning.
Knowledge of AI-driven web scraping techniques and automation.
Soft Skills:

Strong communication skills in English, French, and Arabic.
Ability to collaborate effectively in a cross-functional team environment.
Self-motivated, with a passion for continuous learning and staying updated with the latest industry trends.
Detail-oriented and able to work on multiple projects simultaneously while meeting deadlines.
"""

PDF_PATH = "data\Resume_chayma_elbahri_Eng.pdf"  
def test_api(task):
    with open(PDF_PATH, 'rb') as file:
        
        files = {'file': file}
        data = {'job_description': JOB_DESCRIPTION, 'task': task}

        response = requests.post(API_URL, files=files, data=data)

        print(f"Task: {task}")
        print("Response Code:", response.status_code)
        print("Response JSON:", response.json())
        print("-" * 50)

if __name__ == "__main__":
    print("Testing Compatibility Task...")
    test_api("compatibility")

    print("Testing Insights Task...")
    test_api("insights")
