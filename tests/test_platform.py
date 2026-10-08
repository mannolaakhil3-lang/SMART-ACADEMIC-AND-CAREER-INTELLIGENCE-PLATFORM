"""
SMART ACADEMIC AND CAREER INTELLIGENCE PLATFORM
Team: G-2 PBL Project Test Suite
Automated Unit Tests & Integration Tests for Engine and Flask Web Routes
"""

import unittest
from app import app
from recommendation_engine import (
    CareerRecommendationEngine,
    get_recommendations,
    CAREER_TAXONOMY,
    PRIORITY_LEVELS
)


class TestRecommendationEngine(unittest.TestCase):
    """Unit tests for the rule-based career recommendation engine."""

    def setUp(self):
        self.engine = CareerRecommendationEngine()

    def test_canonical_demo_student(self):
        """
        Verify the canonical demo student produces exact expected results:
        - Rank #1: Data Analyst (88%)
        - Rank #2: Software Developer (82%)
        - Rank #3: AI/ML Engineer (76%)
        """
        student_data = {
            "name": "Demo Student",
            "branch": "CSE",
            "academic_year": "3rd Year",
            "cgpa": 8.2,
            "skills": ["Python", "SQL", "Problem Solving", "Communication"],
            "interests": ["Technology", "Data Science", "Analytics"],
            "soft_skills": ["Teamwork", "Analytical Thinking", "Communication"],
            "career_preference": "Data Analyst"
        }

        results = self.engine.analyze_student_profile(student_data)

        self.assertEqual(results["student"]["name"], "Demo Student")
        self.assertEqual(results["primary_recommendation"]["career"], "Data Analyst")
        self.assertEqual(results["primary_recommendation"]["match_percentage"], 88)

        top_3 = results["top_3_recommendations"]
        self.assertEqual(len(top_3), 3)

        self.assertEqual(top_3[0]["career"], "Data Analyst")
        self.assertEqual(top_3[0]["match_percentage"], 88)

        self.assertEqual(top_3[1]["career"], "Software Developer")
        self.assertEqual(top_3[1]["match_percentage"], 82)

        self.assertEqual(top_3[2]["career"], "AI/ML Engineer")
        self.assertEqual(top_3[2]["match_percentage"], 76)

        # Verify matching skills
        matching_skills = results["primary_recommendation"]["matching_skills"]
        self.assertIn("Python", matching_skills)
        self.assertIn("SQL", matching_skills)

        # Verify skill gaps have priorities
        skill_gaps = results["primary_recommendation"]["skill_gaps"]
        self.assertTrue(len(skill_gaps) > 0)
        gap_names = [g["skill"] for g in skill_gaps]
        self.assertIn("Statistics", gap_names)
        self.assertIn("Data Visualization", gap_names)
        for g in skill_gaps:
            self.assertIn(g["priority"], [PRIORITY_LEVELS["HIGH"], PRIORITY_LEVELS["MEDIUM"], PRIORITY_LEVELS["LOW"]])

        # Verify personalized learning plan (exactly 5 steps)
        plan = results["primary_recommendation"]["learning_plan"]
        self.assertEqual(len(plan), 5)
        for idx, step in enumerate(plan, 1):
            self.assertEqual(step["step_number"], idx)
            self.assertTrue(len(step["title"]) > 0)
            self.assertTrue(len(step["description"]) > 0)

        # Verify career comparison matrix
        comparison = results["career_comparison"]
        self.assertEqual(len(comparison), 3)
        self.assertEqual(comparison[0]["career"], "Data Analyst")
        self.assertEqual(comparison[1]["career"], "Software Developer")
        self.assertEqual(comparison[2]["career"], "AI/ML Engineer")

    def test_custom_student_profile(self):
        """Test engine behavior on a profile oriented toward Web Development."""
        student_data = {
            "name": "Alex",
            "branch": "IT",
            "academic_year": "2nd Year",
            "cgpa": 7.5,
            "skills": ["JavaScript", "HTML", "CSS", "React"],
            "interests": ["Web Design", "Frontend", "User Interface"],
            "soft_skills": ["Creativity"],
            "career_preference": "Web Developer"
        }

        results = self.engine.analyze_student_profile(student_data)
        self.assertIsNotNone(results["primary_recommendation"])
        self.assertEqual(len(results["top_3_recommendations"]), 3)
        # Check that match percentage is a valid integer between 0 and 100
        for rec in results["top_3_recommendations"]:
            self.assertGreaterEqual(rec["match_percentage"], 0)
            self.assertLessEqual(rec["match_percentage"], 100)

    def test_taxonomy_integrity(self):
        """Ensure all careers in taxonomy have required benchmark structures."""
        for career, meta in CAREER_TAXONOMY.items():
            self.assertIn("skills", meta)
            self.assertIn("core_requirements", meta)
            self.assertIn("interests", meta)
            self.assertIn("description", meta)
            self.assertIn("learning_plan", meta)
            self.assertIn("skill_gap_priorities", meta)
            self.assertEqual(len(meta["learning_plan"]), 5, f"{career} must have 5 learning steps")


