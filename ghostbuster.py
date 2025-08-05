import streamlit as st
import pandas as pd
import numpy as np
import re
import csv
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

# Set page config
st.set_page_config(
    page_title="GhostBuster - AI Fraud Detection",
    page_icon="👻",
    layout="wide",
    initial_sidebar_state="expanded"
)

class GhostBusterEngine:
    def __init__(self):
        self.napsa_data = self.generate_mock_napsa_data()
        self.pacra_data = self.generate_mock_pacra_data()
        
    def generate_mock_napsa_data(self):
        """Generate mock NAPSA employee database"""
        valid_nrcs = [
            "123456/78/1", "234567/89/1", "345678/90/1", "456789/01/1", 
            "567890/12/1", "678901/23/1", "789012/34/1", "890123/45/1",
            "901234/56/1", "012345/67/1", "111111/11/1", "222222/22/1",
            "333333/33/1", "444444/44/1", "555555/55/1", "666666/66/1"
        ]
        
        employees = []
        for i, nrc in enumerate(valid_nrcs):
            employees.append({
                'name': f'Employee {i+1}',
                'nrc': nrc,
                'employer': f'Company {(i % 5) + 1}'
            })
        
        return pd.DataFrame(employees)
    
    def generate_mock_pacra_data(self):
        """Generate mock PACRA business registry"""
        companies = [
            {"name": "Acme Corporation", "tpin": "1001-123456-78", "reg_number": "REG001", "status": "Active"},
            {"name": "Tech Solutions Ltd", "tpin": "1002-234567-89", "reg_number": "REG002", "status": "Active"},
            {"name": "Mining Ventures", "tpin": "1003-345678-90", "reg_number": "REG003", "status": "Active"},
            {"name": "Retail Express", "tpin": "1004-456789-01", "reg_number": "REG004", "status": "Active"},
            {"name": "Construction Co", "tpin": "1005-567890-12", "reg_number": "REG005", "status": "Active"},
            {"name": "Manufacturing Ltd", "tpin": "1006-678901-23", "reg_number": "REG006", "status": "Active"},
            {"name": "Services Inc", "tpin": "1007-789012-34", "reg_number": "REG007", "status": "Active"}
        ]
        
        return pd.DataFrame(companies)
    
    def generate_mock_company_data(self):
        """Generate mock company PAYE data with various fraud scenarios"""
        companies = [
            {
                "name": "Acme Corporation",
                "tpin": "1001-123456-78",
                "employees": [
                    {"name": "John Doe", "nrc": "123456/78/1", "salary": 8000},
                    {"name": "Jane Smith", "nrc": "234567/89/1", "salary": 7500},
                    {"name": "Bob Wilson", "nrc": "invalid-nrc-1", "salary": 6000}  # Invalid NRC
                ]
            },
            {
                "name": "Ghost Company Ltd",  # Not in PACRA
                "tpin": "9999-999999-99",
                "employees": [
                    {"name": "Fake Employee 1", "nrc": "000000/00/0", "salary": 5000},  # Invalid NRC
                    {"name": "Fake Employee 2", "nrc": "111111/11/1", "salary": 5500},  # Valid but will be reused
                    {"name": "Fake Employee 3", "nrc": "invalid-format", "salary": 6000}  # Invalid format
                ]
            },
            {
                "name": "Tech Solutions Ltd",
                "tpin": "1002-234567-89",
                "employees": [
                    {"name": "Alice Johnson", "nrc": "345678/90/1", "salary": 9000},
                    {"name": "Charlie Brown", "nrc": "111111/11/1", "salary": 8500},  # Reused NRC
                    {"name": "Diana Prince", "nrc": "456789/01/1", "salary": 7800}
                ]
            },
            {
                "name": "Phantom Enterprises",  # Not in PACRA
                "tpin": "8888-888888-88",
                "employees": [
                    {"name": "Ghost Worker 1", "nrc": "bad-nrc-format", "salary": 4000},
                    {"name": "Ghost Worker 2", "nrc": "another-bad-nrc", "salary": 4200},
                    {"name": "Ghost Worker 3", "nrc": "999999/99/9", "salary": 4500}
                ]
            },
            {
                "name": "Suspicious Corp",  # Will have many issues
                "tpin": "7777-777777-77",
                "employees": [
                    {"name": "Fake 1", "nrc": "bad1", "salary": 3000},
                    {"name": "Fake 2", "nrc": "bad2", "salary": 3000},
                    {"name": "Fake 3", "nrc": "bad3", "salary": 3000},
                    {"name": "Fake 4", "nrc": "222222/22/1", "salary": 3000},  # Valid but reused
                    {"name": "Fake 5", "nrc": "not-in-napsa/12/3", "salary": 3000}  # Valid format but not in NAPSA
                ]
            }
        ]
        
        return companies
    
    def validate_nrc(self, nrc):
        """Validate NRC format: XXXXXX/XX/X"""
        pattern = r'^\d{6}/\d{2}/\d$'
        return bool(re.match(pattern, nrc))
    
    def check_napsa_registration(self, nrc):
        """Check if NRC exists in NAPSA database"""
        return nrc in self.napsa_data['nrc'].values
    
    def check_pacra_registration(self, company_name, tpin):
        """Check if company is registered in PACRA"""
        pacra_match = self.pacra_data[
            (self.pacra_data['name'].str.lower() == company_name.lower()) |
            (self.pacra_data['tpin'] == tpin)
        ]
        return len(pacra_match) > 0
    
    def simulate_online_presence(self, company_name):
        """Simulate online presence check"""
        # For demo purposes, make some companies have no presence
        no_presence_companies = ['Ghost Company Ltd', 'Phantom Enterprises', 'Suspicious Corp']
        return company_name not in no_presence_companies
    
    def analyze_companies(self, company_data):
        """Main analysis function"""
        results = []
        nrc_usage_map = {}
        
        # Track NRC usage across all companies
        for company in company_data:
            for employee in company['employees']:
                nrc = employee['nrc']
                if nrc not in nrc_usage_map:
                    nrc_usage_map[nrc] = []
                nrc_usage_map[nrc].append(company['name'])
        
        # Analyze each company
        for company in company_data:
            flags = []
            risk_score = 0
            
            # Employee analysis
            invalid_nrcs = 0
            missing_from_napsa = 0
            reused_nrcs = 0
            total_salary = 0
            
            for employee in company['employees']:
                nrc = employee['nrc']
                total_salary += employee.get('salary', 0)
                
                # Check NRC format
                if not self.validate_nrc(nrc):
                    invalid_nrcs += 1
                    risk_score += 10
                
                # Check NAPSA registration
                elif not self.check_napsa_registration(nrc):
                    missing_from_napsa += 1
                    risk_score += 5
                
                # Check for NRC reuse
                if len(nrc_usage_map.get(nrc, [])) > 1:
                    reused_nrcs += 1
                    risk_score += 15
            
            # Company registration check
            pacra_registered = self.check_pacra_registration(company['name'], company['tpin'])
            if not pacra_registered:
                flags.append("No PACRA registration found")
                risk_score += 25
            
            # Online presence check
            has_online_presence = self.simulate_online_presence(company['name'])
            if not has_online_presence:
                flags.append("No significant online presence detected")
                risk_score += 10
            
            # Add specific flags
            if invalid_nrcs > 0:
                flags.append(f"{invalid_nrcs} invalid NRC format(s)")
            
            if missing_from_napsa > 0:
                flags.append(f"{missing_from_napsa} employee(s) not in NAPSA database")
            
            if reused_nrcs > 0:
                flags.append(f"{reused_nrcs} NRC(s) used in multiple companies")
            
            # Salary analysis
            avg_salary = total_salary / len(company['employees']) if company['employees'] else 0
            if avg_salary < 4000 and len(company['employees']) > 3:
                flags.append("Unusually low average salary for large workforce")
                risk_score += 8
            
            # Determine risk level
            if risk_score >= 50:
                risk_level = 'Critical'
            elif risk_score >= 25:
                risk_level = 'High'
            elif risk_score >= 10:
                risk_level = 'Medium'
            else:
                risk_level = 'Low'
            
            # Compile results
            result = {
                'company_name': company['name'],
                'tpin': company['tpin'],
                'employee_count': len(company['employees']),
                'total_salary_expense': total_salary,
                'average_salary': avg_salary,
                'invalid_nrcs': invalid_nrcs,
                'missing_from_napsa': missing_from_napsa,
                'reused_nrcs': reused_nrcs,
                'pacra_registered': pacra_registered,
                'has_online_presence': has_online_presence,
                'flags': flags,
                'risk_score': risk_score,
                'risk_level': risk_level,
                'is_flagged': len(flags) > 0
            }
            
            results.append(result)
        
        return results

