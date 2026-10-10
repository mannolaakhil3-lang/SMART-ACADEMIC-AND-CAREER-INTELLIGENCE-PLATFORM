"""
Automated Test Suite for Machine Learning Module & Integration
Smart Academic and Career Intelligence Platform (Team G-2)

Tests:
1. Dataset loading and schema validation
2. Missing dataset and missing column error handling
3. Feature engineering and student input normalization
4. Random Forest model training, evaluation, and test split metrics
5. Model serialization, persistence, and safe loading
6. Missing model bundle graceful degradation
7. Career prediction inference and probability calibration
8. Hybrid consensus and dual-perspective synthesis
9. Flask integration (GET /demo, POST /analyze, 404 handling)
"""

import os
import unittest
import tempfile
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier

from ml_model import (
    load_dataset,
    preprocess_data,
    extract_features_from_student,
    train_model,
    evaluate_model,
    train_and_save_pipeline,
    CareerMLPredictor,
    predict_career,
    compute_hybrid_guidance,
    DATA_PATH,
    MODEL_PATH,
    METRICS_PATH,
    FEATURE_COLUMNS,
    TARGET_COLUMN
)
from app import app, DEMO_STUDENT
from recommendation_engine import calculate_career_match


class TestDatasetAndPreprocessing(unittest.TestCase):
    """Tests for dataset loading, validation, and feature preprocessing."""

    def test_load_dataset_success(self):
        """Verify the primary dataset loads with correct columns and non-empty rows."""
        self.assertTrue(os.path.exists(DATA_PATH), f"Dataset missing at {DATA_PATH}")
        df = load_dataset(DATA_PATH)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertGreater(len(df), 50)
        
        # Verify all expected feature columns and target column are present
        for col in FEATURE_COLUMNS:
            self.assertIn(col, df.columns)
        self.assertIn(TARGET_COLUMN, df.columns)

    def test_load_dataset_missing_file_raises_error(self):
        """Verify FileNotFoundError is raised when dataset path does not exist."""
        with self.assertRaises(FileNotFoundError):
            load_dataset("non_existent_path_to_dataset.csv")

    def test_load_dataset_missing_columns_raises_error(self):
        """Verify ValueError is raised when dataset is missing required features."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write("cgpa,python,career\n8.5,1,Data Analyst\n")
            temp_path = f.name

        try:
            with self.assertRaises(ValueError):
                load_dataset(temp_path)
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    def test_preprocess_data(self):
        """Verify feature matrix X and target vector y are split and contain no NaNs."""
        df = load_dataset(DATA_PATH)
        X, y = preprocess_data(df)
        self.assertEqual(len(X), len(y))
        self.assertEqual(list(X.columns), FEATURE_COLUMNS)
        self.assertFalse(X.isnull().any().any(), "X should have no missing values")
        self.assertFalse(y.isnull().any(), "y should have no missing values")

    def test_extract_features_valid_student(self):
        """Verify extract_features_from_student returns a single-row DataFrame with all features."""
        student = {
            "cgpa": 8.5,
            "skills": ["python", "sql", "problem solving"],
            "soft_skills": ["communication"],
            "interests": ["data science", "analytics"]
        }
        X_student = extract_features_from_student(student)
        self.assertIsInstance(X_student, pd.DataFrame)
        self.assertEqual(len(X_student), 1)
        self.assertEqual(list(X_student.columns), FEATURE_COLUMNS)
        self.assertEqual(X_student["python"].iloc[0], 1)
        self.assertEqual(X_student["sql"].iloc[0], 1)
        self.assertEqual(X_student["data_science_interest"].iloc[0], 1)
        self.assertAlmostEqual(X_student["cgpa"].iloc[0], 8.5)

    def test_extract_features_string_inputs(self):
        """Verify string format inputs (comma-separated) are parsed correctly."""
        student = {
            "cgpa": "7.8",
            "skills": "Python, SQL, Java",
            "soft_skills": "Teamwork, Communication",
            "interests": "Technology, Coding"
        }
        X_student = extract_features_from_student(student)
        self.assertEqual(X_student["python"].iloc[0], 1)
        self.assertEqual(X_student["sql"].iloc[0], 1)
        self.assertEqual(X_student["java"].iloc[0], 1)
        self.assertAlmostEqual(X_student["cgpa"].iloc[0], 7.8)

    def test_extract_features_invalid_cgpa_fallback(self):
        """Verify invalid or non-numeric CGPA falls back to safe default."""
        student = {
            "cgpa": "invalid_value",
            "skills": ["python"],
            "interests": ["tech"]
        }
        X_student = extract_features_from_student(student)
        self.assertGreaterEqual(X_student["cgpa"].iloc[0], 0.0)
        self.assertLessEqual(X_student["cgpa"].iloc[0], 10.0)


class TestMLModelTrainingAndEvaluation(unittest.TestCase):
    """Tests for model training, metrics calculation, and serialization."""

    def test_train_model_returns_fitted_classifier(self):
        """Verify train_model returns a fitted scikit-learn RandomForestClassifier."""
        df = load_dataset(DATA_PATH)
        X, y = preprocess_data(df)
        model = train_model(X, y, random_state=42, n_estimators=20)
        self.assertIsInstance(model, RandomForestClassifier)
        self.assertTrue(hasattr(model, "classes_"))
        self.assertGreater(len(model.classes_), 1)

    def test_evaluate_model_metrics(self):
        """Verify evaluate_model computes genuine multiclass accuracy, precision, recall, and F1."""
        df = load_dataset(DATA_PATH)
        X, y = preprocess_data(df)
        model = train_model(X, y, random_state=42, n_estimators=20)
        metrics = evaluate_model(model, X, y)
        
        self.assertIn("accuracy", metrics)
        self.assertIn("precision", metrics)
        self.assertIn("recall", metrics)
        self.assertIn("f1_score", metrics)
        self.assertIn("confusion_matrix", metrics)
        self.assertIn("feature_importances", metrics)
        
        self.assertGreaterEqual(metrics["accuracy"], 0.0)
        self.assertLessEqual(metrics["accuracy"], 100.0)
        self.assertGreater(len(metrics["feature_importances"]), 0)


class TestMLPredictorService(unittest.TestCase):
    """Tests for CareerMLPredictor singleton and prediction interface."""

    def test_model_file_exists_and_loads(self):
        """Verify persisted model bundle loads successfully."""
        self.assertTrue(os.path.exists(MODEL_PATH), f"Model bundle missing at {MODEL_PATH}")
        predictor = CareerMLPredictor.get_instance()
        self.assertTrue(predictor.is_available())

    def test_predict_career_on_demo_student(self):
        """Verify predict_career produces valid predictions on canonical demo student."""
        res = predict_career(DEMO_STUDENT)
        self.assertTrue(res.get("available"))
        self.assertIn("predicted_career", res)
        self.assertIn("confidence_score", res)
        self.assertIn("career_probabilities", res)
        self.assertIn("active_features", res)
        self.assertIn("metrics", res)

        # Check probability structure
        probs = res["career_probabilities"]
        self.assertGreater(len(probs), 0)
        for p in probs:
            self.assertIn("career", p)
            self.assertIn("probability", p)
            self.assertGreaterEqual(p["probability"], 0.0)

    def test_missing_model_file_graceful_handling(self):
        """Verify predictor returns graceful fallback when model bundle does not exist."""
        temp_predictor = CareerMLPredictor(model_path="non_existent_model.joblib")
        res = temp_predictor.predict(DEMO_STUDENT)
        self.assertFalse(res["available"])
        self.assertIn("message", res)

    def test_hybrid_guidance_consensus_agreed(self):
        """Verify compute_hybrid_guidance detects consensus when rule and ML agree."""
        rule_res = {
            "primary_recommendation": {
                "career": "Data Analyst",
                "match_percentage": 88
            }
        }
        ml_res = {
            "available": True,
            "predicted_career": "Data Analyst",
            "confidence_score": 75.0
        }
        hybrid = compute_hybrid_guidance(rule_res, ml_res)
        self.assertTrue(hybrid["hybrid_available"])
        self.assertTrue(hybrid["consensus"])
        self.assertEqual(hybrid["status"], "CONSENSUS_AGREED")
        self.assertAlmostEqual(hybrid["hybrid_score"], round((0.70 * 88) + (0.30 * 75.0), 1))

    def test_hybrid_guidance_divergent(self):
        """Verify compute_hybrid_guidance detects divergent perspectives cleanly."""
        rule_res = {
            "primary_recommendation": {
                "career": "Data Analyst",
                "match_percentage": 88
            }
        }
        ml_res = {
            "available": True,
            "predicted_career": "Software Developer",
            "confidence_score": 30.0
        }
        hybrid = compute_hybrid_guidance(rule_res, ml_res)
        self.assertTrue(hybrid["hybrid_available"])
        self.assertFalse(hybrid["consensus"])
        self.assertEqual(hybrid["status"], "DIVERGENT")

    def test_hybrid_guidance_when_ml_offline(self):
        """Verify compute_hybrid_guidance handles offline ML gracefully."""
        rule_res = {
            "primary_recommendation": {
                "career": "Data Analyst",
                "match_percentage": 88
            }
        }
        ml_res = {"available": False}
        hybrid = compute_hybrid_guidance(rule_res, ml_res)
        self.assertFalse(hybrid["hybrid_available"])
        self.assertEqual(hybrid["status"], "RULE_ONLY")
        self.assertEqual(hybrid["hybrid_score"], 88)


class TestFlaskMLIntegration(unittest.TestCase):
    """Integration tests for Flask routes verifying ML and Rule-Based coexistence."""

    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

    def test_demo_route_presents_both_rule_and_ml_sections(self):
        """GET /demo should render results page containing both rule-based and ML outputs."""
        response = self.client.get("/demo")
        self.assertEqual(response.status_code, 200)
        html = response.data.decode("utf-8")
        
        # Rule-based elements
        self.assertIn("Career Intelligence Report: Demo Student", html)
        self.assertIn("Data Analyst", html)
        self.assertIn("88% Match", html)
        self.assertIn("Rule-Based", html)

        # ML elements
        self.assertIn("MACHINE LEARNING CAREER PREDICTION", html)
        self.assertIn("Random Forest Classifier", html)
        self.assertIn("DUAL-PERSPECTIVE SYNTHESIS", html)
        self.assertIn("Test Accuracy", html)
        self.assertIn("Weighted F1-Score", html)

    def test_analyze_post_executes_ml_and_rule_analysis(self):
        """POST /analyze with student form data executes both engines and returns 200."""
        form_data = {
            "name": "Alex Chen",
            "branch": "CSE",
            "academic_year": "3rd Year",
            "cgpa": "8.4",
            "skills": "Python, SQL, Machine Learning, Statistics",
            "soft_skills": "Communication, Problem Solving",
            "interests": "Data Science, Analytics, AI",
            "career_preference": "Data Analyst"
        }
        response = self.client.post("/analyze", data=form_data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        html = response.data.decode("utf-8")
        
        self.assertIn("Alex Chen", html)
        self.assertIn("MACHINE LEARNING CAREER PREDICTION", html)
        self.assertIn("DUAL-PERSPECTIVE SYNTHESIS", html)
        self.assertIn("Print Report", html)

    def test_error_handler_404_clean_response(self):
        """Accessing a non-existent route should return 404 without raw server stack trace."""
        response = self.client.get("/non_existent_endpoint_xyz")
        self.assertEqual(response.status_code, 404)
        html = response.data.decode("utf-8")
        self.assertIn("The requested page was not found (404)", html)
        self.assertNotIn("Traceback (most recent call last)", html)


if __name__ == "__main__":
    unittest.main()
