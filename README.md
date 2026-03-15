# 👻 GhostBuster — ZRA Fraud Detection System

> An AI-powered tool to detect fake companies and phantom employees using rule-based logic, mock datasets, and an interactive dashboard — built for the **ZRA Hackathon**.

---

## 📌 Overview

GhostBuster helps the **Zambia Revenue Authority (ZRA)** identify fraudulent PAYE submissions by cross-referencing company and employee data against mock registries that simulate **NAPSA**, **PACRA**, and **ZRA** databases.

It flags:
- 🏚️ **Ghost companies** — businesses not registered in PACRA
- 👤 **Phantom employees** — workers with invalid or duplicated NRCs
- 📉 **Salary anomalies** — suspiciously low payroll patterns
- 🔁 **Duplicate NRCs** — same employee claimed across multiple companies

---

## 🗂️ Project Structure

```
ZRA-Hackathon/
├── ghostbuster.py                        # Main Streamlit app & detection engine
├── sampledata.py                         # Mock data generator (NAPSA, PACRA, PAYE)
├── gui.js                                # Frontend JS utilities
├── requirements.txt                      # Python dependencies
├── company_paye_data_with_province.csv   # Sample PAYE dataset with provinces
│
├── Back_End_Logic/                       # Core validation modules
│   ├── NRC_Validation_Module/            # NRC format & checksum validation
│   ├── NRC_Validation_Module2.py
│   ├── NAPSA_Validation_Module.py        # NAPSA cross-reference logic
│   ├── NAPSA_Validation_Moduel2.py
│   ├── NRC_validation_doccumentation.txt
│   └── Processed_Document_Statuses/
│
└── Mock_data/                            # Simulated datasets
    ├── NAPSA_dataset.csv                 # Mock employee registry
    ├── pacra_company_registry.csv        # Mock business registry
    ├── company_paye_data_with_province.csv
    ├── company_paye_data_with_province_with_napsa_status.csv
    ├── paye_with_edge_cases.csv
    ├── fake_nrc_tpin_with_province.csv
    ├── reference_nrc_dataset.csv
    ├── subset_nrc_dataset.csv
    ├── AUDIT1.csv / AUDIT2.csv
    └── *.py                              # Data generation scripts
```

---

## ⚙️ Prerequisites

- Python 3.8 or higher
- pip3

---

## 🚀 Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/kaps10000/ZRA-Hackathon.git
cd ZRA-Hackathon
```

### 2. Install dependencies

```bash
pip3 install -r requirements.txt --user
```

Or if your system blocks user installs:

```bash
pip3 install -r requirements.txt --break-system-packages
```

### 3. Run the app

```bash
python3 -m streamlit run ghostbuster.py
```

The dashboard will open automatically in your browser at **http://localhost:8501**

> **Tip:** When prompted for an email by Streamlit on first launch, just press **Enter** to skip.

---

## 🖥️ Using the Dashboard

| Page | Description |
|---|---|
| **Home** | System overview and mock database statistics |
| **Upload Data** | Run analysis on demo data or upload your own CSV |
| **Analysis Results** | View flagged companies, risk charts, and export CSV |
| **System Info** | Scoring methodology and future roadmap |

### Quick Start
1. Open the app and navigate to **Upload Data**
2. Click **"Run Analysis on Demo Data"**
3. Go to **Analysis Results** to view flagged companies and risk scores

---

## 🔍 How Fraud Detection Works

### Validation Checks

| Check | Points | Description |
|---|---|---|
| Invalid NRC format | +10 | Employee ID doesn't match `XXXXXX/XX/X` pattern |
| Missing from NAPSA | +5 | Valid NRC but not found in pension registry |
| Duplicate NRC | +15 | Same NRC used across multiple companies |
| No PACRA registration | +25 | Company not found in business registry |
| No online presence | +10 | No detectable web/social presence |
| Low salary anomaly | +8 | Average salary suspiciously low for workforce size |

### Risk Levels

| Score | Risk Level |
|---|---|
| 0 – 9 | 🟢 Low |
| 10 – 24 | 🟡 Medium |
| 25 – 49 | 🔴 High |
| 50+ | ⚫ Critical |

---

## 📊 Mock Data Scenarios

The demo dataset includes 5 companies designed to test detection:

| Company | Scenario |
|---|---|
| Acme Corporation | Mostly legitimate, one invalid NRC |
| Ghost Company Ltd | Not in PACRA, multiple invalid NRCs |
| Tech Solutions Ltd | Valid company but reused NRCs |
| Phantom Enterprises | Unregistered, all bad NRC formats |
| Suspicious Corp | Multiple fraud indicators combined |

---

## 🛠️ Tech Stack

- **[Streamlit](https://streamlit.io/)** — Interactive web dashboard
- **[Pandas](https://pandas.pydata.org/)** — Data manipulation
- **[Plotly](https://plotly.com/python/)** — Charts and visualizations
- **[NumPy](https://numpy.org/)** — Numerical operations
- **[OpenPyXL](https://openpyxl.readthedocs.io/)** — Excel export support

---

## 🔮 Roadmap

- [ ] Live file upload for real PAYE CSV submissions
- [ ] Machine learning models for advanced anomaly detection
- [ ] Real-time API integration with NAPSA and PACRA
- [ ] Salary benchmarking against industry/province standards
- [ ] Network analysis to detect clusters of related fraudulent entities
- [ ] Mobile app for field verification by ZRA officers

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you'd like to change.

1. Fork the repository
2. Create your branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "Add your feature"`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a Pull Request

---

## 📄 License

This project was built for the ZRA Hackathon. See the repository for licensing details.

---

*Built with ❤️ for the Zambia Revenue Authority Hackathon*