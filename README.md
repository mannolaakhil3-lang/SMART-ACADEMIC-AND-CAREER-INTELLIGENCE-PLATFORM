# SMART ACADEMIC AND CAREER INTELLIGENCE PLATFORM
**Team:** G-2

A lightweight, high-performance web platform that delivers transparent, deterministic career recommendations, skill gap analyses, and personalized learning plans for students.

---

## 🚀 Key Highlights & Architectural Features

- **No Black-Box AI / No External API Dependencies:** Uses a fully deterministic **Rule-Based Career Recommendation Engine**.
- **Fast & Responsive Stack:** Python Flask backend with modern, responsive HTML5/CSS3/JavaScript frontend.
- **Instant Demo Mode:** Evaluate the canonical student profile with a single click.
- **Comprehensive Outputs:**
  1. **Top 3 Career Recommendations** with quantitative match percentages and progress bars.
  2. **Matching Skills** highlighting current student competencies.
  3. **Skill Gaps** identifying missing core skills for target roles.
  4. **Recommended Skills** prioritized for maximum career impact.
  5. **Personalized 5-Step Learning Plan** structured as a practical roadmap.

---

## 🎯 6 Supported Career Tracks

1. **Data Analyst**
2. **Software Developer**
3. **AI/ML Engineer**
4. **Cybersecurity Analyst**
5. **UI/UX Designer**
6. **Business Analyst**

---

## ⚙️ Rule-Based Recommendation Scoring Model

The recommendation engine scores each career track using a deterministic weighted evaluation:

- **Matching Skills (50% Weight):** Measures alignment between student skills and industry core competencies.
- **Interests Alignment (30% Weight):** Evaluates student passions and domain interests.
- **Academic Standing / CGPA (20% Weight):** Normalizes the student's CGPA on a standard 10.0 scale.

---

## 📦 Installation & Setup

### 1. Prerequisites
- Python 3.8 or higher installed on your machine.

### 2. Navigate to the Project Directory
```powershell
cd C:\Users\manno\.gemini\antigravity\scratch\career-intelligence-platform
```

### 3. Install Dependencies
```powershell
python -m pip install -r requirements.txt
```

---

## ▶️ Running the Application

Execute:
```powershell
python app.py
```

The application will start on:
👉 **Local URL:** `http://127.0.0.1:5000`

---

## 🧪 Step-by-Step Demo Walkthrough

1. Open your browser and navigate to: `http://127.0.0.1:5000`
2. **Option A (One-Click Instant Demo):**
   - Click the **"Try Demo"** button on the Home hero section or navigation bar.
   - The platform immediately loads the canonical student profile:
     - **Name:** Demo Student
     - **Branch:** CSE
     - **CGPA:** 8.2
     - **Skills:** Python, SQL, Problem Solving, Communication
     - **Interests:** Technology, Data Science, Analytics
   - The results screen renders immediately showing:
     - **Top 3 Career Recommendations:**
       1. Data Analyst — **88% Match**
       2. Software Developer — **82% Match**
       3. AI/ML Engineer — **76% Match**
     - **Matching Skills:** Python, SQL, Problem Solving
     - **Skill Gaps:** Statistics, Data Visualization, Machine Learning
     - **Recommended Skills:** Statistics, Power BI, Data Visualization
     - **Personalized Learning Plan:** 5 sequential steps from Python strengthening to GitHub portfolio deployment.
3. **Option B (Custom Analysis):**
   - Click **"Start Analysis"** on the Home page.
   - Fill in custom student details (or click **"Load Demo Values"** in the helper banner).
   - Click **"ANALYZE MY CAREER"** to generate the customized recommendations.

---

## 📁 Project Structure

```
career-intelligence-platform/
│
├── app.py                     # Flask application entry point & routing
├── recommendation_engine.py   # Rule-Based Career Recommendation Engine
├── requirements.txt           # Python package requirements
├── README.md                  # Project documentation & instructions
│
├── templates/
│   ├── index.html             # Home page with hero and feature highlights
│   ├── analysis.html          # Student input form with demo loader
│   └── results.html           # Comprehensive career recommendations report
│
└── static/
    ├── style.css              # Modern, clean, responsive styles & progress bars
    └── script.js              # Interactive animations & form helper scripts
```
