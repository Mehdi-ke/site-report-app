from flask import Flask, render_template, request
import anthropic
from datetime import date
from dotenv import load_dotenv
import os
import base64

load_dotenv()

app = Flask(__name__)
client = anthropic.Anthropic()

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
MAX_FILE_SIZE = 5 * 1024 * 1024

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def get_media_type(filename):
    ext = filename.rsplit(".", 1)[1].lower()
    media_types = {
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
        "png": "image/png",
        "gif": "image/gif"
    }
    return media_types.get(ext, "image/jpeg")

def generate_site_report(worker_input, site_name, image_data=None, media_type=None):
    today = date.today().strftime("%d/%m/%Y")

    system_prompt = f"""You are a construction site report assistant for UK construction projects.
Convert the worker's description into a formal site report.
You MUST include every section below, in this exact order, with these exact headers.
Never skip a section. Never add extra sections.

DATE: {today}

SITE: {site_name if site_name else "[Extract from input or write Not specified]"}

PROJECT:
[Extract project name or description from input. If not mentioned write "Not specified".]

WEATHER:
[Extract weather from the worker's description only. If not mentioned write "Not recorded".]

WORKFORCE:
[Number of workers or trades mentioned. Otherwise write "Not reported".]

ACTIVITIES COMPLETED:
- [Bullet point list of completed work. Include all significant tasks mentioned.]

MATERIALS DELIVERED / USED:
- [List materials mentioned. If none mentioned write "None reported".]

PLANT & EQUIPMENT USED:
- [List machinery, tools or equipment mentioned. If none mentioned write "None reported".]

QUALITY OBSERVATIONS:
- [Record inspections, testing, completed standards or quality concerns mentioned. If none mentioned write "None reported".]

SAFETY OBSERVATIONS:
- [PPE observations, hazards identified, incidents or near misses, temporary controls or safety actions mentioned. If none mentioned write "None reported".]

ISSUES RAISED:
- [List delays, access issues, shortages, defects, weather impacts, client requests or other problems. If none mentioned write "None reported".]

NEXT DAY PLAN:
- [Bullet point list of planned work for the following day. If no future work is mentioned write "Not reported".]

FURTHER DETAILS:
[Anything not captured in other categories. If nothing further write "None".]

REPORT COMPILED BY:
AI Site Assistant

Return only the completed report. No introduction. No closing remarks. No extra text."""

    if image_data:
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": media_type,
                            "data": image_data
                        }
                    },
                    {
                        "type": "text",
                        "text": f"""Convert this to a site report: {worker_input}

At the end of the report, after REPORT COMPILED BY, add this section:

SITE PHOTO OBSERVATIONS:
[Write 2-4 factual sentences describing what is visible in the image. Base the description only on visible evidence and the worker's description. Focus on: construction progress, site conditions, materials, equipment, work areas, safety observations, visible issues or defects. If the worker's description and the image support each other, mention the relationship. Do not speculate about work that cannot be seen. Do not infer weather from the image. Do not identify people. Do not guess activities that are not clearly visible.]"""
                    }
                ]
            }
        ]
    else:
        messages = [
            {
                "role": "user",
                "content": f"Convert this to a site report: {worker_input}"
            }
        ]

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        system=system_prompt,
        messages=messages
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
    image_data = None
    media_type = None

    if "site_photo" in request.files:
        file = request.files["site_photo"]

        if file.filename != "":
            if not allowed_file(file.filename):
                upload_message = "File type not allowed. Please upload a PNG, JPG or GIF."
            else:
                file_bytes = file.read()

                if len(file_bytes) > MAX_FILE_SIZE:
                    upload_message = "File too large. Maximum size is 5MB."
                else:
                    image_data = base64.standard_b64encode(file_bytes).decode("utf-8")
                    media_type = get_media_type(file.filename)
                    upload_message = f"Photo uploaded and analysed: {file.filename}"

    report = generate_site_report(worker_input, site_name, image_data, media_type)

    return render_template("index.html",
                         report=report,
                         worker_input=worker_input,
                         site_name=site_name,
                         upload_message=upload_message,
                         image_data=image_data,
                         media_type=media_type)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)