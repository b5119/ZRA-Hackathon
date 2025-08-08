import pandas as pd
import os

# File paths
base_path = "C:/Users/Administrator/ZRA-Hackathon/Mock_data/"
target_file = "AUDIT1.csv"  # Change this to your target file
target_path = os.path.join(base_path, target_file)

# NAPSA file name
napsa_files = [
    "NAPSA_dataset.csv"
]

napsa_df = None
for filename in napsa_files:
    napsa_path = os.path.join(base_path, filename)
    try:
        napsa_df = pd.read_csv(napsa_path)
        print(f"Found NAPSA file: {filename}")
        break
    except FileNotFoundError:
        continue

if napsa_df is None:
    print("Error: NAPSA file not found. Available files:")
    for f in os.listdir(base_path):
        if f.lower().startswith('napsa'):
            print(f"  - {f}")
    exit()

# Check NAPSA columns
print("NAPSA columns:", list(napsa_df.columns))

# Find NRC column in NAPSA data
nrc_col = None
if "NRC" in napsa_df.columns:
    nrc_col = "NRC"
elif "nrc" in napsa_df.columns:
    nrc_col = "nrc"
else:
    print("Available NAPSA columns:", list(napsa_df.columns))
    exit("NRC column not found in NAPSA data")

napsa_nrc_set = set(napsa_df[nrc_col].astype(str).str.strip())

# Load target file
try:
    df = pd.read_csv(target_path)
    print("Target file columns:", list(df.columns))
except FileNotFoundError:
    print(f"Target file not found: {target_path}")
    exit()

# Find NRC column in target data
target_nrc_col = None
if "NRC" in df.columns:
    target_nrc_col = "NRC"
elif "nrc" in df.columns:
    target_nrc_col = "nrc"
elif "Employee NRC" in df.columns:
    target_nrc_col = "Employee NRC"
elif "employee nrc" in df.columns:
    target_nrc_col = "employee nrc"
else:
    print("Available target columns:", list(df.columns))
    exit("NRC column not found in target data")

# Clean NRC column
df[target_nrc_col] = df[target_nrc_col].astype(str).str.strip()

# Add NAPSA status
df["NAPSA STATUS"] = df[target_nrc_col].apply(
    lambda x: "Registered" if x in napsa_nrc_set else "Not Registered"
)

# Save result to specific output directory
output_dir = "C:/Users/Administrator/ZRA-Hackathon/Back_End_Logic/Processed_Document_Statuses/"
os.makedirs(output_dir, exist_ok=True)  # Create directory if it doesn't exist

output_filename = target_file.replace(".csv", "_with_napsa_status.csv")
output_path = os.path.join(output_dir, output_filename)
df.to_csv(output_path, index=False)

# Print summary
registered = (df["NAPSA STATUS"] == "Registered").sum()
not_registered = (df["NAPSA STATUS"] == "Not Registered").sum()

print(f"\nFile processed: {output_path}")
print(f"Registered: {registered}")
print(f"Not Registered: {not_registered}")
print(f"Total: {len(df)}")