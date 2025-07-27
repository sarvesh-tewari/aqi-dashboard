# 📋 AQI Dashboard - Usage Instructions

## 🚀 **Quick Start Guide**

### **For First-Time Setup**

1. **Clone/Download the Project**
   ```bash
   # If you have the project locally, navigate to it:
   cd aqi-dashboard
   ```

2. **Run Automated Setup**
   ```bash
   python setup.py
   ```
   This will:
   - ✅ Check Python version (3.8+ required)
   - ✅ Create virtual environment
   - ✅ Install all dependencies
   - ✅ Check if data exists

3. **Activate Virtual Environment**
   ```bash
   # On macOS/Linux:
   source venv-aqi/bin/activate
   
   # On Windows:
   venv-aqi\Scripts\activate
   ```

4. **Start the Dashboard**
   ```bash
   streamlit run dashboard.py
   ```

5. **Open Your Browser**
   - Go to: `http://localhost:8501`
   - The dashboard will load automatically

---

## 📊 **Dashboard Features**

### **🏙️ City Selection**
- Use the sidebar to select which cities to analyze
- Choose from: Lucknow, Mysuru, Delhi, Dehradun
- You can select multiple cities for comparison

### **📅 Time Filters**
- **Year Filter**: Select specific years (2017-2025)
- **Date Range**: Choose custom start and end dates
- **AQI Range**: Filter by minimum and maximum AQI values

### **📈 Dashboard Tabs**

#### **1. Overview Tab**
- **Key Metrics**: Total records, data completeness, average AQI, peak AQI
- **Summary Statistics**: Detailed statistical analysis by city
- **Data Quality**: Missing data tracking and reporting

#### **2. Time Series Analysis**
- **Interactive Line Charts**: AQI trends over time
- **AQI Category Lines**: Visual reference for air quality levels
- **Multi-city Comparison**: Compare trends across cities
- **Hover Information**: Detailed data on hover

#### **3. City Comparison**
- **Box Plots**: AQI distribution analysis by city
- **Bar Charts**: Average AQI comparison with error bars
- **Statistical Insights**: Mean, standard deviation, data counts

#### **4. Monthly Analysis**
- **Heatmap**: Monthly average AQI patterns
- **Seasonal Trends**: Identify seasonal air quality patterns
- **City-Month Matrix**: Easy comparison across cities and months

#### **5. Data Table**
- **Raw Data View**: Complete dataset in tabular format
- **Sorting**: Click column headers to sort
- **CSV Export**: Download filtered data for further analysis

---

## 🔄 **Adding New Cities**

### **Step 1: Update the Scraper**
Edit `aqi_scraper.py` and add new cities to the list:
```python
cities_to_download = [
    ("Uttar Pradesh", "Lucknow"),
    ("Karnataka", "Mysuru"),
    ("Delhi", "Delhi"),
    ("Uttarakhand", "Dehradun"),
    ("New State", "New City"),  # Add your new city here
]
```

### **Step 2: Collect Data**
```bash
# Make sure virtual environment is activated
source venv-aqi/bin/activate

# Run the scraper
python aqi_scraper.py
```

### **Step 3: Organize Downloads**
```bash
# Move downloaded files to project structure
python organize_downloads.py
```

### **Step 4: Process Data**
```bash
# Clean and standardize the data
python process_aqi_data.py
```

### **Step 5: Restart Dashboard**
```bash
# The dashboard will automatically include new cities
streamlit run dashboard.py
```

---

## 🛠️ **Troubleshooting**

### **Common Issues & Solutions**

#### **1. "streamlit: command not found"**
```bash
# Solution: Activate virtual environment first
source venv-aqi/bin/activate
streamlit run dashboard.py
```

#### **2. "ModuleNotFoundError"**
```bash
# Solution: Install dependencies
pip install -r requirements.txt
```

#### **3. "ChromeDriver not found"**
- Ensure Chrome browser is installed
- Download chromedriver for your Chrome version
- Place it in the project root directory

#### **4. "Data files not found"**
```bash
# Solution: Run data collection and processing
python aqi_scraper.py
python organize_downloads.py
python process_aqi_data.py
```

#### **5. "Port 8501 already in use"**
```bash
# Solution: Use a different port
streamlit run dashboard.py --server.port 8502
```

---

## 📊 **Data Collection Process**

### **Manual Data Collection**
If you need to collect data for new cities:

1. **Prepare the Scraper**
   ```bash
   # Edit aqi_scraper.py to add new cities
   # Add to cities_to_download list
   ```

2. **Run Collection**
   ```bash
   python aqi_scraper.py
   # This will download Excel files to your Downloads folder
   ```

