import pandas as pd
import random
from faker import Faker

fake = Faker()

def generate_fake_nrc():
    part1 = random.randint(100000, 999999)
    part2 = random.randint(10, 99)
    part3 = random.randint(1, 9)
    return f"{part1}/{part2}/{part3}"

def generate_fake_tpin():
    return str(random.randint(1000000000, 9999999999))

# Create dataset
num_records = 1000
data = {
    "Full Name": [fake.name() for _ in range(num_records)],
    "NRC": [generate_fake_nrc() for _ in range(num_records)],
    "TPIN": [generate_fake_tpin() for _ in range(num_records)]
}

df = pd.DataFrame(data)
df.to_csv("fake_nrc_tpin_dataset.csv", index=False)
print("Dataset saved as fake_nrc_tpin_dataset.csv")
