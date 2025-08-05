"""
Generate sample CSV files for GhostBuster system testing
This script creates mock datasets that simulate real ZRA, NAPSA, and PACRA data
"""

import pandas as pd
import random
from datetime import datetime, timedelta

def generate_napsa_data():
    """Generate mock NAPSA employee database"""
    employees = []
    
    # Generate 50 legitimate employees
    for i in range(1, 51):
        # Generate valid NRC format: XXXXXX/XX/X
        year = random.randint(80, 99)
        month = random.randint(1, 12)
        sequence = random.randint(100000, 999999)
        nrc = f"{sequence:06d}/{year:02d}/{month}"
        
        employees.append({
            'employee_id': f"EMP{i:04d}",
            'full_name': f"Employee {i}",
            'nrc': nrc,
            'date_registered': datetime.now() - timedelta(days=random.randint(30, 3650)),
            'employer_tpin': f"100{random.randint(1, 10)}-{random.randint(100000, 999999)}-{random.randint(10, 99)}",
            'monthly_contribution': random.randint(200, 2000)
        })
    
    df = pd.DataFrame(employees)
    df.to_csv('data/napsa_employees.csv', index=False)
    print(f"Generated NAPSA data: {len(df)} employees")
    return df

def generate_pacra_data():
    """Generate mock PACRA business registry"""
    companies = [
        {"name": "Acme Corporation", "tpin": "1001-123456-78", "reg_number": "REG001"},
        {"name": "Tech Solutions Ltd", "tpin": "1002-234567-89", "reg_number": "REG002"},
        {"name": "Mining Ventures", "tpin": "1003-345678-90", "reg_number": "REG003"},
        {"name": "Retail Express", "tpin": "1004-456789-01", "reg_number": "REG004"},
        {"name": "Construction Co", "tpin": "1005-567890-12", "reg_number": "REG005"},
        {"name": "Manufacturing Ltd", "tpin": "1006-678901-23", "reg_number": "REG006"},
        {"name": "Services Inc", "tpin": "1007-789012-34", "reg_number": "REG007"},
        {"name": "Logistics Pro", "tpin": "1008-890123-45", "reg_number": "REG008"},
        {"name": "Finance Corp", "tpin": "1009-901234-56", "reg_number": "REG009"},
        {"name": "Healthcare Ltd", "tpin": "1010-012345-67", "reg_number": "REG010"}
    ]
    
    # Add additional fields
    for company in companies:
        company.update({
            'registration_date': datetime.now() - timedelta(days=random.randint(365, 3650)),
            'status': 'Active',
            'business_type': random.choice(['Private Limited', 'Public Limited', 'Partnership']),
            'address': f"Plot {random.randint(1, 999)}, {random.choice(['Cairo', 'Addis Ababa', 'Great East', 'Independence'])} Road, Lusaka"
        })
    
    df = pd.DataFrame(companies)
    df.to_csv('data/pacra_companies.csv', index=False)
    print(f"Generated PACRA data: {len(df)} companies")
    return df

def generate_company_paye_data():
    """Generate mock company PAYE submissions with fraud scenarios"""
    companies_data = []
    
    # Scenario 1: Legitimate company
    companies_data.append({
        'company_name': 'Acme Corporation',
        'tpin': '1001-123456-78',
        'submission_date': '2024-01-15',
        'employees': [
            {'name': 'John Doe', 'nrc': '123456/85/1', 'gross_salary': 8000, 'paye_tax': 1200},
            {'name': 'Jane Smith', 'nrc': '234567/90/3', 'gross_salary': 7500, 'paye_tax': 1000},
            {'name': 'Bob Wilson', 'nrc': '345678/88/7', 'gross_salary': 6000, 'paye_tax': 750}
        ]
    })
    
    # Scenario 2: Ghost company (not in PACRA)
    companies_data.append({
        'company_name': 'Ghost Mining Ltd',
        'tpin': '9999-999999-99',
        'submission_date': '2024-01-20',
        'employees': [
            {'name': 'Phantom Worker 1', 'nrc': '000000/00/0', 'gross_salary': 5000, 'paye_tax': 500},
            {'name': 'Phantom Worker 2', 'nrc': 'invalid-nrc', 'gross_salary': 5500, 'paye_tax': 600},
            {'name': 'Phantom Worker 3', 'nrc': '999999/99/9', 'gross_salary': 6000, 'paye_tax': 700}
        ]
    })
    
    # Scenario 3: Company with duplicate employees
    companies_data.append({
        'company_name': 'Tech Solutions Ltd',
        'tpin': '1002-234567-89',
        'submission_date': '2024-01-18',
        'employees': [
            {'name': 'Alice Johnson', 'nrc': '456789/92/4', 'gross_salary': 9000, 'paye_tax': 1500},
            {'name': 'Charlie Brown', 'nrc': '123456/85/1', 'gross_salary': 8500, 'paye_tax': 1300},  # Duplicate NRC
            {'name': 'Diana Prince', 'nrc': '567890/89/2', 'gross_salary': 7800, 'paye_tax': 1100}
        ]
    })
    
    # Scenario 4: Suspicious company with many fake employees
    companies_data.append({
        'company_name': 'Suspicious Corp',
        'tpin': '7777-777777-77',
        'submission_date': '2024-01-25',
        'employees': [
            {'name': 'Fake Employee 1', 'nrc': 'bad-format-1', 'gross_salary': 3000, 'paye_tax': 200},
            {'name': 'Fake Employee 2', 'nrc': 'bad-format-2', 'gross_salary': 3000, 'paye_tax': 200},
            {'name': 'Fake Employee 3', 'nrc': 'bad-format-3', 'gross_salary': 3000, 'paye_tax': 200},
            {'name': 'Real Employee', 'nrc': '678901/91/5', 'gross_salary': 3000, 'paye_tax': 200},
            {'name': 'Another Fake', 'nrc': 'not-valid/format', 'gross_salary': 3000, 'paye_tax': 200}
        ]
    })
    
    # Convert to flat CSV format
    paye_records = []
    for company in companies_data:
        for employee in company['employees']:
            paye_records.append({
                'company_name': company['company_name'],
                'company_tpin': company['tpin'],
                'submission_date': company['submission_date'],
                'employee_name': employee['name'],
                'employee_nrc': employee['nrc'],
                'gross_salary': employee['gross_salary'],
                'paye_tax': employee['paye_tax']
            })
    
    df = pd.DataFrame(paye_records)