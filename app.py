from flask import Flask, render_template, request
import anthropic
from datetime import date
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
client = anthropic.Anthropic()

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
    report = generate_site_report(worker_input, site_name)
    return render_template("index.html", report=report, worker_input=worker_input, site_name=site_name)

if __name__ == "__main__":
    port = int(__import__('os').environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)