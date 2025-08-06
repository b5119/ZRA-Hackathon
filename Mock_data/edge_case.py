import pandas as pd
import random
from faker import Faker
import os

# Set base path
base_path = "C:/Users/Administrator/ZRA-Hackathon/Mock_data"

# Load all required CSVs using full paths
company_paye_df = pd.read_csv(os.path.join(base_path, "company_paye_data_with_province.csv"))
fake_nrc_df = pd.read_csv(os.path.join(base_path, "fake_nrc_tpin_dataset.csv"))
fake_nrc_with_province_df = pd.read_csv(os.path.join(base_path, "fake_nrc_tpin_with_province.csv"))
pacra_df = pd.read_csv(os.path.join(base_path, "pacra_company_registry.csv"))

faker = Faker()

# Province map
province_map = {
    "Central": "01", "Copperbelt": "10", "Eastern": "02", "Luapula": "03", "Lusaka": "04",
    "Muchinga": "05", "Northern": "06", "North-Western": "07", "Southern": "08", "Western": "09"
}

# Start with PAYE dataset
paye_df = fake_nrc_with_province_df.copy()
edge_cases = []

# ---------------------------------------------------------
# 1. 15 Employees with Duplicate NRCs
# ---------------------------------------------------------
sample_nrcs = company_paye_df.sample(3)['Employee NRC'].tolist()  # 3 NRCs × 5 each = 15
for nrc in sample_nrcs:
    for _ in range(5):
        edge_cases.append({
            "Full Name": faker.name(),
            "Province": random.choice(list(province_map.keys())),
            "NRC": nrc,
            "TPIN": faker.random_number(digits=11, fix_len=True)
        })

# ---------------------------------------------------------
# 2. 20 Companies that Don’t Exist in PACRA
# ---------------------------------------------------------
existing_tpins = set(pacra_df["TPIN"])
fake_tpins = set()
while len(fake_tpins) < 20:
    tpin = str(faker.random_number(digits=11, fix_len=True))
    if tpin not in existing_tpins:
        fake_tpins.add(tpin)

for fake_tpin in fake_tpins:
    edge_cases.append({
        "Full Name": faker.name(),
        "Province": random.choice(list(province_map.keys())),
        "NRC": f"{random.randint(1, 99):02d}/{random.randint(100000,999999)}/1",
        "TPIN": fake_tpin
    })

# ---------------------------------------------------------
# 3. 25 Invalid NRC Formats
# ---------------------------------------------------------
invalid_nrcs = [
    "1234567890", "99/999999/ABC", "07-123456/1", "AB/123456/7", "10/12345/1",
    "01_123456/7", "10/12X456/8", "!!/123456/9", "00/1234/0", "10//123456/1",
    "07/1234567", "77.123456.1", "05/123456789", "12/abc123/9", "11/000000/0",
    "0A/123456/1", "04/1A3456/2", "02/12/1", "??/??????/?", "14/111111/6",
    "06/12/89/1", "03\\123456\\1", "08 123456 1", "09/1234x6/3", "13-999999-5"
]

for nrc in invalid_nrcs:
    edge_cases.append({
        "Full Name": faker.name(),
        "Province": random.choice(list(province_map.keys())),
        "NRC": nrc,
        "TPIN": faker.random_number(digits=11, fix_len=True)
    })

# ---------------------------------------------------------
# Merge original PAYE + edge cases
# ---------------------------------------------------------
edge_df = pd.DataFrame(edge_cases)
combined_df = pd.concat([paye_df, edge_df], ignore_index=True)

# Save to output file
output_path = os.path.join(base_path, "paye_with_edge_cases.csv")
combined_df.to_csv(output_path, index=False)

print(f"File saved to: {output_path}")
