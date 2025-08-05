# 📆 Google Calendar Extractor

## 🧠 Project Summary

This project provides a Python-based tool that extracts **all past and future events** from a user's **Google Calendar** and stores them in a structured CSV file. It serves as a personal or organizational utility to track event history, measure productivity, analyze time allocation, or build time-based reports for billing or operations.

---

## 🛠️ Tech Stack

| Category              | Tools & Technologies                                      |
|-----------------------|-----------------------------------------------------------|
| **Language**           | Python 3                                                  |
| **API Integration**    | Google Calendar API, OAuth2 (via `google-auth`, `google-api-python-client`) |
| **Data Handling**      | `pandas`, `datetime`, `os`, `csv`                         |
| **Credential Storage** | `token.json`, `credentials.json`                         |
| **Runtime Environment**| Jupyter Notebook, Python Script, CLI                     |
| **Deployment**         | GitHub Repository (manual run, or CRON-compatible)       |

---

## 🔍 Data Science Techniques

Even though this is a tool-focused project, it lays the foundation for several common data science workflows:

- **Data Extraction (ETL)**  
  Automated extraction of calendar data using authenticated API calls and storage in flat file format for downstream analysis.

- **Data Normalization**  
  Timezone handling, string sanitization, and datetime parsing to ensure clean, analysis-ready data.

- **Pipeline Reusability**  
  Modular script structure allows easy integration into larger ETL workflows or recurring cron jobs.

- **Historical Tracking**  
  Enables retrospective analysis of time spent across meetings, projects, clients, or departments.

- **Foundation for Analytics**  
  Sets up a data layer that can be plugged into visualization tools (e.g., Power BI, Tableau) or further statistical modeling (e.g., clustering by meeting type, forecasting workload, etc.)

---

## 📈 Impact

- ✅ **Centralized Event History**  
  Eliminates the need to manually scroll through calendar UIs to access historical data.

- ⏱ **Time Audit & Optimization**  
  Enables personal productivity review or organizational time-allocation tracking.

- 📊 **Billing & Client Tracking**  
  Helpful for consultants, analysts, or healthcare professionals needing evidence of time spent per client or category.

- 🧩 **Plug-and-Play Integration**  
  CSV output makes it easy to use with Excel, Python, R, BI tools, or Google Sheets for custom dashboards.

- 🔄 **Repeatable & Scalable**  
  Designed to be run at any interval with minimal setup — ideal for weekly/monthly analytics pipelines.

---

## 📂 File Structure

```bash
calendar-extractor/
│
├── calendar_extractor.py        # Main script: connects to API and writes CSV
├── credentials.json             # OAuth 2.0 credentials (from Google Console)
├── token.json                   # OAuth token (auto-generated after first run)
├── events.csv                   # Output file with event history
├── README.md                    # Documentation
└── requirements.txt             # Python dependencies

