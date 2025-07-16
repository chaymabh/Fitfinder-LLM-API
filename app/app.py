from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
from process.process_resume import process_resume
from model.get_insights import calculate_compatibility, generate_summary  

load_dotenv()

app = Flask(__name__)

@app.route('/upload_resume', methods=['POST'])
def upload_resume():

    api_key = request.headers.get('X-API-Key')
    if api_key != os.getenv('API_KEY'):
        return jsonify({"status": "error", "message": "Invalid or missing API key"}), 401

    if 'file' not in request.files:
        return jsonify({"status": "error", "message": "No file uploaded"}), 400
    if 'job_description' not in request.form:
        return jsonify({"status": "error", "message": "No job description provided"}), 400
    if 'task' not in request.form:
        return jsonify({"status": "error", "message": "No task specified"}), 400

    file = request.files['file']
    job_description = request.form['job_description']
    task = request.form['task'].lower()  
    try:
        cleaned_resume = process_resume(file)
        if not cleaned_resume:
            return jsonify({"status": "error", "message": "Failed to process resume"}), 500
    except Exception as e:
        return jsonify({"status": "error", "message": f"Resume processing failed: {str(e)}"}), 500

    if task == "compatibility":
        try:
            result, compatibility_score = calculate_compatibility(cleaned_resume, job_description)
            return jsonify({
                "status": "success",
                "compatibility_score": f"{compatibility_score:.2f}%",
                "meets_criteria": result
            })
        except Exception as e:
            return jsonify({"status": "error", "message": f"Compatibility calculation failed: {str(e)}"}), 500

    elif task == "insights":
        try:
            insights = generate_summary(cleaned_resume, job_description)
            return jsonify({"status": "success", "insights": insights})
        except Exception as e:
            return jsonify({"status": "error", "message": f"Insights generation failed: {str(e)}"}), 500

    else:
        return jsonify({"status": "error", "message": "Invalid task. Choose either 'compatibility' or 'insights'"}), 400

if __name__ == '__main__':
    app.run(debug=True)