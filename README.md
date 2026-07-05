# Site Report Generator

**Turn a worker's spoken or typed description of their day into a professional site report in seconds.**

Site managers and operatives spend time at the end of every shift filling in paper or PDF site reports — often from memory, in a van, on a phone. This tool eliminates that friction. A worker describes their day in plain English (or speaks it), uploads an optional site photo, and receives a complete, consistently formatted report ready to print or save as PDF.

---

## The Problem It Solves

Site reports are a contractual and operational necessity — but they are slow to produce, inconsistently formatted, and often incomplete when written by hand after a long shift. Missing information, vague entries, and inconsistent section headings create problems for QS teams, site managers, and project records.

This tool enforces a fixed 16-section report structure every time, extracts only what the worker actually reported (no invented observations), and produces a print-ready A4 document in under 10 seconds.

---

## Who Uses It

- **Site operatives** — describe their day by voice or text at the end of a shift
- **Site managers** — review and print structured daily records without chasing workers for information
- **QS and commercial teams** — consistent format makes cross-referencing with programmes and contract records straightforward

---

## What It Produces

Every report contains the same 16 sections:

| Section | Source |
|---|---|
| Date | Auto-populated |
| Site / Project | Extracted from worker description |
| Weather | Worker description only |
| Workforce | Trades or numbers mentioned |
| Activities Completed | Confirmed completed work only |
| Materials Delivered / Used | Materials used today |
| Materials Required / Ordered | Materials needed for upcoming work |
| Plant & Equipment Used | Machinery mentioned by the worker |
| Quality Observations | Only what the worker explicitly states |
| Safety Observations | PPE, hazards, incidents, near misses |
| Issues Raised | Delays, defects, access problems, shortages |
| Requests / Actions Required | Procurement needs, actions needed from others |
| Next Day Plan | Tomorrow's planned activities |
| Further Details | Anything not captured above |
| Report Compiled By | AI Site Assistant |
| Site Photo Observations | Claude Vision analysis of uploaded photo |

**Key principle: the worker's description is the primary source of truth. If something is not reported, the field reads "Not reported" — the AI never invents observations or assumptions.**

---

## Example

**Worker input:**

> "Site is the Victory project in Manchester. Weather is warm and clear today. We continued external works around the apartment buildings. The wheeled excavator was used to level and clear parts of the ground. We require a delivery of 150 concrete blocks, 100 bags of cement, 2 tonnes of sand and gravel. No accidents reported today. Tomorrow we plan to complete site clearance and begin paving works."

**Generated report (selected sections):**

```
DATE:                    04/07/2026
SITE:                    Manchester
PROJECT:                 Victory
WEATHER:                 Warm and clear

ACTIVITIES COMPLETED:
- Continued external works around apartment buildings
- Levelled and cleared ground using wheeled excavator

MATERIALS REQUIRED / ORDERED:
- 150 concrete blocks
- 100 bags of cement
- 2 tonnes of sand and gravel

SAFETY OBSERVATIONS:
No accidents or injuries reported

NEXT DAY PLAN:
- Complete site clearance
- Begin paving works around building

REPORT COMPILED BY:
AI Site Assistant
```

---

## Features

- **Voice input** — worker speaks their description using the browser's built-in speech recognition (no app or plugin required); text input available as alternative
- **Photo upload with AI analysis** — upload a site photo and Claude Vision analyses it, cross-referencing with the worker's description to add a Site Photo Observations section
- **Print-ready output** — formatted for A4, with the site photo printed at the end of the report
- **Construction relevance check** — rejects unrelated input with a clear message
- **Original transcript option** — worker can choose whether to include their raw spoken transcript in the report

---

## Technology

- Python / Flask
- Anthropic Claude API with Vision (claude-haiku-4-5-20251001)
- Web Speech API (voice input, no third-party library)
- Jinja2 templates
- CSS Grid — two-panel responsive layout
- python-dotenv

---

## How to Run

```bash
# 1. Clone the repo
git clone https://github.com/Mehdi-ke/site-report-app
cd site-report-app

# 2. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate  # Mac/Linux

# 3. Install dependencies
pip install flask anthropic python-dotenv gunicorn

# 4. Add your API key
# Create a .env file in the project root:
ANTHROPIC_API_KEY=your-key-here

# 5. Run the app
python app.py
```

Open your browser at `http://127.0.0.1:5000`

---

## File Upload Notes

- Accepts PNG, JPG, GIF up to 5MB
- Images are processed in memory — no files are stored on the server
