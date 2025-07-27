# 🌬️ AQI Dashboard - India Air Quality Analysis

A comprehensive Air Quality Index (AQI) analysis dashboard for Indian cities, featuring interactive visualizations and data processing capabilities.

## 🏙️ Cities Covered

- **Lucknow** (Uttar Pradesh)
- **Mysuru** (Karnataka) 
- **Delhi** (Delhi)
- **Dehradun** (Uttarakhand)
- **Chandigarh** (Chandigarh)

## 📊 Features

### 📈 Interactive Dashboard
- **City Metrics**: Year-wise AQI statistics, days above/below thresholds, peak AQI values
- **Time Series**: Interactive line charts showing AQI trends over time
- **City Comparison**: Side-by-side comparison of multiple cities
- **Monthly Analysis**: Heatmap visualization with year-wise filtering
- **Data Table**: Raw data view with download capabilities

### 🔧 Data Processing
- **Automated Scraping**: Selenium-based web scraper for CPCB data
- **Data Cleaning**: Standardized processing of Excel files
- **Missing Data Handling**: Placeholder records for missing years/months
- **Parquet Storage**: Efficient columnar data format

### 📁 Project Structure
```
aqi-dashboard/
├── dashboard.py              # Main Streamlit dashboard
├── aqi_scraper.py           # Web scraping script
├── process_aqi_data.py      # Data processing script
├── organize_downloads.py    # File organization script
├── setup.py                 # Environment setup
├── requirements.txt         # Python dependencies
├── data/                   # Data storage
│   ├── Lucknow/           # City-specific Excel files
│   ├── Mysuru/
│   ├── Delhi/
│   ├── Dehradun/
│   ├── Chandigarh/
│   └── processed/         # Processed Parquet files
└── scripts/               # Additional utilities
```

## 🚀 Quick Start

### 1. Setup Environment
```bash
# Clone the repository
git clone <repository-url>
cd aqi-dashboard

# Setup Python environment
python setup.py
```

### 2. Run Dashboard
```bash
# Activate virtual environment
source venv-aqi/bin/activate

# Start dashboard
streamlit run dashboard.py
```

### 3. Access Dashboard
Open your browser and go to: `http://localhost:8501`

## 📋 Usage Instructions

### Adding New Cities
1. **Download Data**: Use `aqi_scraper.py` or manually download from CPCB
2. **Organize Files**: Run `organize_downloads.py` to move files to correct folders
3. **Process Data**: Run `process_aqi_data.py` to update the dataset
4. **Update Dashboard**: Restart the dashboard to see new cities

### Data Collection Commands
```bash
# Download data for all cities
python aqi_scraper.py

# Organize downloaded files
python organize_downloads.py

# Process and update dataset
python process_aqi_data.py
```

## 🛠️ Technical Details

### Data Sources
- **CPCB Website**: Central Pollution Control Board official data
- **Years**: 2017-2025 (varies by city)
- **Format**: Daily AQI values by month

### Technologies Used
- **Python**: Core programming language
- **Streamlit**: Interactive web dashboard
- **Selenium**: Web scraping automation
- **Pandas**: Data processing and analysis
- **Plotly**: Interactive visualizations
- **Parquet**: Efficient data storage

### Data Quality
- **Available Data**: Actual AQI measurements
- **Missing Data**: Placeholder records with quality indicators
- **Validation**: Automatic data quality checks

## 📊 Dashboard Features

### City Metrics Tab
- Days with AQI > 100 (Poor air quality)
- Days with AQI < 50 (Good air quality)
- Peak AQI values by year
- Year-wise summary statistics

### Time Series Tab
- Interactive line charts
- Multi-city comparison
- Date range filtering
- AQI threshold highlighting

### City Comparison Tab
- Side-by-side city analysis
- Statistical comparisons
- Trend analysis

### Monthly Analysis Tab
- Heatmap visualization
- Year-wise filtering
- Red color scale for AQI intensity
- Complete 12-month view

### Data Table Tab
- Raw data view
- CSV download functionality
- Filtered data export

## 🔧 Troubleshooting

### Common Issues
1. **Streamlit not found**: Ensure virtual environment is activated
2. **Data not loading**: Check if processed files exist in `data/processed/`
3. **Scraping errors**: Verify internet connection and CPCB website availability

### Environment Setup
```bash
# If setup.py fails, manually install dependencies
pip install -r requirements.txt

# For Chrome WebDriver issues
# Download chromedriver and place in project root
```

## 📈 Data Statistics

- **Total Records**: ~14,000 AQI measurements
- **Cities**: 5 major Indian cities
- **Time Period**: 2017-2025
- **Data Quality**: Mixed (available + missing placeholders)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is for educational and research purposes. Please respect data source terms and conditions.

## 🙏 Acknowledgments

- **CPCB**: Central Pollution Control Board for data
- **Streamlit**: Interactive dashboard framework
- **Open Source Community**: Various Python libraries

---

**🌬️ Breathe Easy, Analyze Smart** 📊
