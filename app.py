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

    system_prompt = f"""You are a construction site report assistant.
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

Return only the report. No introduction. No closing remarks. No extra text."""

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

Also add this section at the end of the report:
SITE PHOTO DESCRIPTION:
[The worker has provided the above description of their day. Using both what the worker described AND what you can observe in the attached photo, write 2-3 sentences describing the site photo in a construction context. Focus on what the worker is highlighting — progress made, conditions on site, any issues visible, or safety observations. Connect what you see in the image to the worker's account where relevant.]"""
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