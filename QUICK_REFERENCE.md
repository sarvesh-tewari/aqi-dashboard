# ⚡ Quick Reference - AQI Dashboard

## 🚀 **Essential Commands**

### **Setup & Start**
```bash
# One-command setup
python setup.py

# Activate environment
source venv-aqi/bin/activate

# Start dashboard
streamlit run dashboard.py
```

### **Data Collection for New Cities**
```bash
# 1. Edit aqi_scraper.py to add new cities
# 2. Collect data
python aqi_scraper.py

# 3. Organize files
python organize_downloads.py

# 4. Process data
python process_aqi_data.py

# 5. Restart dashboard
streamlit run dashboard.py
```

### **Troubleshooting**
```bash
# If streamlit not found
source venv-aqi/bin/activate
streamlit run dashboard.py

# If dependencies missing
pip install -r requirements.txt

# If port 8501 busy
streamlit run dashboard.py --server.port 8502
```

## 📊 **Dashboard URL**
- **Local**: http://localhost:8501
- **Default Port**: 8501
- **Alternative Port**: 8502 (if 8501 is busy)

## 🏙️ **Available Cities**
- **Delhi** (2017-2025) - 2,979 records
- **Lucknow** (2017-2025) - 2,910 records  
- **Mysuru** (2019-2025) - 1,849 records
- **Dehradun** (2022-2025) - 948 records

## 📈 **Dashboard Features**
- **5 Tabs**: Overview, Time Series, City Comparison, Monthly Analysis, Data Table
- **Sidebar Filters**: City, Year, Date Range, AQI Range
- **Export**: CSV download from Data Table tab
- **Interactive**: Hover for details, click to sort

## 📁 **Key Files**
- `dashboard.py` - Main dashboard
- `aqi_scraper.py` - Data collection
- `process_aqi_data.py` - Data processing
- `organize_downloads.py` - File organization
- `setup.py` - Automated setup
- `requirements.txt` - Dependencies

## 🎯 **Adding New Cities**
1. Edit `aqi_scraper.py` → Add to `cities_to_download` list
2. Run `python aqi_scraper.py`
3. Run `python organize_downloads.py`
4. Run `python process_aqi_data.py`
5. Restart dashboard

## 🔧 **Data Files**
- **Raw Data**: `data/{city_name}/` folders
- **Processed Data**: `data/processed/aqi_data.parquet`
- **Summary**: `data/processed/aqi_summary.json`

## 📋 **Common Issues**
- **"streamlit: command not found"** → Activate virtual environment
- **"ModuleNotFoundError"** → Run `pip install -r requirements.txt`
- **"Data files not found"** → Run data collection scripts
- **"Port 8501 busy"** → Use `--server.port 8502`

---

**🌬️ Quick Reference - Keep this handy!** 📋 