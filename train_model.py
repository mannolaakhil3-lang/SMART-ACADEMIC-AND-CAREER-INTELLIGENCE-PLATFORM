"""
Model Training & Evaluation Script
Smart Academic and Career Intelligence Platform (Team G-2)

Executes genuine supervised learning:
1. Loads dataset (data/career_dataset.csv)
2. Splits into Train (75%) and Test (25%) using train_test_split(random_state=42, stratify=y)
3. Trains scikit-learn RandomForestClassifier
4. Evaluates on unseen test set: Accuracy, Precision, Recall, F1-Score, Confusion Matrix
5. Saves trained model to models/career_model.joblib & models/model_metrics.json
6. Runs a test inference on the canonical Demo Student profile.
"""

import os
import sys
import json
from ml_model import (
    train_and_save_pipeline,
    predict_career,
    DATA_PATH,
    MODEL_PATH,
    METRICS_PATH,
    FEATURE_COLUMNS
)

# Canonical Demo Student Profile for Team G-2 Benchmark
DEMO_STUDENT = {
    "name": "Demo Student",
    "branch": "CSE",
    "academic_year": "3rd Year",
    "cgpa": "8.2",
    "skills": ["Python", "SQL", "Problem Solving"],
    "soft_skills": ["Communication", "Teamwork"],
    "interests": ["Technology", "Data Science", "Analytics"],
    "career_preference": "Data Analyst"
}

def main():
    print("=" * 70)
    print("TEAM G-2: TRAINING RANDOM FOREST CAREER CLASSIFIER")
    print("=" * 70)
    print(f"Dataset path: {DATA_PATH}")
    print(f"Features: {len(FEATURE_COLUMNS)} features")
    
    # Check if dataset exists, if not generate it
    if not os.path.exists(DATA_PATH):
        print("Dataset not found. Generating data/career_dataset.csv...")
        from data.generate_dataset import generate_dataset
        generate_dataset(DATA_PATH)
        
    print("\n--- 1. Training & Evaluation Pipeline ---")
    metrics = train_and_save_pipeline(
        dataset_path=DATA_PATH,
        model_save_path=MODEL_PATH,
        metrics_save_path=METRICS_PATH,
        test_size=0.25,
        random_state=42
    )
    
    print("\n[+] MODEL TRAINING COMPLETE!")
    print(f"Model Architecture: {metrics['model_name']}")
    print(f"Total Dataset Samples: {metrics['total_samples']}")
    print(f"Training Samples: {metrics['train_samples']} (75%)")
    print(f"Test Samples: {metrics['test_samples']} (25%)")
    print(f"Career Classes ({len(metrics['classes'])}): {', '.join(metrics['classes'])}")
    
    print("\n--- 2. Measured Test Set Performance Metrics ---")
    print(f"  • Model Test Accuracy: {metrics['accuracy']:.2f}%")
    print(f"  • Weighted Precision:  {metrics['precision']:.2f}%")
    print(f"  • Weighted Recall:     {metrics['recall']:.2f}%")
    print(f"  • Weighted F1-Score:   {metrics['f1_score']:.2f}%")
    
    print("\n--- 3. Top 5 Feature Importances (Model Contribution Indicators) ---")
    for idx, item in enumerate(metrics["feature_importances"][:5], 1):
        print(f"  {idx}. {item['label']} ({item['feature']}): {item['importance']}%")
        
    print("\n--- 4. Confusion Matrix ---")
    print("Classes in order:", metrics["classes"])
    for row in metrics["confusion_matrix"]:
        print(" ", row)
        
    print("\n--- 5. Inference Test on Canonical Demo Student Profile ---")
    print(f"Student: {DEMO_STUDENT['name']} (CGPA {DEMO_STUDENT['cgpa']})")
    print(f"Skills:  {', '.join(DEMO_STUDENT['skills'])}")
    print(f"Interests: {', '.join(DEMO_STUDENT['interests'])}")
    
    prediction = predict_career(DEMO_STUDENT)
    if prediction.get("available"):
        print(f"\n[+] ML PREDICTED CAREER: {prediction['predicted_career']}")
        print(f"[+] PREDICTION CONFIDENCE: {prediction['confidence_score']}%")
        print("\nAll Class Probabilities:")
        for item in prediction["career_probabilities"]:
            print(f"   - {item['career']}: {item['probability']}%")
    else:
        print(f"[-] Prediction failed: {prediction.get('message')}")
        
    print("\n" + "=" * 70)
    print("Artifacts generated:")
    print(f"  * Model bundle: {MODEL_PATH}")
    print(f"  * Metrics JSON: {METRICS_PATH}")
    print("=" * 70)

if __name__ == "__main__":
    main()