3. **Organize Files**
   ```bash
   python organize_downloads.py
   # This moves files to data/city_name/ folders
   ```

4. **Process Data**
   ```bash
   python process_aqi_data.py
   # This creates the parquet file for the dashboard
   ```

---

## 🎯 **Advanced Usage**

### **Custom Data Analysis**

#### **Export Filtered Data**
1. Use sidebar filters to select your criteria
2. Go to "Data Table" tab
3. Click "Download Data as CSV"
4. Use the CSV file in Excel, Python, or other tools

#### **Compare Specific Time Periods**
1. Use "Date Range" filter in sidebar
2. Select specific years or date range
3. Compare cities during those periods

#### **Analyze AQI Categories**
- **Good (0-50)**: Green line on charts
- **Moderate (51-100)**: Yellow line on charts
- **Unhealthy for Sensitive Groups (101-150)**: Orange line
- **Unhealthy (151-200)**: Red line
- **Very Unhealthy (201-300)**: Purple line

### **Performance Tips**
- **Caching**: Data is cached for faster loading
- **Filtering**: Use sidebar filters to reduce data load
- **Export**: Download filtered data for external analysis

---

## 📁 **File Structure Reference**

```
aqi-dashboard/
├── README.md                    # 📚 Main documentation
├── requirements.txt             # 📦 Dependencies
├── setup.py                    # 🚀 Automated setup
├── dashboard.py                 # 📊 Main dashboard
├── aqi_scraper.py              # 🕷️ Data collection
├── process_aqi_data.py         # 🔄 Data processing
├── organize_downloads.py       # 📁 File organization
├── data/
│   ├── Lucknow/                # 📊 Raw data
│   ├── Mysuru/
│   ├── Delhi/
│   ├── Dehradun/
│   └── processed/
│       ├── aqi_data.parquet    # 📈 Processed data
│       └── aqi_summary.json    # 📊 Summary stats
└── venv-aqi/                   # 🐍 Virtual environment
```

---

## 🔧 **Development Commands**

### **Setup Commands**
```bash
# Create virtual environment
python -m venv venv-aqi

# Activate virtual environment
source venv-aqi/bin/activate  # macOS/Linux
venv-aqi\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run setup script
python setup.py
```

### **Data Pipeline Commands**
```bash
# Collect data
python aqi_scraper.py

# Organize files
python organize_downloads.py

# Process data
python process_aqi_data.py
```

### **Dashboard Commands**
```bash
# Start dashboard
streamlit run dashboard.py

# Start on specific port
streamlit run dashboard.py --server.port 8502

# Start with debug info
streamlit run dashboard.py --logger.level debug
```

---

## 📊 **Data Coverage Reference**

| City | Years | Records | AQI Range | Status |
|------|-------|---------|-----------|--------|
| **Delhi** | 2017-2025 | 2,979 | 41-494 | ✅ Complete |
| **Lucknow** | 2017-2025 | 2,910 | 29-487 | ✅ Complete |
| **Mysuru** | 2019-2025 | 1,849 | 17-217 | ✅ Complete |
| **Dehradun** | 2022-2025 | 948 | 18-327 | ✅ Complete |

---

## 🚀 **Future Enhancements**

### **Planned Features**
- **🌡️ Weather Integration**: Temperature and rainfall data
- **📊 More Cities**: Expand to additional Indian cities
- **🔍 Advanced Analytics**: Trend analysis and forecasting
- **📱 Mobile Optimization**: Enhanced mobile experience
- **🌍 Geographic Visualization**: Map-based city selection

### **Custom Indicators**
- **Custom AQI Calculations**: Add your own indicators
- **Health Impact Analysis**: Correlate AQI with health data
- **Policy Impact Assessment**: Analyze policy effectiveness
- **Predictive Modeling**: Forecast future AQI trends

---

## 📞 **Support & Resources**

### **Documentation**
- **README.md**: Comprehensive project overview
- **PROJECT_SUMMARY.md**: Clean project summary
- **This file**: Detailed usage instructions

### **Troubleshooting**
1. Check the troubleshooting section above
2. Verify all dependencies are installed
3. Ensure data files are in correct locations
4. Check console output for error messages

### **Getting Help**
- Check the README.md for detailed setup instructions
- Use the setup.py script for automated installation
- Review the troubleshooting section in this guide

---

## 🎯 **Quick Reference Commands**

```bash
# Setup
python setup.py

# Activate environment
source venv-aqi/bin/activate

# Start dashboard
streamlit run dashboard.py

# Collect data for new cities
python aqi_scraper.py
python organize_downloads.py
python process_aqi_data.py

# Check data files
ls data/processed/
```

---

**🌬️ Breathe Easy, Stay Informed!**

*Keep this guide handy for future reference.* 📋 