import os
import pandas as pd
import numpy as np

def napsa_validator():
    """
    NAPSA Registration Validator
    Checks company employee data against NAPSA database and marks registration status
    """
    
    # === File Paths ===
    base_path = "C:/Users/Administrator/ZRA-Hackathon/Mock_data/"
    output_dir = "C:/Users/Administrator/ZRA-Hackathon/Back_End_Logic/Processed_Document_Statuses/"
    
    # Input files
    napsa_path = os.path.join(base_path, "NAPSA_dataset.csv")
    company_paye_path = os.path.join(base_path, "company_paye_data_with_province.csv")
    cross_check_path = os.path.join(base_path, "CrossCheck_EMPLOYEES.csv")
    
    # Output files
    os.makedirs(output_dir, exist_ok=True)
    paye_output = os.path.join(output_dir, "company_paye_with_napsa_status.csv")
    cross_check_output = os.path.join(output_dir, "crosscheck_with_napsa_status.csv")
    missing_nrcs_output = os.path.join(output_dir, "missing_napsa_nrcs.csv")
    matches_output = os.path.join(output_dir, "NAPSA_Matches.csv")
    
    # === Load NAPSA Database ===
    try:
        print("Loading NAPSA database...")
        napsa_df = pd.read_csv(napsa_path)
        
        # Clean and normalize NAPSA data
        if 'NRC' in napsa_df.columns:
            napsa_df['NRC'] = napsa_df['NRC'].astype(str).str.strip().str.replace('-', '').str.replace('/', '')
            napsa_nrc_set = set(napsa_df['NRC'])
        else:
            raise ValueError("NRC column not found in NAPSA database")
            
        # Also create name set if available
        napsa_names_set = set()
        if 'Employee Name' in napsa_df.columns:
            napsa_df['Employee Name'] = napsa_df['Employee Name'].str.strip().str.upper()
            napsa_names_set = set(napsa_df['Employee Name'])
            
        print(f"NAPSA database loaded: {len(napsa_df)} records")
        
    except FileNotFoundError:
        print(f"Error: NAPSA database not found at {napsa_path}")
        return
    except Exception as e:
        print(f"Error loading NAPSA database: {e}")
        return
    
    # === Function to check NAPSA registration ===
    def check_napsa_registration(nrc, name=None):
        """Check if NRC (and optionally name) exists in NAPSA database"""
        if pd.isna(nrc) or str(nrc).strip() == '':
            return "Missing NRC"
        
        # Clean NRC for comparison
        clean_nrc = str(nrc).strip().replace('-', '').replace('/', '')
        
        # Check NRC match
        nrc_match = clean_nrc in napsa_nrc_set
        
        # If name is provided and we have names in NAPSA data, check name match too
        if name and napsa_names_set:
            clean_name = str(name).strip().upper()
            name_match = clean_name in napsa_names_set
            
            if nrc_match and name_match:
                return "Registered (NRC & Name Match)"
            elif nrc_match:
                return "Registered (NRC Match Only)"
            elif name_match:
                return "Name Found (Different NRC)"
            else:
                return "Not Registered"
        else:
            return "Registered" if nrc_match else "Not Registered"
    
    # === Process Company PAYE Data ===
    try:
        print("\nProcessing company PAYE data...")
        df = pd.read_csv(company_paye_path)
        
        # Clean NRC formatting
        if "NRC" not in df.columns:
            raise ValueError("NRC column not found in company PAYE data")
        
        df["NRC"] = df["NRC"].astype(str).str.strip()
        
        # Check NAPSA registration status
        name_col = None
        if 'Full Name' in df.columns:
            name_col = 'Full Name'
        elif 'Employee Name' in df.columns:
            name_col = 'Employee Name'
        
        if name_col:
            df["NAPSA REGISTRATION STATUS"] = df.apply(
                lambda row: check_napsa_registration(row["NRC"], row[name_col]), 
                axis=1
            )
        else:
            df["NAPSA REGISTRATION STATUS"] = df["NRC"].apply(
                lambda x: check_napsa_registration(x)
            )
        
        # Reorder columns
        columns = df.columns.tolist()
        first_cols = [col for col in ["Full Name", "Employee Name", "NRC"] if col in columns]
        company_cols = [col for col in ["Company Name", "Business Name"] if col in columns]
        tpin_col = ["TPIN"] if "TPIN" in columns else []
        status_col = ["NAPSA REGISTRATION STATUS"]
        last_cols = [col for col in ["Province"] if col in columns]
        
        middle_cols = [col for col in columns if col not in (first_cols + company_cols + tpin_col + status_col + last_cols)]
        new_order = first_cols + company_cols + tpin_col + middle_cols + status_col + last_cols
        
        df = df[new_order]
        df.to_csv(paye_output, index=False)
        
        # Summary statistics
        status_counts = df["NAPSA REGISTRATION STATUS"].value_counts()
        print(f"Company PAYE data processed and saved to: {paye_output}")
        print("Status Summary:")
        for status, count in status_counts.items():
            print(f"  {status}: {count}")
            
    except FileNotFoundError:
        print(f"Company PAYE file not found: {company_paye_path}")
    except Exception as e:
        print(f"Error processing company PAYE data: {e}")
    
    # === Process Cross-Check Employees Data ===
    try:
        print(f"\nProcessing cross-check employees data...")
        cross_df = pd.read_csv(cross_check_path)
        
        # Normalize data
        if 'Employee Name' in cross_df.columns:
            cross_df['Employee Name'] = cross_df['Employee Name'].str.strip().str.upper()
        
        if 'NRC' in cross_df.columns:
            cross_df['NRC'] = cross_df['NRC'].astype(str).str.strip()
            
            # Check NAPSA registration
            if 'Employee Name' in cross_df.columns:
                cross_df["NAPSA REGISTRATION STATUS"] = cross_df.apply(
                    lambda row: check_napsa_registration(row["NRC"], row["Employee Name"]), 
                    axis=1
                )
            else:
                cross_df["NAPSA REGISTRATION STATUS"] = cross_df["NRC"].apply(
                    lambda x: check_napsa_registration(x)
                )
            
            # Save processed cross-check data
            cross_df.to_csv(cross_check_output, index=False)
            print(f"Cross-check data processed and saved to: {cross_check_output}")
            
            # Create matches file (employees found in both datasets)
            if 'TPIN' in cross_df.columns and 'Employee Name' in cross_df.columns:
                matches = pd.merge(
                    cross_df,
                    napsa_df,
                    how='inner',
                    on=['TPIN', 'Employee Name']
                )
                matches.to_csv(matches_output, index=False)
                print(f"NAPSA matches saved to: {matches_output}")
                print(f"Found {len(matches)} exact matches (TPIN + Name)")
        
    except FileNotFoundError:
        print(f"Cross-check file not found: {cross_check_path}")
    except Exception as e:
        print(f"Error processing cross-check data: {e}")
    
    # === Generate Missing NRCs Report ===
    try:
        print(f"\nGenerating missing NRCs report...")
        missing_records = []
        
        # Check company PAYE data
        if 'df' in locals():
            missing_paye = df[df["NAPSA REGISTRATION STATUS"].str.contains("Not Registered|Missing NRC", na=False)]
            if not missing_paye.empty:
                missing_paye_copy = missing_paye.copy()
                missing_paye_copy['Source'] = 'Company PAYE'
                missing_records.append(missing_paye_copy)
        
        # Check cross-check data  
        if 'cross_df' in locals():
            missing_cross = cross_df[cross_df["NAPSA REGISTRATION STATUS"].str.contains("Not Registered|Missing NRC", na=False)]
            if not missing_cross.empty:
                missing_cross_copy = missing_cross.copy()
                missing_cross_copy['Source'] = 'Cross-Check'
                missing_records.append(missing_cross_copy)
        
        # Combine and save missing records
        if missing_records:
            all_missing = pd.concat(missing_records, ignore_index=True)
            all_missing.to_csv(missing_nrcs_output, index=False)
            print(f"Missing NRCs report saved to: {missing_nrcs_output}")
            print(f"Total missing/unregistered NRCs: {len(all_missing)}")
        else:
            print("No missing NRCs found!")
            
    except Exception as e:
        print(f"Error generating missing NRCs report: {e}")
    
    print(f"\nNAPSA validation completed!")
    print(f"All output files saved in: {output_dir}")

# Run the validator
if __name__ == "__main__":
    napsa_validator()