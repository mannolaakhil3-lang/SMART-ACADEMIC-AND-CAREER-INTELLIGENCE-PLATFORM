"""
Flask Web Application
SMART ACADEMIC AND CAREER INTELLIGENCE PLATFORM
Team: G-2
"""

from typing import Dict, Any
from flask import Flask, render_template, request, redirect, url_for
from recommendation_engine import calculate_career_match, parse_list_input
from ml_model import predict_career, compute_hybrid_guidance

app = Flask(__name__)

# Canonical Demo Student Data (Team G-2 PBL Benchmark)
DEMO_STUDENT: Dict[str, Any] = {
    "name": "Demo Student",
    "branch": "CSE",
    "academic_year": "3rd Year",
    "cgpa": "8.2",
    "skills": "Python, SQL, Problem Solving",
    "soft_skills": "Communication, Teamwork",
    "interests": "Technology, Data Science, Analytics",
    "career_preference": "Data Analyst"
}


@app.route("/")
def home():
    """Home landing page with platform overview and workflow visual."""
    return render_template("index.html")


@app.route("/profile")
def profile_alias():
    """Alias route for analysis profile input."""
    return redirect(url_for("analysis"))


@app.route("/analysis")
def analysis():
    """Student analysis form page with prefill support."""
    prefill = request.args.get("prefill") == "true"
    initial_data = DEMO_STUDENT if prefill else {
        "name": "",
        "branch": "",
        "academic_year": "3rd Year",
        "cgpa": "",
        "skills": "",
        "soft_skills": "",
        "interests": "",
        "career_preference": ""
    }
    return render_template("analysis.html", data=initial_data, error=None)


@app.route("/demo")
def demo():
    """Directly triggers the canonical demo evaluation and displays results."""
    skills_list = parse_list_input(DEMO_STUDENT["skills"])
    soft_skills_list = parse_list_input(DEMO_STUDENT["soft_skills"])
    interests_list = parse_list_input(DEMO_STUDENT["interests"])
    cgpa_val = float(DEMO_STUDENT["cgpa"])

    results = calculate_career_match(
        student_name=DEMO_STUDENT["name"],
        branch=DEMO_STUDENT["branch"],
        academic_year=DEMO_STUDENT["academic_year"],
        cgpa=cgpa_val,
        student_skills=skills_list,
        soft_skills=soft_skills_list,
        student_interests=interests_list,
        career_preference=DEMO_STUDENT["career_preference"]
    )

    # Execute ML Prediction & Hybrid Consensus
    ml_student_payload = {
        "name": DEMO_STUDENT["name"],
        "branch": DEMO_STUDENT["branch"],
        "academic_year": DEMO_STUDENT["academic_year"],
        "cgpa": cgpa_val,
        "skills": skills_list,
        "soft_skills": soft_skills_list,
        "interests": interests_list,
        "career_preference": DEMO_STUDENT["career_preference"]
    }
    ml_results = predict_career(ml_student_payload)
    hybrid_guidance = compute_hybrid_guidance(results, ml_results)

    return render_template(
        "results.html",
        results=results,
        ml_results=ml_results,
        hybrid_guidance=hybrid_guidance,
        is_demo=True
    )


@app.route("/results", methods=["GET"])
def direct_results():
    """Friendly redirect for direct GET requests to /results."""
    return redirect(url_for("analysis"))


@app.route("/analyze", methods=["POST"])
def analyze():
    """Handles submission from analysis form and computes career recommendations."""
    # Capture raw form fields
    name = request.form.get("name", "").strip()
    branch = request.form.get("branch", "").strip()
    academic_year = request.form.get("academic_year", "3rd Year").strip()
    raw_cgpa = request.form.get("cgpa", "").strip()
    raw_skills = request.form.get("skills", "").strip()
    raw_soft_skills = request.form.get("soft_skills", "").strip()
    raw_interests = request.form.get("interests", "").strip()
    career_preference = request.form.get("career_preference", "").strip()

    # Form state to preserve user inputs on error
    form_data = {
        "name": name,
        "branch": branch,
        "academic_year": academic_year,
        "cgpa": raw_cgpa,
        "skills": raw_skills,
        "soft_skills": raw_soft_skills,
        "interests": raw_interests,
        "career_preference": career_preference
    }

    # Validation: Required text fields
    if not name:
        return render_template(
            "analysis.html",
            data=form_data,
            error="Please enter the student's full name."
        ), 400

    if not branch:
        return render_template(
            "analysis.html",
            data=form_data,
            error="Please enter the student's branch or academic discipline."
        ), 400

    if not raw_skills:
        return render_template(
            "analysis.html",
            data=form_data,
            error="Please provide at least one technical or professional skill."
        ), 400

    if not raw_interests:
        return render_template(
            "analysis.html",
            data=form_data,
            error="Please provide at least one area of interest or domain passion."
        ), 400

    # Validation: CGPA numerical range check (0.0 to 10.0)
    try:
        cgpa_val = float(raw_cgpa)
        if cgpa_val < 0.0 or cgpa_val > 10.0:
            return render_template(
                "analysis.html",
                data=form_data,
                error="CGPA must be a valid number between 0.0 and 10.0."
            ), 400
    except (ValueError, TypeError):
        return render_template(
            "analysis.html",
            data=form_data,
            error="Invalid CGPA entered. Please enter a valid decimal number between 0.0 and 10.0 (e.g., 8.2)."
        ), 400

    # Parse and normalize list inputs
    skills_list = parse_list_input(raw_skills)
    soft_skills_list = parse_list_input(raw_soft_skills)
    interests_list = parse_list_input(raw_interests)

    if not skills_list:
        return render_template(
            "analysis.html",
            data=form_data,
            error="Please enter valid skill keywords separated by commas."
        ), 400

    if not interests_list:
        return render_template(
            "analysis.html",
            data=form_data,
            error="Please enter valid interest keywords separated by commas."
        ), 400

    # Execute Rule-Based Recommendation Engine
    results = calculate_career_match(
        student_name=name,
        branch=branch,
        academic_year=academic_year,
        cgpa=cgpa_val,
        student_skills=skills_list,
        soft_skills=soft_skills_list,
        student_interests=interests_list,
        career_preference=career_preference
    )

    # Execute ML Career Prediction & Hybrid Consensus
    student_payload = {
        "name": name,
        "branch": branch,
        "academic_year": academic_year,
        "cgpa": cgpa_val,
        "skills": skills_list,
        "soft_skills": soft_skills_list,
        "interests": interests_list,
        "career_preference": career_preference
    }
    ml_results = predict_career(student_payload)
    hybrid_guidance = compute_hybrid_guidance(results, ml_results)

    return render_template(
        "results.html",
        results=results,
        ml_results=ml_results,
        hybrid_guidance=hybrid_guidance,
        is_demo=False
    )


@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 with friendly user message and no exposed stack trace."""
    return render_template(
        "analysis.html",
        data=DEMO_STUDENT,
        error="The requested page was not found (404). You have been safely returned to the analysis portal."
    ), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 without exposing server stack traces to users."""
    return render_template(
        "analysis.html",
        data=DEMO_STUDENT,
        error="An unexpected server error occurred (500). Please check your inputs and try again."
    ), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
