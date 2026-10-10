"""
Machine Learning Module for Academic and Career Intelligence Platform
Team: G-2

Supervised Machine Learning system utilizing scikit-learn RandomForestClassifier.
Provides feature engineering, model training, test evaluation, persistence,
and real-time inference with probability calibration and feature contribution indicators.

DISCLAIMER: The dataset used for model training is a synthetic/demo dataset created
specifically for academic project validation.
"""

import os
import json
import logging
from typing import Dict, Any, List, Tuple, Optional
import numpy as np
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)

logger = logging.getLogger(__name__)

# Standard model and data paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "career_dataset.csv")
MODEL_DIR = os.path.join(BASE_DIR, "models")
MODEL_PATH = os.path.join(MODEL_DIR, "career_model.joblib")
METRICS_PATH = os.path.join(MODEL_DIR, "model_metrics.json")

# Model feature schema
FEATURE_COLUMNS: List[str] = [
    "cgpa",
    "python",
    "sql",
    "java",
    "cpp",
    "javascript",
    "machine_learning",
    "statistics",
    "data_visualization",
    "communication",
    "problem_solving",
    "leadership",
    "cloud_computing",
    "cybersecurity",
    "ui_ux_design",
    "technology_interest",
    "data_science_interest",
    "business_interest",
    "design_interest",
    "research_interest",
    "security_interest"
]

TARGET_COLUMN: str = "career"

# Human-readable labels for features
FEATURE_LABELS: Dict[str, str] = {
    "cgpa": "Academic CGPA",
    "python": "Python Programming",
    "sql": "SQL & Relational Databases",
    "java": "Java Development",
    "cpp": "C++ & System Programming",
    "javascript": "JavaScript & Web Tech",
    "machine_learning": "Machine Learning & AI",
    "statistics": "Applied Statistics & Probability",
    "data_visualization": "Data Visualization & Dashboards",
    "communication": "Professional Communication",
    "problem_solving": "Algorithmic & Problem Solving",
    "leadership": "Leadership & Project Coordination",
    "cloud_computing": "Cloud Computing & DevOps",
    "cybersecurity": "Cybersecurity & Network Defense",
    "ui_ux_design": "UI/UX & User-Centered Design",
    "technology_interest": "Technology Passion",
    "data_science_interest": "Data Science & Analytics Passion",
    "business_interest": "Business & Strategy Passion",
    "design_interest": "Design & Aesthetics Passion",
    "research_interest": "Research & Theory Passion",
    "security_interest": "Information Security Passion"
}

# Synonyms for mapping unstructured student strings into binary features
SKILL_SYNONYMS: Dict[str, List[str]] = {
    "python": ["python", "py", "pandas", "numpy"],
    "sql": ["sql", "mysql", "postgresql", "postgres", "sqlite", "oracle", "database"],
    "java": ["java", "spring", "springboot"],
    "cpp": ["c++", "cpp", "c", "c programming"],
    "javascript": ["javascript", "js", "typescript", "ts", "react", "node", "nodejs", "html", "css", "web development"],
    "machine_learning": ["machine learning", "ml", "deep learning", "dl", "artificial intelligence", "ai", "scikit-learn", "tensorflow", "pytorch", "nlp", "computer vision"],
    "statistics": ["statistics", "stats", "probability", "mathematics", "math", "linear algebra"],
    "data_visualization": ["data visualization", "visualization", "tableau", "power bi", "powerbi", "matplotlib", "seaborn", "excel"],
    "communication": ["communication", "presentation", "verbal communication", "writing", "interpersonal"],
    "problem_solving": ["problem solving", "problem-solving", "analytical", "analytical thinking", "dsa", "data structures", "algorithms"],
    "leadership": ["leadership", "management", "team lead", "project management", "agile", "scrum", "teamwork"],
    "cloud_computing": ["cloud", "cloud computing", "aws", "azure", "gcp", "devops", "docker", "kubernetes", "linux", "ci/cd"],
    "cybersecurity": ["cybersecurity", "security", "ethical hacking", "network security", "cryptography", "infosec", "penetration testing"],
    "ui_ux_design": ["ui", "ux", "ui/ux", "design", "figma", "wireframing", "prototyping", "user research", "product design"]
}

