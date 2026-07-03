# Site Report Generator

A Flask web app that converts a worker's plain English description of their day into a formal, structured construction site report — instantly.

## What It Does

A worker describes their day in their own words. The app sends that description to the Anthropic Claude API with a structured output prompt, which returns a formal site report with fixed sections every time:

- **Date** — automatically populated
- **Site** — extracted from input or entered manually
- **Weather** — extracted from input
- **Activities Completed** — bullet point list
- **Issues Raised** — problems, delays, near misses
- **Next Day Plan** — tomorrow's planned activities
- **Report Compiled By** — AI Site Assistant

The report renders on screen and can be printed or saved as a PDF directly from the browser.

## Technology

- Python
- Flask
- Anthropic Claude API (claude-haiku-4-5-20251001)
- Jinja2 templates
- CSS Grid layout
- python-dotenv for secure API key management

## Key Concepts

- **Structured output prompting** — system prompt engineered to return consistent fixed-section reports every time
- **CSS Grid** — two-panel responsive layout, print-ready with media queries
- **Date injection** — today's date passed from Python into the prompt automatically

## How to Run Locally

1. Clone the repo
2. Create and activate a virtual environment:
```bash
   python -m venv venv
   venv\Scripts\activate
```
3. Install dependencies:
```bash
   pip install flask anthropic python-dotenv
```
4. Create a `.env` file with your Anthropic API key:
ANTHROPIC_API_KEY=your-key-here
5. Run the app:
```bash
   python app.py
```
6. Open your browser at `http://127.0.0.1:5000`

## Example Input

> "Sunny day on site. Groundworks team finished the drainage run on the east side. Had a near miss with a forklift near the welfare unit, reported to site manager. Tomorrow the concrete pump is booked for 7am for the pile caps on zone 2."

## Example Output
DATE: 03/07/2026
SITE: Not specified
WEATHER: Sunny
ACTIVITIES COMPLETED:

Groundworks team completed drainage run on east side
ISSUES RAISED:
Near miss incident involving forklift near welfare unit (reported to site manager)
NEXT DAY PLAN:
Concrete pump booked for 7am for pile caps on zone 2
REPORT COMPILED BY: AI Site Assistant



