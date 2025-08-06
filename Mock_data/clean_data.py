import os
import pandas as pd

base_path = base_path = "C:/Users/Administrator/ZRA-Hackathon/Mock_data/"
  # Adjust to match your actual folder path

# File paths (all 5 included)
file_paths = [
    "company_paye_data_with_province.csv",
    "fake_nrc_tpin_dataset.csv",
    "fake_nrc_tpin_with_province.csv",
    "pacra_company_registry.csv",
    "paye_with_edge_cases.csv",  # Included
]

# Column ordering logic
def reorder_columns(df):
    columns = df.columns.tolist()

    # Key columns if they exist
    first_cols = [col for col in ["Full Name", "NRC"] if col in columns]
    company_cols = [col for col in ["Company Name", "Business Name"] if col in columns]
    tpin_col = ["TPIN"] if "TPIN" in columns else []
    last_col = ["Province"] if "Province" in columns else []

    # Any remaining columns
    known_cols = first_cols + company_cols + tpin_col + last_col
    middle_cols = [col for col in columns if col not in known_cols]

    # Final ordered list
    new_order = first_cols + company_cols + tpin_col + middle_cols + last_col
    return df[new_order]

# Clean each file in place
for filename in file_paths:
    file_path = os.path.join(base_path, filename)
    df = pd.read_csv(file_path)
    reordered_df = reorder_columns(df)
    reordered_df.to_csv(file_path, index=False)  # Overwrites original file
    print(f"Cleaned and saved: {filename}")
