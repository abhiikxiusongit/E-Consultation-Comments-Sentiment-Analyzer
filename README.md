# E-Consultation Sentiment Analysis

> AI-powered web application for analyzing public consultation comments using Natural Language Processing.

## Overview

E-Consultation Sentiment Analysis is a Flask-based web application designed to help analyze citizen feedback in a fast and meaningful way. The system takes multiple comments as input, applies sentiment analysis using NLP techniques, and presents the results through charts, word clouds, downloadable CSV files, and PDF reports.

This project is especially useful for government consultations, policy feedback analysis, surveys, and opinion mining where large numbers of public responses need to be summarized efficiently.

---

## Problem Statement

In many public consultation processes, authorities receive hundreds or even thousands of comments from citizens. Reading and interpreting them manually is time-consuming and may delay policy decisions.

This project solves that problem by:
- Automatically classifying comments into Positive, Neutral, and Negative categories
- Generating visual insights for faster understanding
- Providing downloadable outputs for reporting and documentation
- Making citizen feedback analysis more structured and accessible

---

## Features

- Sentiment analysis using **TextBlob**
- Sentiment analysis using **VADER**
- Comment-wise sentiment score and confidence
- Session-based storage of analysis history
- Interactive sentiment distribution chart
- Overall word cloud generation
- Positive, Neutral, and Negative word clouds
- CSV export for analyzed comments
- PDF report export
- Clean web interface for easy interaction

---

## Tech Stack

### Backend
- Python
- Flask
- Flask-SQLAlchemy
- SQLite

### NLP and Data Analysis
- TextBlob
- VADER Sentiment
- NLTK
- Pandas
- NumPy

### Visualization
- Plotly
- Matplotlib
- WordCloud

### Export and Reporting
- WeasyPrint
- ReportLab

### Frontend
- HTML
- CSS
- Bootstrap
- JavaScript

---

## How It Works

1. User enters multiple comments into the input form.
2. User selects a sentiment analysis method: TextBlob or VADER.
3. The system processes each comment individually.
4. Results are stored in the database.
5. The application displays:
   - total comments
   - sentiment counts
   - average sentiment
   - chart visualization
   - word clouds
   - detailed comment-wise results
6. The user can export the results in CSV or PDF format.

---

## Project Structure

```bash
e-consultation-sentiment-analysis/
│
├── app.py
├── requirements.txt
├── README.md
├── CONTRIBUTORS.md
├── .gitignore
├── sentiment_analysis.db
│
├── templates/
│   ├── index.html
│   ├── results.html
│   ├── history.html
│   └── pdf_report.html
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
└── venv/
```

---

## Installation

### Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/e-consultation-sentiment-analysis.git
cd e-consultation-sentiment-analysis
```

### Create virtual environment

#### Windows PowerShell
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

#### Windows Command Prompt
```cmd
python -m venv venv
venv\Scripts\activate
```

### Install required libraries

```bash
pip install -r requirements.txt
```

### Run the application

```bash
python app.py
```

### Open in browser

```bash
http://127.0.0.1:5000
```

---

## Usage

- Enter one comment per line
- Choose the analysis method
- Click on **Analyze**
- Review sentiment summary and visual outputs
- Export the results as CSV or PDF if needed

---

## Output Includes

- Sentiment label for each comment
- Sentiment score
- Confidence score
- Total positive, neutral, and negative comments
- Average sentiment of the session
- Pie chart of sentiment distribution
- Word cloud visualizations
- Exportable CSV file
- Exportable PDF report

---

## Use Cases

This project can be used in:
- Government e-consultation platforms
- Public opinion analysis
- Survey feedback analysis
- Policy review systems
- Academic NLP demonstrations
- Hackathon prototypes and research presentations

---

## Future Enhancements

- Multi-language sentiment analysis
- Advanced transformer-based models
- Better sarcasm and context detection
- Real-time dashboard analytics
- User authentication and role-based access
- Cloud deployment support

---

## Team

- **Your Name** – Backend development, Flask integration, NLP pipeline
- **Teammate 1 Name** – Frontend development, user interface design
- **Teammate 2 Name** – Testing, documentation, exports, support

> Replace the above names with the actual team member names.

---

## Contributors

Each team member should:
- be added as a GitHub collaborator
- make at least one commit from their own GitHub account
- be listed in `CONTRIBUTORS.md`
- mention their role clearly for resume and portfolio use

---

## License

This project is currently intended for academic, learning, and hackathon purposes.

---

## Acknowledgement

This project was developed as part of a collaborative problem-solving and hackathon effort to improve large-scale feedback analysis through Natural Language Processing and data visualization.
