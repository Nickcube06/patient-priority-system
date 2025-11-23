import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Patient System",
    page_icon="🏥",
    layout="centered"
)

# Title and Description
st.title("Patient System")
st.markdown("Enter patient details below and click **Calculate** to determine treatment priority.")

# Initialize session state for the dataframe if it doesn't exist
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame(
        [
            {"Patient": "", "Age": 0, "Condition": "mild", "Sickness": "Unknown"},
        ]
    )

# Define options for dropdowns
condition_options = ["lethal", "moderate", "mild"]
sickness_options = [
    "Heart Attack", 
    "Stroke", 
    "ACV",
    "Cancer",
    "Kidney Disease",
    "EPOC",
    "Diabetes",
    "Neumonía",
    "Covid",
    "Burn", 
    "Fracture", 
    "Flu", 
    "Allergic Reaction", 
    "Unknown"
]

# Data Editor for Patient Input
st.subheader("Patient Entry")
edited_df = st.data_editor(
    st.session_state.df,
    num_rows="dynamic",
    column_config={
        "Patient": st.column_config.TextColumn(
            "Patient Name",
            help="Enter the name of the patient",
            required=True,
            validate="^.+$"
        ),
        "Age": st.column_config.NumberColumn(
            "Age",
            min_value=0,
            max_value=120,
            step=1,
            required=True
        ),
        "Condition": st.column_config.SelectboxColumn(
            "Condition Severity",
            help="Select the severity of the condition",
            width="medium",
            options=condition_options,
            required=True
        ),
        "Sickness": st.column_config.SelectboxColumn(
            "Sickness Type",
            help="Select the type of sickness",
            width="medium",
            options=sickness_options,
            required=True
        )
    },
    hide_index=True,
    use_container_width=True
)

# Calculate Button
if st.button("Calculate Treatment Order", type="primary"):
    # Filter out empty rows where Patient name is empty
    valid_patients = edited_df[edited_df["Patient"] != ""].copy()
    
    if valid_patients.empty:
        st.warning("Please enter at least one patient with a name.")
    else:
        from functools import cmp_to_key

        # 1. Define Severity Maps for Comparison
        condition_map = {
            "lethal": 3,
            "moderate": 2,
            "mild": 1
        }
        
        sickness_map = {
            "Heart Attack": 10,
            "Stroke": 9,
            "ACV": 9,
            "Cancer": 8,
            "Kidney Disease": 7,
            "EPOC": 7,
            "Diabetes": 6,
            "Neumonía": 6,
            "Covid": 5,
            "Burn": 5,
            "Fracture": 4,
            "Flu": 3,
            "Allergic Reaction": 2,
            "Unknown": 1
        }

        # Pre-calculate scores for efficient comparison
        valid_patients["Condition_Score"] = valid_patients["Condition"].map(condition_map).fillna(0)
        valid_patients["Sickness_Score"] = valid_patients["Sickness"].map(sickness_map).fillna(0)

        # Custom Comparator Function
        def compare_patients(row1, row2):
            # row1 and row2 are pandas Series or dicts
            score1 = 0
            score2 = 0
            
            # Criteria 1: Age (Older is riskier)
            if row1["Age"] > row2["Age"]:
                score1 += 1
            elif row2["Age"] > row1["Age"]:
                score2 += 1
                
            # Criteria 2: Condition (Worse is riskier)
            if row1["Condition_Score"] > row2["Condition_Score"]:
                score1 += 1
            elif row2["Condition_Score"] > row1["Condition_Score"]:
                score2 += 1
                
            # Criteria 3: Sickness (More lethal is riskier)
            if row1["Sickness_Score"] > row2["Sickness_Score"]:
                score1 += 1
            elif row2["Sickness_Score"] > row1["Sickness_Score"]:
                score2 += 1
            
            # Return comparison result
            # If score1 > score2, row1 is "greater" (higher risk) -> return 1
            # If score2 > score1, row2 is "greater" -> return -1
            # If equal, return 0
            return score1 - score2

        # Convert DataFrame to list of dicts for sorting
        patients_list = valid_patients.to_dict('records')
        
        # Sort using the custom comparator
        # reverse=True because we want the "highest risk" (positive comparison result) first
        sorted_list = sorted(patients_list, key=cmp_to_key(compare_patients), reverse=True)
        
        # Create sorted DataFrame
        sorted_patients = pd.DataFrame(sorted_list)
        
        # Display Results
        st.divider()
        st.subheader("📋 Treatment Priority List")
        
        # Display the sorted list
        st.dataframe(
            sorted_patients[["Patient", "Age", "Condition", "Sickness"]],
            use_container_width=True,
            hide_index=True
        )
