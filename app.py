from flask import Flask, render_template, request
import anthropic
from datetime import date
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
client = anthropic.Anthropic()

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "pdf"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_site_report(worker_input, site_name):
    today = date.today().strftime("%d/%m/%Y")
    
    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        system=f"""You are a construction site report assistant.
Convert the worker's description into a formal site report.
You MUST always include every section below, in this exact order, with these exact headers.
Never skip a section. Never add extra sections.

DATE: {today}
SITE: {site_name if site_name else "[extract from input or write Not specified]"}
WEATHER: [extract weather from input — if not mentioned write Not recorded]
ACTIVITIES COMPLETED:
- [bullet point list of completed activities]
ISSUES RAISED:
- [bullet point list of issues — if none write None reported]
NEXT DAY PLAN:
- [bullet point list of planned activities]
REPORT COMPILED BY: AI Site Assistant

Return only the report. No introduction. No closing remarks. No extra text.""",
        messages=[
            {"role": "user", "content": f"Convert this to a site report: {worker_input}"}
        ]
    )
    
    return message.content[0].text

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    worker_input = request.form["worker_input"]
    site_name = request.form["site_name"]
    
    upload_message = None
    uploaded_filename = None

    if "site_photo" in request.files:
        file = request.files["site_photo"]
        
        if file.filename != "":
            if not allowed_file(file.filename):
                upload_message = "File type not allowed. Please upload a PNG, JPG, GIF or PDF."
            else:
                file.seek(0, os.SEEK_END)
                file_size = file.tell()
                file.seek(0)
                
                if file_size > MAX_FILE_SIZE:
                    upload_message = "File too large. Maximum size is 5MB."
                else:
                    uploaded_filename = file.filename
                    save_path = os.path.join(UPLOAD_FOLDER, uploaded_filename)
                    file.save(save_path)
                    upload_message = f"File uploaded successfully: {uploaded_filename}"

    report = generate_site_report(worker_input, site_name)
    
    return render_template("index.html", 
                         report=report, 
                         worker_input=worker_input, 
                         site_name=site_name,
                         upload_message=upload_message,
                         uploaded_filename=uploaded_filename)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)