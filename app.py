from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os

from utils.pdf_parser import extract_text_from_pdf
from utils.skill_extractor import extract_skills
from utils.matcher import match_jobs


app = Flask(__name__)



# CONFIGURATION


UPLOAD_FOLDER = "uploads"

ALLOWED_EXTENSIONS = {"pdf"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024


os.makedirs(UPLOAD_FOLDER, exist_ok=True)



# CHECK FILE EXTENSION


def allowed_file(filename):

    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


# HOME PAGE

@app.route("/")
def home():

    return render_template("index.html")



# RESUME ANALYSIS

@app.route("/analyze", methods=["POST"])
def analyze():

    
    # Check file

    if "resume" not in request.files:

        return "No resume uploaded!"


    resume = request.files["resume"]


    
    # Check filename
    

    if resume.filename == "":

        return "Please select a resume!"


    
    # Check PDF
    

    if not allowed_file(resume.filename):

        return "Only PDF files are allowed!"


    
    # Secure filename


    filename = secure_filename(resume.filename)


    file_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        filename
    )


    
    # Save resume
    

    resume.save(file_path)


    
    # Extract PDF text


    resume_text = extract_text_from_pdf(file_path)


    
    # Check extracted text
    

    if not resume_text.strip():

        return """
        Could not extract text from this PDF.

        Please upload a text-based PDF resume.
        """


    
    # Extract skills
    

    skills = extract_skills(resume_text)


    
    # Match jobs
    

    job_results = match_jobs(
        resume_text,
        skills
    )


    
    # Calculate ATS-style score
    

    if job_results:

        overall_score = round(
            sum(job["match_score"] for job in job_results)
            / len(job_results)
        )

    else:

        overall_score = 0


    # Best role
    

    if job_results:

        best_role = job_results[0]["title"]

        best_match = job_results[0]["match_score"]

    else:

        best_role = "No matching role found"

        best_match = 0


    
    # Render results  


    return render_template(
        "result.html",

        filename=filename,

        skills=skills,

        jobs=job_results,

        overall_score=overall_score,

        best_role=best_role,

        best_match=best_match,

        resume_text=resume_text
    )


# RUN APPLICATION

if __name__ == "__main__":

    app.run(debug=True)