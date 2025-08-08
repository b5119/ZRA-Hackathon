import pandas as pd
import random
from faker import Faker

fake = Faker()

# Define province map
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

# Generate NRC and TPIN using province code
def generate_fake_nrc(province_code):
    part2 = random.randint(10, 99)
    part3 = random.randint(1, 9)
    return f"{province_code}{random.randint(1000, 9999)}/{part2}/{part3}"

def generate_fake_tpin(province_code):
    return f"{province_code}{random.randint(100000000, 999999999)}"

def generate_fake_napsa(province_code):
    return f"{province_code}{random.randint(10000000, 99999999)}"  # 10-digit starting with province

# Generate dataset
num_records = 100
data = {
    "Full Name": [],
    "Province": [],
    "NRC": [],
    "TPIN": [],
    "NAPSA": []
}

for _ in range(num_records):
    province = random.choice(list(province_map.keys()))
    province_code = province_map[province]
    full_name = fake.name()
    nrc = generate_fake_nrc(province_code)
    tpin = generate_fake_tpin(province_code)
    napsa = generate_fake_napsa(province_code)

    data["Full Name"].append(full_name)
    data["Province"].append(province)
    data["NRC"].append(nrc)
    data["TPIN"].append(tpin)
    data["NAPSA"].append(napsa)

# Create DataFrame and save
output_path = "C:/Users/Administrator/ZRA-Hackathon/Mock_data/NAPSA_dataset.csv"
df = pd.DataFrame(data)
df.to_csv(output_path, index=False)
print(f"\u2705 Dataset saved as {output_path}")
