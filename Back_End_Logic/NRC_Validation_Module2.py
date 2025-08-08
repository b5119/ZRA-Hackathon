import os
import pandas as pd
import re

# Base directory paths
base_path = "C:/Users/Administrator/ZRA-Hackathon/Mock_data/"
output_dir = "C:/Users/Administrator/ZRA-Hackathon/Back_End_Logic/Processed_Document_Statuses/"

# Input file (file to check)
input_file = "subset_nrc_dataset.csv"  # File you want to validate
input_path = os.path.join(base_path, input_file)

# NRC Database file (reference file)
nrc_database_file = "reference_nrc_dataset.csv"  # Reference file to check against
nrc_database_path = os.path.join(base_path, nrc_database_file)

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# Define possible NRC column names
possible_nrc_columns = ["NRC", "nrc", "Employee NRC", "employee nrc", "NRC Number", "nrc number"]

# List of valid province codes used in NRC generation
valid_province_codes = {
    "01", "02", "03", "04", "05", "06", "07", "08", "09", "10"
}

# NRC validation function (format only)
def validate_nrc_format(nrc):
    """Check if NRC follows correct format pattern"""
    if not isinstance(nrc, str):
        return False
    pattern = r"^(\d{6})/(\d{2})/(\d)$"
    match = re.match(pattern, nrc)
    if not match:
        return False

    prefix, year, citizenship = match.groups()
    province_code = prefix[:2]

    if province_code not in valid_province_codes:
        return False
    if citizenship not in ["1", "2"]:
        return False

    return True

def get_nrc_status(nrc, valid_nrc_set):
    """Simple NRC validation - Valid or Invalid only"""
    if pd.isna(nrc) or str(nrc).strip() == '':
        return "Invalid"
    
    nrc_str = str(nrc).strip()
    format_valid = validate_nrc_format(nrc_str)
    in_database = nrc_str in valid_nrc_set
    
    # Simple Valid/Invalid logic
    if format_valid and in_database:
        return "Valid"
    else:
        return "Invalid"

# Load NRC database (like Home Affairs database)
valid_nrc_set = set()
try:
    nrc_db_df = pd.read_csv(nrc_database_path)
    print(f"Loaded NRC database: {nrc_database_file}")
    print("NRC database columns:", list(nrc_db_df.columns))
    
    # Find NRC column in database
    nrc_db_col = None
    for col in nrc_db_df.columns:
        if col in possible_nrc_columns or "NRC" in col.upper():
            nrc_db_col = col
            break
    
    if nrc_db_col:
        valid_nrc_set = set(nrc_db_df[nrc_db_col].astype(str).str.strip())
        print(f"Loaded {len(valid_nrc_set)} valid NRCs from database")
    else:
        print("Warning: No NRC column found in database file")
        
except FileNotFoundError:
    print(f"Warning: NRC database not found: {nrc_database_path}")
    print("Available files:")
    for f in os.listdir(base_path):
        if f.endswith('.csv'):
            print(f"  - {f}")
    print("Continuing with format validation only...")

# Load input file with error handling
try:
    df = pd.read_csv(input_path)
    print(f"\nSuccessfully loaded: {input_file}")
    print("Available columns:", list(df.columns))
except FileNotFoundError:
    print(f"Error: Input file not found: {input_path}")
    print("Available files in directory:")
    for f in os.listdir(base_path):
        if f.endswith('.csv'):
            print(f"  - {f}")
    exit()

# Automatically detect the NRC column (handle variations)
nrc_col = None

for col in df.columns:
    if col in possible_nrc_columns:
        nrc_col = col
        break
    # Also check if column contains "NRC"
    elif "NRC" in col.upper():
        nrc_col = col
        break

if nrc_col:
    print(f"Found NRC column: '{nrc_col}'")
    
    # Apply simple NRC validation (Valid/Invalid only)
    df["Status"] = df[nrc_col].apply(lambda x: get_nrc_status(x, valid_nrc_set))
    
    # Output file
    output_file = "validated_" + input_file
    output_path = os.path.join(output_dir, output_file)
    
    # Count Valid and Invalid
    valid_count = (df["Status"] == "Valid").sum()
    invalid_count = (df["Status"] == "Invalid").sum()
    
    print(f"\nValidation Results:")
    print(f"Valid: {valid_count}")
    print(f"Invalid: {invalid_count}")
    print(f"Total: {len(df)}")
    
    # Create simple summary
    summary_rows = []
    summary_rows.append({nrc_col: "", "Status": "=== SUMMARY ===", "Total": ""})
    summary_rows.append({nrc_col: "", "Status": "Valid", "Total": valid_count})
    summary_rows.append({nrc_col: "", "Status": "Invalid", "Total": invalid_count})
    summary_rows.append({nrc_col: "", "Status": "TOTAL", "Total": len(df)})
    
    summary_df = pd.DataFrame(summary_rows)
    
    # Pad original DataFrame with an empty "Total" column for alignment
    df["Total"] = ""
    
    # Append summary with separator
    df = pd.concat([df, pd.DataFrame([{}]), summary_df], ignore_index=True)
    
    # Save the updated DataFrame
    df.to_csv(output_path, index=False)
    print(f"\nProcessed file saved to: {output_path}")
    
else:
    print("Error: No NRC column found in the input file.")
    print("Available columns:", list(df.columns))
    print("Expected column names: NRC, Employee NRC, etc.")
    exit()