class TestFlaskWebRoutes(unittest.TestCase):
    """Integration tests for Flask HTTP endpoints and user flows."""

    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

    def test_index_route(self):
        """Test home page loads with 200 OK and expected PBL branding."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        html = response.data.decode("utf-8")
        self.assertIn("SMART ACADEMIC AND CAREER INTELLIGENCE PLATFORM", html)
        self.assertIn("Team: G-2", html)
        self.assertIn("Rule-Based Career Recommendation Engine", html)
        self.assertIn("How It Works", html)
        self.assertIn("Technology Stack", html)

    def test_analysis_get_route(self):
        """Test analysis form page loads with 200 OK."""
        response = self.client.get("/analysis")
        self.assertEqual(response.status_code, 200)
        html = response.data.decode("utf-8")
        self.assertIn("Student Academic & Skills Profile", html)
        self.assertIn('name="cgpa"', html)
        self.assertIn('name="skills"', html)
        self.assertIn('name="interests"', html)

    def test_analysis_prefill_route(self):
        """Test analysis form pre-populates canonical demo values with ?prefill=true."""
        response = self.client.get("/analysis?prefill=true")
        self.assertEqual(response.status_code, 200)
        html = response.data.decode("utf-8")
        self.assertIn("Demo Student", html)
        self.assertIn("8.2", html)
        self.assertIn("Python, SQL", html)

    def test_analyze_post_valid_demo_student(self):
        """Test submitting valid demo student profile through POST /analyze."""
        form_data = {
            "name": "Demo Student",
            "branch": "CSE",
            "academic_year": "3rd Year",
            "cgpa": "8.2",
            "skills": "Python, SQL, Problem Solving, Communication",
            "interests": "Technology, Data Science, Analytics",
            "soft_skills": "Teamwork, Analytical Thinking",
            "career_preference": "Data Analyst"
        }
        response = self.client.post("/analyze", data=form_data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        html = response.data.decode("utf-8")
        self.assertIn("Career Intelligence Report: Demo Student", html)
        self.assertIn("Data Analyst", html)
        self.assertIn("88% Match", html)
        self.assertIn("Software Developer", html)
        self.assertIn("82% Match", html)
        self.assertIn("AI/ML Engineer", html)
        self.assertIn("76% Match", html)
        self.assertIn("Career Comparison Matrix", html)
        self.assertIn("Print Report", html)

    def test_analyze_validation_errors(self):
        """Test form validation catches empty fields and invalid CGPA."""
        # Test missing name
        res = self.client.post("/analyze", data={"name": "", "branch": "CSE", "cgpa": "8.0", "skills": "Python", "interests": "Tech"})
        self.assertEqual(res.status_code, 400)
        self.assertIn("Please enter the student&#39;s full name.", res.data.decode("utf-8"))

        # Test invalid CGPA > 10.0
        res = self.client.post("/analyze", data={"name": "Test", "branch": "CSE", "cgpa": "11.5", "skills": "Python", "interests": "Tech"})
        self.assertEqual(res.status_code, 400)
        self.assertIn("CGPA must be a valid number between 0.0 and 10.0.", res.data.decode("utf-8"))

        # Test invalid negative CGPA
        res = self.client.post("/analyze", data={"name": "Test", "branch": "CSE", "cgpa": "-2.0", "skills": "Python", "interests": "Tech"})
        self.assertEqual(res.status_code, 400)
        self.assertIn("CGPA must be a valid number between 0.0 and 10.0.", res.data.decode("utf-8"))

        # Test missing skills
        res = self.client.post("/analyze", data={"name": "Test", "branch": "CSE", "cgpa": "8.0", "skills": "", "interests": "Tech"})
        self.assertEqual(res.status_code, 400)
        self.assertIn("Please provide at least one technical or professional skill.", res.data.decode("utf-8"))

    def test_direct_results_get_redirects(self):
        """Accessing /results directly via GET without session data should redirect to /analysis."""
        response = self.client.get("/results", follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.location.endswith("/analysis"))


if __name__ == "__main__":
    unittest.main()
