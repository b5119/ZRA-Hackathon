import pandas as pd
import random
from faker import Faker

fake = Faker()

# Province map with codes
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

def generate_fake_nrc(province_code):
    part2 = random.randint(10, 99)
    part3 = random.randint(1, 9)
    return f"{province_code}{random.randint(1000, 9999)}/{part2}/{part3}"

def generate_fake_tpin(province_code):
    return f"{province_code}{random.randint(100000000, 999999999)}"

# Final PAYE dataset
records = []

for _ in range(1000):  # 1000 companies
    province = random.choice(list(province_map.keys()))
    province_code = province_map[province]
    company_name = fake.company()
    company_tpin = generate_fake_tpin(province_code)

    # Each company has 1 to 5 employees
    for _ in range(random.randint(1, 10)):
        employee_name = fake.name()
        employee_nrc = generate_fake_nrc(province_code)
        records.append({
            "Company Name": company_name,
            "TPIN": company_tpin,
            "Employee Name": employee_name,
            "Employee NRC": employee_nrc,
            "Province": province
        })

# Save to CSV
df = pd.DataFrame(records)
df.to_csv("company_paye_data_with_province.csv", index=False)
print("PAYE dataset saved as company_paye_data_with_province.csv")
