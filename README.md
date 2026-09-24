# PrepAI – Placement Preparation Platform

PrepAI is a web-based placement preparation platform designed to help students practice technical subjects, coding problems, aptitude questions, mock interviews, and resume analysis in one place.

## Features

### Technical Practice

* Python
* Java
* SQL
* DBMS
* Data Structures & Algorithms
* Computer Networks

### Coding Practice

* Easy Problems
* Medium Problems
* Placement-Oriented Problems

### Aptitude Practice

* Quantitative Aptitude
* Logical Reasoning
* Verbal Ability

### Mock Interview

* Technical Interview
* HR Interview
* Interview performance tracking

### Resume Analyzer

* PDF resume upload
* Resume text extraction
* Resume section detection
* Technical skill detection
* Resume improvement suggestions

### Performance Analytics

* Questions attempted
* Interview sessions
* Subject-wise technical scores
* Overall technical performance
* Areas of strength and improvement

### User Authentication

* Registration
* Login
* Session-based access control

## Technology Stack

### Frontend

* HTML5
* CSS3
* JavaScript

### Backend

* Python
* Flask

### Database

* MySQL
* SQLAlchemy

### Other Tools & Libraries

* PyPDF
* Git
* GitHub

## Project Structure

```text
PrepAI/
│
├── app.py
├── .gitignore
├── README.md
│
├── templates/
│   ├── index.html
│   ├── register.html
│   ├── login.html
│   ├── dashboard.html
│   ├── analytics.html
│   ├── resume_analyzer.html
│   └── ...
│
└── static/
    └── css/
        └── style.css
```

## Key Modules

### Technical Practice

The platform provides subject-wise practice modules for core computer science topics. Each module contains multiple-choice questions, scoring, progress tracking, and result pages.

### Coding Practice

Users can practice programming problems categorized by difficulty and placement relevance.

### Mock Interview

PrepAI provides separate technical and HR interview practice. Interview responses are evaluated using predefined criteria and completed interview activity is tracked.

### Resume Analyzer

Users can upload a PDF resume. PrepAI extracts text from the document and checks for important resume sections and technical skills. It then provides suggestions for improving the resume.

### Performance Analytics

The analytics dashboard combines practice activity and technical test performance to provide a quick view of preparation progress.

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/mannukumari0508/PrepAI.git
cd PrepAI
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

### 3. Activate the Virtual Environment

For Windows PowerShell:

```bash
venv\Scripts\Activate.ps1
```

### 4. Install Dependencies

```bash
pip install flask flask-sqlalchemy werkzeug pypdf
```

### 5. Configure MySQL

Create the required MySQL database and configure the database connection in the Flask application.

### 6. Run the Application

```bash
python app.py
```

Then open:

```text
http://127.0.0.1:5000
```

## Learning Objectives

This project was developed to strengthen practical understanding of:

* Flask web application development
* Python programming
* MySQL database integration
* SQLAlchemy
* HTML, CSS and JavaScript
* User authentication
* Session management
* File upload and PDF processing
* Quiz and scoring systems
* Performance tracking
* Git and GitHub

## Future Improvements

Possible future enhancements include:

* AI-powered interview feedback using an external AI API
* Real code execution for coding problems
* Larger question banks
* Personalized study recommendations
* Advanced resume analysis
* Detailed performance charts
* Role-based preparation plans
* Deployment on a cloud platform

## Author

**Mannu Kumari**

B.Tech – Computer Science & Engineering
Asansol Engineering College

GitHub: `https://github.com/mannukumari0508`
