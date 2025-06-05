# 🛂 U.S. Border Crossing Dashboard

This Streamlit dashboard visualizes border crossing activity across U.S. ports using official data from [data.gov](https://data.gov).

## 🎯 Objective

To provide an interactive and insightful dashboard that enables users to:
- Analyze U.S. border crossing data
- Identify high-traffic ports and patterns
- Filter by state, transport mode (measure), and time

## 📊 Dataset

- **Source**: [Border Crossing Entry Data – data.gov](https://catalog.data.gov/dataset/border-crossing-entry-data-683ae)
- **Fields include**:
  - Port Name
  - State
  - Port Code
  - Border
  - Date (`Jan 2024` format)
  - Measure (e.g., Personal Vehicle, Pedestrian, Train)
  - Value (number of crossings)
  - Latitude / Longitude

## 🚀 Features of the Dashboard

- **Interactive Filters**:
  - Select State(s), Measure(s), and Date Range
  - “Select All” checkboxes
- **Dynamic Map**:
  - Auto-zooms to filtered ports
  - Highlights selected port from dropdown
- **KPIs**:
  - Total Crossings, Unique Ports, Top Measure
- **Charts**:
  - Top Ports Bar Chart (adjustable width)
  - Monthly Trend Line Chart
- **Lightweight Layout** using `st.columns` and `pydeck`

## 🛠️ How to Run This Dashboard Locally

### ✅ Prerequisites
- Python 3.9+ installed
- Git installed (optional but recommended)

### 📦 Install Dependencies
Open your terminal in the project folder and run:
```bash
pip install -r requirements.txt
