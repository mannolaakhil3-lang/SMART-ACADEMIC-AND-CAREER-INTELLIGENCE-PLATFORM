"""
Flask Web Application
SMART ACADEMIC AND CAREER INTELLIGENCE PLATFORM
Team: G-2
"""

from flask import Flask, render_template, request, redirect, url_for
from recommendation_engine import calculate_career_match, parse_list_input

app = Flask(__name__)

# Canonical Demo Student Data
DEMO_STUDENT = {
    "name": "Demo Student",
    "branch": "CSE",
    "cgpa": "8.2",
    "skills": "Python, SQL, Problem Solving, Communication",
    "interests": "Technology, Data Science, Analytics"
}


@app.route("/")
def home():
    """Home landing page."""
    return render_template("index.html")


@app.route("/analysis")
def analysis():
    """Student analysis form page."""
    # Check if demo prefill is requested
    prefill = request.args.get("prefill") == "true"
    initial_data = DEMO_STUDENT if prefill else {
        "name": "",
        "branch": "",
        "cgpa": "",
        "skills": "",
        "interests": ""
    }
    return render_template("analysis.html", data=initial_data)


@app.route("/demo")
def demo():
    """Directly triggers the complete demo evaluation and displays results."""
    skills_list = parse_list_input(DEMO_STUDENT["skills"])
    interests_list = parse_list_input(DEMO_STUDENT["interests"])
    cgpa_val = float(DEMO_STUDENT["cgpa"])

    results = calculate_career_match(
        student_name=DEMO_STUDENT["name"],
        branch=DEMO_STUDENT["branch"],
        cgpa=cgpa_val,
        student_skills=skills_list,
        student_interests=interests_list
    )
    return render_template("results.html", results=results, is_demo=True)


@app.route("/analyze", methods=["POST"])
def analyze():
    """Handles submission from analysis form and computes career recommendations."""
    name = request.form.get("name", "").strip() or "Student"
    branch = request.form.get("branch", "").strip() or "General Engineering"
    
    try:
        cgpa = float(request.form.get("cgpa", 7.0))
    except ValueError:
        cgpa = 7.0

    raw_skills = request.form.get("skills", "").strip()
    raw_interests = request.form.get("interests", "").strip()

    skills_list = parse_list_input(raw_skills)
    interests_list = parse_list_input(raw_interests)

    results = calculate_career_match(
        student_name=name,
        branch=branch,
        cgpa=cgpa,
        student_skills=skills_list,
        student_interests=interests_list
    )

    return render_template("results.html", results=results, is_demo=False)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