INTEREST_SYNONYMS: Dict[str, List[str]] = {
    "technology_interest": ["technology", "tech", "software", "coding", "computers", "it", "web", "systems"],
    "data_science_interest": ["data science", "analytics", "data", "big data", "business intelligence", "machine learning", "ai"],
    "business_interest": ["business", "management", "finance", "consulting", "economics", "strategy", "marketing", "operations"],
    "design_interest": ["design", "ui", "ux", "ui/ux", "graphic design", "creative", "art", "user experience"],
    "research_interest": ["research", "academia", "algorithms", "scientific", "theory", "deep learning", "papers"],
    "security_interest": ["security", "cybersecurity", "ethical hacking", "forensics", "privacy", "defense"]
}


def load_dataset(filepath: str = DATA_PATH) -> pd.DataFrame:
    """Load the project dataset from disk and validate required columns."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Dataset file not found at: {filepath}")
    
    df = pd.read_csv(filepath)
    expected_cols = set(FEATURE_COLUMNS + [TARGET_COLUMN])
    actual_cols = set(df.columns)
    
    missing = expected_cols - actual_cols
    if missing:
        raise ValueError(f"Dataset missing required columns: {missing}")
    
    return df


def preprocess_data(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
    """Preprocess dataset: separate features X and labels y, handle missing values."""
    # Check and impute missing values if any exist
    clean_df = df.copy()
    
    if clean_df[FEATURE_COLUMNS].isnull().any().any():
        for col in FEATURE_COLUMNS:
            if col == "cgpa":
                clean_df[col] = clean_df[col].fillna(clean_df[col].mean())
            else:
                clean_df[col] = clean_df[col].fillna(0)
    
    X = clean_df[FEATURE_COLUMNS]
    y = clean_df[TARGET_COLUMN]
    return X, y


def extract_features_from_student(student_data: Dict[str, Any]) -> pd.DataFrame:
    """
    Transform raw student inputs into model-compatible feature DataFrame.
    Normalizes tokenized skills, soft skills, interests, and academic CGPA.
    """
    # Extract CGPA
    try:
        cgpa_val = float(student_data.get("cgpa", 0.0))
        cgpa_val = max(0.0, min(10.0, cgpa_val))
    except (ValueError, TypeError):
        cgpa_val = 7.5  # fallback reasonable average

    # Gather skills text
    skills_raw = student_data.get("skills", [])
    if isinstance(skills_raw, str):
        skills_raw = [s.strip().lower() for s in skills_raw.split(",") if s.strip()]
    else:
        skills_raw = [str(s).strip().lower() for s in skills_raw]

    soft_skills_raw = student_data.get("soft_skills", [])
    if isinstance(soft_skills_raw, str):
        soft_skills_raw = [s.strip().lower() for s in soft_skills_raw.split(",") if s.strip()]
    else:
        soft_skills_raw = [str(s).strip().lower() for s in soft_skills_raw]

    all_student_skills = skills_raw + soft_skills_raw

    # Gather interests text
    interests_raw = student_data.get("interests", [])
    if isinstance(interests_raw, str):
        interests_raw = [s.strip().lower() for s in interests_raw.split(",") if s.strip()]
    else:
        interests_raw = [str(s).strip().lower() for s in interests_raw]

    features: Dict[str, Any] = {"cgpa": cgpa_val}

    # Match skills against synonyms
    for feat, syns in SKILL_SYNONYMS.items():
        matched = 0
        for student_skill in all_student_skills:
            if any(syn in student_skill or student_skill in syn for syn in syns):
                matched = 1
                break
        features[feat] = matched

    # Match interests against synonyms
    for feat, syns in INTEREST_SYNONYMS.items():
        matched = 0
        for student_interest in interests_raw:
            if any(syn in student_interest or student_interest in syn for syn in syns):
                matched = 1
                break
        features[feat] = matched

    # Build 1-row DataFrame preserving exact column order
    return pd.DataFrame([features])[FEATURE_COLUMNS]


def train_model(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    random_state: int = 42,
    n_estimators: int = 100,
    max_depth: Optional[int] = 10
) -> RandomForestClassifier:
    """Train a scikit-learn RandomForestClassifier on training split."""
    model = RandomForestClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        min_samples_split=4,
        min_samples_leaf=2,
        random_state=random_state,
        class_weight="balanced"
    )
    model.fit(X_train, y_train)
    return model


def evaluate_model(
    model: RandomForestClassifier,
    X_test: pd.DataFrame,
    y_test: pd.Series
) -> Dict[str, Any]:
    """
    Evaluate the model on unseen test data.
    Computes genuine Accuracy, Precision, Recall, F1-Score, and Confusion Matrix.
    """
    y_pred = model.predict(X_test)
    
    acc = float(accuracy_score(y_test, y_pred))
    prec = float(precision_score(y_test, y_pred, average="weighted", zero_division=0))
    rec = float(recall_score(y_test, y_pred, average="weighted", zero_division=0))
    f1 = float(f1_score(y_test, y_pred, average="weighted", zero_division=0))
    
    cm = confusion_matrix(y_test, y_pred)
    classes = list(model.classes_)
    
    clf_report = classification_report(y_test, y_pred, output_dict=True, zero_division=0)
    
    # Feature importances
    importances = model.feature_importances_
    feat_imp = sorted(
        [
            {
                "feature": col,
                "label": FEATURE_LABELS.get(col, col),
                "importance": round(float(imp) * 100, 2)
            }
            for col, imp in zip(X_test.columns, importances)
        ],
        key=lambda x: x["importance"],
        reverse=True
    )

    metrics = {
        "model_name": "Random Forest Classifier",
        "accuracy": round(acc * 100, 2),
        "precision": round(prec * 100, 2),
        "recall": round(rec * 100, 2),
        "f1_score": round(f1 * 100, 2),
        "test_samples": len(y_test),
        "train_samples": None,  # Populated during pipeline
        "total_samples": None,
        "classes": classes,
        "confusion_matrix": cm.tolist(),
        "classification_report": clf_report,
        "feature_importances": feat_imp,
        "dataset_disclaimer": "Synthetic/Demo Dataset created for academic project validation."
    }
    return metrics


def train_and_save_pipeline(
    dataset_path: str = DATA_PATH,
    model_save_path: str = MODEL_PATH,
    metrics_save_path: str = METRICS_PATH,
    test_size: float = 0.25,
    random_state: int = 42
) -> Dict[str, Any]:
    """
    Full ML lifecycle pipeline:
    Loads dataset, splits 75/25 with stratification, trains Random Forest,
    evaluates on test split, and persists artifact and metrics JSON.
    """
    df = load_dataset(dataset_path)
    X, y = preprocess_data(df)
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=test_size,
        random_state=random_state,
        stratify=y
    )
    
    model = train_model(X_train, y_train, random_state=random_state)
    metrics = evaluate_model(model, X_test, y_test)
    metrics["train_samples"] = len(X_train)
    metrics["total_samples"] = len(df)
    
    # Ensure destination directories exist
    os.makedirs(os.path.dirname(model_save_path), exist_ok=True)
    os.makedirs(os.path.dirname(metrics_save_path), exist_ok=True)
    
    # Persist model bundle
    bundle = {
        "model": model,
        "feature_columns": FEATURE_COLUMNS,
        "classes": list(model.classes_),
        "metrics": metrics
    }
    joblib.dump(bundle, model_save_path)
    
    # Persist human-readable metrics JSON
    with open(metrics_save_path, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)
        
    logger.info(f"Model successfully saved to {model_save_path}")
    logger.info(f"Metrics saved to {metrics_save_path}")
    return metrics


class CareerMLPredictor:
    """Singleton service to load the trained model into memory and run fast predictions."""
    
    _instance: Optional["CareerMLPredictor"] = None
    
    def __init__(self, model_path: str = MODEL_PATH, metrics_path: str = METRICS_PATH):
        self.model_path = model_path
        self.metrics_path = metrics_path
        self.bundle: Optional[Dict[str, Any]] = None
        self.model: Optional[RandomForestClassifier] = None
        self.metrics: Dict[str, Any] = {}
        self.load_model()

    @classmethod
    def get_instance(cls) -> "CareerMLPredictor":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def load_model(self) -> bool:
        """Attempt to load trained model bundle and metrics. Graceful failure on missing file."""
        if not os.path.exists(self.model_path):
            logger.warning(f"ML Model file not found at {self.model_path}.")
            self.model = None
            return False
            
        try:
            self.bundle = joblib.load(self.model_path)
            self.model = self.bundle["model"]
            self.metrics = self.bundle.get("metrics", {})
            return True
        except Exception as e:
            logger.error(f"Error loading ML model from {self.model_path}: {e}")
            self.model = None
            return False

    def is_available(self) -> bool:
        return self.model is not None

    def predict(self, student_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute career prediction on student profile.
        Returns predicted career, probability distribution, and active feature contributions.
        """
        if not self.is_available():
            # Try reloading once in case model was just trained
            if not self.load_model():
                return {
                    "available": False,
                    "message": "ML prediction is temporarily unavailable. Continuing with rule-based career analysis.",
                    "error": "Model bundle not loaded"
                }

        try:
            X = extract_features_from_student(student_data)
            pred_class = self.model.predict(X)[0]
            probs = self.model.predict_proba(X)[0]
            classes = list(self.model.classes_)
            
            # Map probabilities per class
            class_prob_map = {
                cls_name: round(float(prob) * 100, 1)
                for cls_name, prob in zip(classes, probs)
            }
            sorted_probs = sorted(
                [{"career": k, "probability": v} for k, v in class_prob_map.items()],
                key=lambda x: x["probability"],
                reverse=True
            )
            
            # Find student's active features and their model importance
            student_features = X.iloc[0].to_dict()
            active_features = []
            importances_dict = {
                item["feature"]: item["importance"]
                for item in self.metrics.get("feature_importances", [])
            }
            
            for feat, val in student_features.items():
                if (feat == "cgpa" and val >= 7.0) or (feat != "cgpa" and val == 1):
                    active_features.append({
                        "feature": feat,
                        "label": FEATURE_LABELS.get(feat, feat),
                        "value": val,
                        "model_importance": importances_dict.get(feat, 0.0)
                    })
            
            active_features.sort(key=lambda x: x["model_importance"], reverse=True)
            top_active = active_features[:6]
            
            highest_prob = class_prob_map.get(pred_class, 0.0)
            
            return {
                "available": True,
                "model_name": "Random Forest Classifier",
                "predicted_career": pred_class,
                "confidence_score": highest_prob,
                "career_probabilities": sorted_probs,
                "active_features": top_active,
                "metrics": {
                    "accuracy": self.metrics.get("accuracy", 0.0),
                    "precision": self.metrics.get("precision", 0.0),
                    "recall": self.metrics.get("recall", 0.0),
                    "f1_score": self.metrics.get("f1_score", 0.0),
                    "test_samples": self.metrics.get("test_samples", 0),
                    "total_samples": self.metrics.get("total_samples", 0),
                    "dataset_disclaimer": "Synthetic/Demo Dataset created for academic project validation."
                }
            }
        except Exception as e:
            logger.error(f"Error executing ML prediction: {e}")
            return {
                "available": False,
                "message": "ML prediction is temporarily unavailable. Continuing with rule-based career analysis.",
                "error": str(e)
            }


