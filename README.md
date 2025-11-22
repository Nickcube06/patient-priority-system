# Patient Triage System

A simple Streamlit application to triage patients based on Age, Condition, and Sickness severity using comparison logic.

## Installation
1) Ensure you have Python3 installed.
2) Create virtual environment: "python3 -m venv venv"
3) Install dependencies: "pip install -r requirements.txt"
4) Activate virtual environment 
    (macOS/Linux): "source venv/bin/activate"
    (Windows): "venv\Scripts\activate"

## Running the App

Run the application using Streamlit: "streamlit run app.py"

The application will open in your default web browser.

# Application Logic Explanation

This Patient System is designed to prioritize patients based on a multi-criteria risk assessment. Instead of assigning a single static score to each patient, the system uses a comparison mechanism to determine the relative urgency of treatment.

## How It Works

When you click "Calculate Treatment Order", the system sorts the list of patients by comparing them head-to-head. For any two patients (Patient A and Patient B), the system evaluates them on three distinct criteria:

1.  **Age**: The older patient is considered higher risk.
2.  **Condition Severity**: The severity is ranked as `Lethal > Severe > Non-Lethal`. A worse condition indicates higher risk.
3.  **Sickness Type**: Specific diseases are ranked by their inherent lethality. For example, a Heart Attack is ranked higher than a Fracture, which is ranked higher than the Flu.

### The Comparison System

For each pair of patients, a score is cast for each of the three criteria:
*   If Patient A is older than Patient B, Patient A gets 1 point.
*   If Patient A has a more severe condition, Patient A gets 1 point.
*   If Patient A has a more lethal sickness, Patient A gets 1 point.

The patient with the most points (2 out of 3, or 3 out of 3) is considered the higher priority and is placed higher in the list. This ensures that a patient who is critical in multiple areas is prioritized over someone who might only be critical in one.

## Disclaimer

**IMPORTANT NOTICE**: This application is a theoretical experiment created for educational and demonstration purposes only. It is **NOT** intended for use in real-world medical scenarios, clinical triage, or emergency response. The logic implemented here is a simplified model and does not account for the complexities of actual medical diagnosis and prioritization. The author assumes no responsibility or liability for any consequences resulting from the use of this software in any practical setting.
