# Placement Tracker

A full-stack web app where students track their job applications in one place, see their progress on a dashboard, get AI-generated resume tips, and export their list as a PDF.

**Live demo:** [ADD-LINK-AFTER-DEPLOYMENT](https://placement-tracker-8rat.onrender.com/login)
(The free host sleeps when idle, so the first load can take 30 to 60 seconds. The AI feature may occasionally be unavailable when the Gemini free tier is busy.)

## Features

- Register, log in and log out, with hashed passwords and session-based authentication
- Add, edit the status of, and delete job applications (Applied, Shortlisted, Interview, Offer, Rejected)
- Dashboard with summary cards and a status chart
- AI resume tips for a target role and skill set, using the Google Gemini API
- Export your applications as a PDF
- Each student can only see and change their own data

## Tech stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask, REST API |
| Database | MySQL |
| Frontend | HTML, CSS, JavaScript (fetch), Chart.js |
| AI | Google Gemini API (google-genai) |
| PDF | ReportLab |
| Deployment | Render, Aiven MySQL |

## Screenshots

![Dashboard](screenshots/dashboard.png)
![Applications](screenshots/applications.png)
![AI tips](screenshots/ai-tips.png)
![PDF export](screenshots/pdf.png)

## Security notes

- Passwords are hashed with Werkzeug, never stored in plain text
- Every database query that touches applications filters by the logged-in student's id
- All SQL uses parameterised queries to prevent SQL injection
- User text is inserted into pages with `textContent`, which prevents XSS
- Secrets are kept in environment variables and are not committed to Git

## Run it locally

1. Clone the repo and open the folder:
```
   git clone https://github.com/avishwa25/placement-tracker.git
   cd placement-tracker
```
2. Create and activate a virtual environment, then install the packages:
```
   python -m venv venv
   venv\Scripts\activate.bat
   pip install -r requirements.txt
```
3. Create the database by running `schema.sql` in MySQL Workbench or with the `mysql` client.
4. Copy `.env.example` to `.env` and fill in your own values. A free Gemini API key is available from Google AI Studio.
5. Start the app and open http://127.0.0.1:5000:
```
   python app.py
```

## API overview

| Route | Method | Purpose |
|---|---|---|
| `/api/applications` | GET, POST | List or add applications |
| `/api/applications/<id>` | PUT, DELETE | Update status or delete |
| `/api/stats` | GET | Counts per status for the chart |
| `/api/resume-tip` | POST | Generate AI resume tips |
| `/export/pdf` | GET | Download applications as PDF |

## Author

Avinash G K, [GitHub](https://github.com/avishwa25)