def predict_career(student_data: Dict[str, Any]) -> Dict[str, Any]:
    """Helper function to run ML prediction on student profile."""
    predictor = CareerMLPredictor.get_instance()
    return predictor.predict(student_data)


def compute_hybrid_guidance(
    rule_results: Dict[str, Any],
    ml_results: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Computes transparent hybrid recommendation comparing Rule-Based Engine and ML Model.
    Architecture:
    - Rule-based primary recommendation (e.g. Data Analyst, 88% Match)
    - ML predicted career (e.g. Data Analyst, 78% Confidence)
    - Consensus evaluation and optional transparent hybrid score.
    """
    rule_primary = rule_results.get("primary_recommendation", {})
    rule_career = rule_primary.get("career", "N/A")
    rule_score = rule_primary.get("match_percentage", 0)
    
    if not ml_results.get("available", False):
        return {
            "hybrid_available": False,
            "status": "RULE_ONLY",
            "message": "ML prediction is currently unavailable. Relying solely on deterministic rule-based evaluation.",
            "rule_career": rule_career,
            "rule_score": rule_score,
            "ml_career": None,
            "ml_confidence": None,
            "consensus": False,
            "hybrid_score": rule_score
        }
        
    ml_career = ml_results.get("predicted_career", "N/A")
    ml_confidence = ml_results.get("confidence_score", 0.0)
    
    # Check consensus
    is_consensus = (rule_career.lower() == ml_career.lower())
    
    # Calculate transparent combined hybrid score:
    # 70% Rule-Based Match + 30% ML Probability
    hybrid_score = round((0.70 * rule_score) + (0.30 * ml_confidence), 1)
    
    if is_consensus:
        status = "CONSENSUS_AGREED"
        badge = "High-Confidence Consensus"
        message = (
            f"Both the deterministic rule-based evaluation and the trained Random Forest classifier "
            f"converge on recommending '{rule_career}' as your optimal career pathway."
        )
    else:
        status = "DIVERGENT"
        badge = "Dual-Perspective Guidance"
        message = (
            "The rule-based engine and ML model produced different recommendations. "
            "The result should be interpreted as decision support rather than a definitive career decision."
        )
        
    return {
        "hybrid_available": True,
        "status": status,
        "badge": badge,
        "message": message,
        "rule_career": rule_career,
        "rule_score": rule_score,
        "ml_career": ml_career,
        "ml_confidence": ml_confidence,
        "consensus": is_consensus,
        "hybrid_score": hybrid_score,
        "formula_explanation": "0.70 × Rule-Based Score + 0.30 × ML Probability"
    }
