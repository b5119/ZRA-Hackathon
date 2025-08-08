import os
import pandas as pd

base_path = "C:/Users/Administrator/ZRA-Hackathon/Mock_data/"   # Adjust to match your actual folder path

# File paths (all 5 included)
file_paths = [
    #"company_paye_data_with_province.csv",
    "NAPSA_dataset",
    #"pacra_company_registry.csv",
    #"paye_with_edge_cases.csv",  # Included
]

# Column ordering logic
def reorder_columns(df):
    columns = df.columns.tolist()
    
    # Key columns if they exist (priority order)
    first_cols = [col for col in ["Full Name", "NRC"] if col in columns]
    company_cols = [col for col in ["Company Name", "Business Name"] if col in columns]
    tpin_col = ["TPIN"] if "TPIN" in columns else []
    last_col = ["Province"] if "Province" in columns else []
    
    # Any remaining columns (unspecified ones)
    known_cols = first_cols + company_cols + tpin_col + last_col
    unspecified_cols = [col for col in columns if col not in known_cols]
    
    # Build the final order:
    # 1. First priority columns (Full Name, NRC)
    # 2. Company columns (Company Name, Business Name) 
    # 3. TPIN column
    # 4. Unspecified columns (placed in middle, around 3rd-4th position)
    # 5. Province column (last)
    
    new_order = first_cols + company_cols + tpin_col + unspecified_cols + last_col
    
    return df[new_order]

# Clean each file in place
for filename in file_paths:
    file_path = os.path.join(base_path, filename)
    
    # Add .csv extension if not present
    if not filename.endswith('.csv'):
        file_path += '.csv'
    
    try:
        df = pd.read_csv(file_path)
        reordered_df = reorder_columns(df)
        reordered_df.to_csv(file_path, index=False)  # Overwrites original file
        print(f"Cleaned and saved: {filename}")
        print(f"Column order: {list(reordered_df.columns)}")
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"Error processing {filename}: {str(e)}")