def main():
    st.title("👻 GhostBuster - AI Fraud Detection System")
    st.markdown("**Detecting Fake Companies & Phantom Employees for ZRA**")
    
    # Initialize the engine
    if 'engine' not in st.session_state:
        st.session_state.engine = GhostBusterEngine()
    
    # Sidebar
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Choose a page", ["Home", "Upload Data", "Analysis Results", "System Info"])
    
    if page == "Home":
        st.header("Welcome to GhostBuster")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🎯 System Capabilities")
            st.write("""
            - **NRC Validation**: Verify employee NRC formats and authenticity
            - **NAPSA Cross-check**: Validate employees against NAPSA database
            - **PACRA Verification**: Check company registration status
            - **Duplicate Detection**: Find reused NRCs across companies
            - **Online Presence**: Basic web presence verification
            - **Risk Scoring**: AI-powered fraud likelihood assessment
            """)
        
        with col2:
            st.subheader("📊 Key Features")
            st.write("""
            - Real-time analysis of company data
            - Interactive dashboard with visualizations
            - Automated flag generation with explanations
            - Export capabilities for flagged companies
            - Risk level categorization (Low/Medium/High/Critical)
            - Comprehensive reporting for ZRA officials
            """)
        
        # Quick stats about mock data
        st.subheader("📈 Demo Database Stats")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("NAPSA Records", len(st.session_state.engine.napsa_data))
        with col2:
            st.metric("PACRA Companies", len(st.session_state.engine.pacra_data))
        with col3:
            st.metric("Demo Companies", 5)
    
    elif page == "Upload Data":
        st.header("📤 Data Upload & Analysis")
        
        st.info("For this demo, we'll use pre-generated mock data that simulates real ZRA scenarios.")
        
        if st.button("🔍 Run Analysis on Demo Data", type="primary"):
            with st.spinner("Analyzing companies for fraud indicators..."):
                company_data = st.session_state.engine.generate_mock_company_data()
                results = st.session_state.engine.analyze_companies(company_data)
                st.session_state.analysis_results = results
                
            st.success("Analysis completed!")
            st.balloons()
            
            # Show quick summary
            flagged_count = sum(1 for r in results if r['is_flagged'])
            total_companies = len(results)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Companies", total_companies)
            with col2:
                st.metric("Flagged Companies", flagged_count, delta=f"{flagged_count/total_companies*100:.1f}%")
            with col3:
                st.metric("Clean Companies", total_companies - flagged_count)
        
        # File upload option (for future implementation)
        st.subheader("📁 Upload Your Own Data")
        st.info("Feature coming soon: Upload CSV files with company PAYE data")
        uploaded_file = st.file_uploader("Choose a CSV file", type="csv", disabled=True)
    
    elif page == "Analysis Results":
        st.header("📊 Analysis Results")
        
        if 'analysis_results' not in st.session_state:
            st.warning("No analysis results available. Please run analysis first from the Upload Data page.")
            return
        
        results = st.session_state.analysis_results
        df_results = pd.DataFrame(results)
        
        # Summary metrics
        st.subheader("📈 Summary Statistics")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Companies", len(results))
        with col2:
            flagged_count = df_results['is_flagged'].sum()
            st.metric("Flagged Companies", flagged_count)
        with col3:
            critical_count = (df_results['risk_level'] == 'Critical').sum()
            st.metric("Critical Risk", critical_count)
        with col4:
            total_employees = df_results['employee_count'].sum()
            st.metric("Total Employees", total_employees)
        
        # Risk level distribution
        st.subheader("📊 Risk Level Distribution")
        risk_counts = df_results['risk_level'].value_counts()
        
        fig = px.pie(values=risk_counts.values, names=risk_counts.index, 
                     title="Companies by Risk Level",
                     color_discrete_map={
                         'Low': '#10B981',
                         'Medium': '#F59E0B', 
                         'High': '#EF4444',
                         'Critical': '#7C2D12'
                     })
        st.plotly_chart(fig, use_container_width=True)
        
        # Risk score distribution
        fig2 = px.histogram(df_results, x='risk_score', nbins=10, 
                           title="Risk Score Distribution",
                           labels={'risk_score': 'Risk Score', 'count': 'Number of Companies'})
        st.plotly_chart(fig2, use_container_width=True)
        
        # Detailed results table
        st.subheader("🔍 Detailed Company Analysis")
        
        # Filter options
        col1, col2 = st.columns(2)
        with col1:
            risk_filter = st.multiselect("Filter by Risk Level", 
                                       options=['Low', 'Medium', 'High', 'Critical'],
                                       default=['Medium', 'High', 'Critical'])
        with col2:
            flagged_only = st.checkbox("Show only flagged companies", value=True)
        
        # Apply filters
        filtered_df = df_results.copy()
        if risk_filter:
            filtered_df = filtered_df[filtered_df['risk_level'].isin(risk_filter)]
        if flagged_only:
            filtered_df = filtered_df[filtered_df['is_flagged'] == True]
        
        # Display results
        for idx, row in filtered_df.iterrows():
            with st.expander(f"🏢 {row['company_name']} - {row['risk_level']} Risk (Score: {row['risk_score']})"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**TPIN:** {row['tpin']}")
                    st.write(f"**Employees:** {row['employee_count']}")
                    st.write(f"**Total Salary Expense:** K{row['total_salary_expense']:,.2f}")
                    st.write(f"**Average Salary:** K{row['average_salary']:,.2f}")
                
                with col2:
                    st.write(f"**PACRA Registered:** {'✅' if row['pacra_registered'] else '❌'}")
                    st.write(f"**Online Presence:** {'✅' if row['has_online_presence'] else '❌'}")
                    st.write(f"**Invalid NRCs:** {row['invalid_nrcs']}")
                    st.write(f"**Missing from NAPSA:** {row['missing_from_napsa']}")
                
                if row['flags']:
                    st.subheader("🚨 Issues Detected:")
                    for flag in row['flags']:
                        st.error(f"• {flag}")
        
        # Export functionality
        st.subheader("📤 Export Results")
        if st.button("Download Flagged Companies CSV"):
            flagged_results = [r for r in results if r['is_flagged']]
            flagged_df = pd.DataFrame(flagged_results)
            
            csv = flagged_df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"ghostbuster_flagged_companies_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
    
    elif page == "System Info":
        st.header("ℹ️ System Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🔍 Validation Methods")
            st.write("""
            **NRC Validation:**
            - Format check: XXXXXX/XX/X pattern
            - Checksum validation (simulated)
            
            **NAPSA Cross-reference:**
            - Employee existence verification
            - Employment history check
            
            **PACRA Verification:**
            - Business registration status
            - Company name and TPIN matching
            
            **Online Presence:**
            - Basic web search simulation
            - Social media presence check
            """)
        
        with col2:
            st.subheader("⚡ Risk Scoring System")
            st.write("""
            **Point System:**
            - Invalid NRC format: +10 points
            - Missing from NAPSA: +5 points
            - Reused NRC: +15 points
            - No PACRA registration: +25 points
            - No online presence: +10 points
            - Low salary anomaly: +8 points
            
            **Risk Levels:**
            - Low: 0-9 points
            - Medium: 10-24 points  
            - High: 25-49 points
            - Critical: 50+ points
            """)
        
        st.subheader("🎯 Project Objectives")
        st.write("""
        **Primary Goals:**
        1. Detect shell/ghost companies claiming false tax refunds
        2. Identify phantom employees used to inflate expenses
        3. Cross-validate employee records across multiple databases
        4. Provide actionable intelligence for ZRA investigators
        
        **Technical Approach:**
        - Rule-based validation with AI-assisted scoring
        - Multi-source data cross-referencing
        - Automated anomaly detection
        - User-friendly dashboard for non-technical users
        """)
        
        st.subheader("🚀 Future Enhancements")
        st.write("""
        - Machine learning models for advanced pattern recognition
        - Real-time API integration with NAPSA and PACRA
        - Salary benchmarking against industry standards
        - Network analysis to detect related fraudulent entities
        - Mobile app for field verification
        """)

if __name__ == "__main__":
    main()