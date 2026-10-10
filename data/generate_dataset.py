"""
Dataset Generator for Academic Career Intelligence Platform
Team: G-2
Generates a realistic, synthetic dataset of student academic, skill, and interest profiles.
DISCLAIMER: Synthetic/Demo Dataset created for academic project validation.
"""

import os
import random
import numpy as np
import pandas as pd

# Set deterministic random seed for academic reproducibility
RANDOM_SEED = 42
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)

CAREERS = [
    "Data Analyst",
    "Software Developer",
    "AI/ML Engineer",
    "Cybersecurity Analyst",
    "UI/UX Designer",
    "Business Analyst"
]

SAMPLES_PER_CAREER = 100  # Total 600 records

def generate_student_record(career: str) -> dict:
    """Generate a realistic synthetic student profile conditioned on career target."""
    record = {
        "cgpa": 0.0,
        "python": 0,
        "sql": 0,
        "java": 0,
        "cpp": 0,
        "javascript": 0,
        "machine_learning": 0,
        "statistics": 0,
        "data_visualization": 0,
        "communication": 0,
        "problem_solving": 0,
        "leadership": 0,
        "cloud_computing": 0,
        "cybersecurity": 0,
        "ui_ux_design": 0,
        "technology_interest": 0,
        "data_science_interest": 0,
        "business_interest": 0,
        "design_interest": 0,
        "research_interest": 0,
        "security_interest": 0,
        "career": career
    }

    # Helper function to sample binary with probability p
    b = lambda p: 1 if random.random() < p else 0

    if career == "Data Analyst":
        record["cgpa"] = round(np.clip(np.random.normal(8.0, 0.6), 6.5, 9.8), 2)
        record["python"] = b(0.85)
        record["sql"] = b(0.92)
        record["java"] = b(0.20)
        record["cpp"] = b(0.15)
        record["javascript"] = b(0.25)
        record["machine_learning"] = b(0.35)
        record["statistics"] = b(0.80)
        record["data_visualization"] = b(0.88)
        record["communication"] = b(0.82)
        record["problem_solving"] = b(0.85)
        record["leadership"] = b(0.35)
        record["cloud_computing"] = b(0.20)
        record["cybersecurity"] = b(0.08)
        record["ui_ux_design"] = b(0.30)
        record["technology_interest"] = b(0.75)
        record["data_science_interest"] = b(0.95)
        record["business_interest"] = b(0.70)
        record["design_interest"] = b(0.30)
        record["research_interest"] = b(0.25)
        record["security_interest"] = b(0.10)

    elif career == "Software Developer":
        record["cgpa"] = round(np.clip(np.random.normal(7.9, 0.7), 6.2, 9.9), 2)
        record["python"] = b(0.75)
        record["sql"] = b(0.65)
        record["java"] = b(0.85)
        record["cpp"] = b(0.78)
        record["javascript"] = b(0.70)
        record["machine_learning"] = b(0.20)
        record["statistics"] = b(0.30)
        record["data_visualization"] = b(0.20)
        record["communication"] = b(0.65)
        record["problem_solving"] = b(0.92)
        record["leadership"] = b(0.35)
        record["cloud_computing"] = b(0.35)
        record["cybersecurity"] = b(0.20)
        record["ui_ux_design"] = b(0.25)
        record["technology_interest"] = b(0.95)
        record["data_science_interest"] = b(0.30)
        record["business_interest"] = b(0.25)
        record["design_interest"] = b(0.25)
        record["research_interest"] = b(0.30)
        record["security_interest"] = b(0.20)

    elif career == "AI/ML Engineer":
        record["cgpa"] = round(np.clip(np.random.normal(8.4, 0.5), 7.0, 9.9), 2)
        record["python"] = b(0.95)
        record["sql"] = b(0.60)
        record["java"] = b(0.30)
        record["cpp"] = b(0.60)
        record["javascript"] = b(0.15)
        record["machine_learning"] = b(0.95)
        record["statistics"] = b(0.90)
        record["data_visualization"] = b(0.70)
        record["communication"] = b(0.70)
        record["problem_solving"] = b(0.95)
        record["leadership"] = b(0.30)
        record["cloud_computing"] = b(0.40)
        record["cybersecurity"] = b(0.10)
        record["ui_ux_design"] = b(0.10)
        record["technology_interest"] = b(0.90)
        record["data_science_interest"] = b(0.98)
        record["business_interest"] = b(0.20)
        record["design_interest"] = b(0.15)
        record["research_interest"] = b(0.85)
        record["security_interest"] = b(0.15)

    elif career == "Cybersecurity Analyst":
        record["cgpa"] = round(np.clip(np.random.normal(7.7, 0.7), 6.2, 9.6), 2)
        record["python"] = b(0.80)
        record["sql"] = b(0.50)
        record["java"] = b(0.40)
        record["cpp"] = b(0.75)
        record["javascript"] = b(0.30)
        record["machine_learning"] = b(0.15)
        record["statistics"] = b(0.35)
        record["data_visualization"] = b(0.15)
        record["communication"] = b(0.65)
        record["problem_solving"] = b(0.90)
        record["leadership"] = b(0.35)
        record["cloud_computing"] = b(0.45)
        record["cybersecurity"] = b(0.95)
        record["ui_ux_design"] = b(0.08)
        record["technology_interest"] = b(0.90)
        record["data_science_interest"] = b(0.20)
        record["business_interest"] = b(0.30)
        record["design_interest"] = b(0.10)
        record["research_interest"] = b(0.40)
        record["security_interest"] = b(0.98)

    elif career == "UI/UX Designer":
        record["cgpa"] = round(np.clip(np.random.normal(7.6, 0.7), 6.0, 9.6), 2)
        record["python"] = b(0.20)
        record["sql"] = b(0.15)
        record["java"] = b(0.10)
        record["cpp"] = b(0.08)
        record["javascript"] = b(0.70)
        record["machine_learning"] = b(0.05)
        record["statistics"] = b(0.20)
        record["data_visualization"] = b(0.75)
        record["communication"] = b(0.90)
        record["problem_solving"] = b(0.75)
        record["leadership"] = b(0.55)
        record["cloud_computing"] = b(0.10)
        record["cybersecurity"] = b(0.05)
        record["ui_ux_design"] = b(0.98)
        record["technology_interest"] = b(0.70)
        record["data_science_interest"] = b(0.15)
        record["business_interest"] = b(0.50)
        record["design_interest"] = b(0.98)
        record["research_interest"] = b(0.35)
        record["security_interest"] = b(0.05)

    elif career == "Business Analyst":
        record["cgpa"] = round(np.clip(np.random.normal(8.0, 0.6), 6.5, 9.8), 2)
        record["python"] = b(0.35)
        record["sql"] = b(0.80)
        record["java"] = b(0.15)
        record["cpp"] = b(0.10)
        record["javascript"] = b(0.20)
        record["machine_learning"] = b(0.10)
        record["statistics"] = b(0.65)
        record["data_visualization"] = b(0.85)
        record["communication"] = b(0.95)
        record["problem_solving"] = b(0.85)
        record["leadership"] = b(0.80)
        record["cloud_computing"] = b(0.15)
        record["cybersecurity"] = b(0.10)
        record["ui_ux_design"] = b(0.35)
        record["technology_interest"] = b(0.65)
        record["data_science_interest"] = b(0.50)
        record["business_interest"] = b(0.98)
        record["design_interest"] = b(0.25)
        record["research_interest"] = b(0.20)
        record["security_interest"] = b(0.10)

    return record

def generate_dataset(output_path: str = "data/career_dataset.csv"):
    """Generate and save the synthetic career dataset."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    rows = []
    for career in CAREERS:
        for _ in range(SAMPLES_PER_CAREER):
            rows.append(generate_student_record(career))
    
    # Shuffle dataset
    random.shuffle(rows)
    df = pd.DataFrame(rows)
    
    # Write metadata comment and CSV content
    df.to_csv(output_path, index=False)
    print(f"Generated {len(df)} records across {len(CAREERS)} careers -> {output_path}")
    print("Class distribution:\n", df["career"].value_counts())
    return df

if __name__ == "__main__":
    generate_dataset()
