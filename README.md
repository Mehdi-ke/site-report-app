# Site Report Generator

A Flask web app that converts a worker's plain English description of their day into a formal, structured construction site report — instantly. Supports photo upload with AI-powered image analysis using Claude Vision.

## What It Does

A worker describes their day in their own words and optionally attaches a site photo. The app sends both to the Anthropic Claude API, which returns a professional site report with fixed sections every time:

- **Date** — automatically populated
- **Site** — extracted from input or entered manually, properly capitalised
- **Project** — extracted from worker description
- **Weather** — extracted from worker description only
- **Workforce** — trades or numbers mentioned
- **Activities Completed** — confirmed completed work only
- **Materials Delivered / Used** — materials used today
- **Materials Required / Ordered** — materials requested for upcoming work
- **Plant & Equipment Used** — machinery mentioned by the worker
- **Quality Observations** — only what the worker explicitly states
- **Safety Observations** — PPE, hazards, incidents, near misses
- **Issues Raised** — delays, defects, access problems, shortages
- **Requests / Actions Required** — procurement needs, actions needed from others
- **Next Day Plan** — tomorrow's planned activities
- **Further Details** — anything not captured above
- **Report Compiled By** — AI Site Assistant
- **Site Photo Observations** — AI analysis of the attached photo, cross-referenced with the worker's description

The report renders on screen with the site photo displayed below, and can be printed or saved as A4 PDF directly from the browser.

## Key Design Principles

- **Worker's description is the primary source of truth** — the image is supplementary evidence only
- **No assumptions** — if information is not stated, the report writes "Not reported" rather than guessing
- **No invented quality statements** — Claude never writes "Work completed to standard" unless the worker explicitly says so
- **Materials distinguished** — used/delivered today vs required/ordered for future work are kept separate
- **Issues vs Requests separated** — actual problems kept distinct from procurement requests
- **Proper capitalisation** — site names and place names are correctly formatted

## Technology

- Python
- Flask
- Anthropic Claude API (claude-haiku-4-5-20251001) with Vision
- Jinja2 templates
- CSS Grid layout — two panel responsive design
- Print stylesheet — A4 print-ready with site photo at end of report
- python-dotenv for secure API key management
- Base64 image encoding — no file storage required

## How to Run Locally

1. Clone the repo
2. Create and activate a virtual environment:
```bash
   python -m venv venv
   venv\Scripts\activate
```
3. Install dependencies:
```bash
   pip install flask anthropic python-dotenv gunicorn
```
4. Create a `.env` file with your Anthropic API key:
   ANTHROPIC_API_KEY=your-key-here
5. Run the app:
```bash
   python app.py
```
6. Open your browser at `http://127.0.0.1:5000`

## Example Input

> "Site is the Victory project in Manchester. Weather is warm and clear today. We continued external works around the apartment buildings. The wheeled excavator was used to level and clear parts of the ground. We require a delivery of 150 concrete blocks, 100 bags of cement, 2 tonnes of sand and gravel. No accidents reported today. Tomorrow we plan to complete site clearance and begin paving works."

## Example Output Sections
DATE: 04/07/2026
SITE: Manchester
PROJECT: Victory
WEATHER: Warm and clear
ACTIVITIES COMPLETED:

Continued external works around apartment buildings
Levelled and cleared ground using wheeled excavator
MATERIALS REQUIRED / ORDERED:
150 concrete blocks
100 bags of cement
2 tonnes of sand and gravel
SAFETY OBSERVATIONS:
No accidents or injuries reported
NEXT DAY PLAN:
Complete site clearance
Begin paving works around building
REPORT COMPILED BY:
AI Site Assistant

## File Upload & Vision

- Accepts PNG, JPG, GIF up to 5MB
- Image is read directly into memory — no server-side file storage required
- Claude Vision analyses the image and cross-references it with the worker's description
- Image displays below the report on screen and in print

## Deployment

Deployed on Railway with gunicorn. Environment variables managed via Railway's Variables panel.
