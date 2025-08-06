import pandas as pd
import random
from faker import Faker

fake = Faker()

# Province to TPIN prefix map
province_map = {
    "Central": "01",
    "Copperbelt": "10",
    "Eastern": "02",
    "Luapula": "03",
    "Lusaka": "04",
    "Muchinga": "05",
    "Northern": "06",
    "North-Western": "07",
    "Southern": "08",
    "Western": "09"
}

def generate_fake_tpin(province_code):
    return f"{province_code}{random.randint(100000000, 999999999)}"

records = []

for i in range(1, 1001):  # 1000 companies
    province = random.choice(list(province_map.keys()))
    province_code = province_map[province]
    business_name = fake.company()
    tpin = generate_fake_tpin(province_code)
    reg_number = f"REG{i:04d}"  # REG0001 → REG1000

    records.append({
        "Business Name": business_name,
        "TPIN": tpin,
        "Registration Number": reg_number,
        "Province": province
    })

# Save to CSV
pacra_df = pd.DataFrame(records)
pacra_df.to_csv("pacra_company_registry.csv", index=False)
print("PACRA dataset saved as pacra_company_registry.csv")
