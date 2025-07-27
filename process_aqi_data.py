#!/usr/bin/env python3
"""
AQI Data Processing Script
Processes downloaded Excel files and converts them to a standardized format
"""

import pandas as pd
import os
import json
from pathlib import Path
import numpy as np

def process_excel_file(file_path, city_name, year):
    """Process a single Excel file and return cleaned data"""
    try:
        # Read the Excel file
        df = pd.read_excel(file_path)
        
        # Check for the day column (some files use 'Day', others use 'Date')
        day_column = None
        if 'Day' in df.columns:
            day_column = 'Day'
        elif 'Date' in df.columns:
            day_column = 'Date'
        else:
            print(f"❌ No day column found in {file_path}")
            return None
        
        # Create a standardized dataframe
        processed_data = []
        
        for _, row in df.iterrows():
            day = row[day_column]
            
            # Skip if day is NaN or invalid
            if pd.isna(day) or day == '':
                continue
            
            # Convert day to integer if it's not already
            try:
                day = int(day)
            except (ValueError, TypeError):
                continue
            
            # Process each month column - handle both abbreviated and full month names
            month_mappings = {
                # Abbreviated names
                'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
                'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12,
                # Full names
                'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6,
                'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12
            }
            
            for month_name, month_num in month_mappings.items():
                if month_name in df.columns:
                    aqi_value = row[month_name]
                    
                    # Skip if AQI value is NaN or invalid
                    if pd.isna(aqi_value) or aqi_value == '' or aqi_value == '-':
                        continue
                    
                    # Convert to numeric
                    try:
                        aqi_value = float(aqi_value)
                    except (ValueError, TypeError):
                        continue
                    
                    # Create date
                    try:
                        date_obj = pd.to_datetime(f"{year}-{month_num:02d}-{day:02d}")
                    except:
                        continue
                    
                    processed_data.append({
                        'city': city_name,
                        'year': year,
                        'month': month_num,
                        'day': day,
                        'date': date_obj,
                        'aqi_value': aqi_value,
                        'data_quality': 'available',
                        'missing_data': False
                    })
        
        if processed_data:
            return pd.DataFrame(processed_data)
        else:
            print(f"⚠️ No valid data found in {file_path}")
            return None
            
    except Exception as e:
        print(f"❌ Error processing {file_path}: {e}")
        return None

def create_missing_data_records(city_name, missing_years):
    """Create placeholder records for missing years"""
    missing_records = []
    
    for year in missing_years:
        # Create records for each day of each month
        for month in range(1, 13):
            days_in_month = pd.Period(f"{year}-{month:02d}").days_in_month
            
            for day in range(1, days_in_month + 1):
                try:
                    date_obj = pd.to_datetime(f"{year}-{month:02d}-{day:02d}")
                    
                    missing_records.append({
                        'city': city_name,
                        'year': year,
                        'month': month,
                        'day': day,
                        'date': date_obj,
                        'aqi_value': np.nan,
                        'data_quality': 'missing',
                        'missing_data': True
                    })
                except:
                    continue
    
    return pd.DataFrame(missing_records)

def process_all_cities():
    """Process all cities and create the final dataset"""
    print("🚀 Starting AQI Data Processing")
    print("=" * 50)
    
    # Define cities to process
    cities = ["Lucknow", "Mysuru", "Delhi", "Dehradun", "Chandigarh"]
    
    all_data = []
    missing_data_tracker = {}
    
    for city in cities:
        print(f"\n🏙️ Processing {city}...")
        
        city_data = []
        processed_years = set()
        
        # Look for Excel files in the city's folder
        city_folder = f"data/{city}"
        
        if not os.path.exists(city_folder):
            print(f"❌ Folder not found: {city_folder}")
            continue
        
        # Find all Excel files for this city
        excel_files = []
        for file in os.listdir(city_folder):
            if file.endswith(('.xlsx', '.xls')) and city in file:
                excel_files.append(file)
        
        if not excel_files:
            print(f"❌ No Excel files found for {city}")
            continue
        
        print(f"📁 Found {len(excel_files)} Excel files")
        
        # Process each Excel file
        for file in excel_files:
            file_path = os.path.join(city_folder, file)
            
            # Extract year from filename
            year = None
            for i in range(2017, 2026):
                if str(i) in file:
                    year = i
                    break
            
            if year is None:
                print(f"⚠️ Could not extract year from {file}")
                continue
            
            print(f"  📊 Processing {file} (Year: {year})")
            
            # Process the file
            df = process_excel_file(file_path, city, year)
            
            if df is not None and not df.empty:
                city_data.append(df)
                processed_years.add(year)
                print(f"    ✅ Processed {len(df)} records")
            else:
                print(f"    ❌ No data processed")
        
        # Check for missing years and create placeholders
        expected_years = set(range(2017, 2026))
        missing_years = expected_years - processed_years
        
        if missing_years:
            print(f"    ❌ Missing data for years: {sorted(missing_years)}")
            missing_data_tracker[city] = sorted(missing_years)
        
        if city_data:
            city_df = pd.concat(city_data, ignore_index=True)
            city_df['data_quality'] = 'available'
            city_df['missing_data'] = False
            
            if missing_years:
                missing_df = create_missing_data_records(city, missing_years)
                city_df = pd.concat([city_df, missing_df], ignore_index=True)
                print(f"    📊 Added {len(missing_df)} missing data placeholders")
            
            all_data.append(city_df)
            print(f"  ✅ Total records for {city}: {len(city_df)}")
        else:
            print(f"  ❌ No data processed for {city}")
    
    if all_data:
        # Combine all city data
        final_df = pd.concat(all_data, ignore_index=True)
        
        # Sort by city, date
        final_df = final_df.sort_values(['city', 'date'])
        
        # Create output directory
        output_dir = "data/processed"
        os.makedirs(output_dir, exist_ok=True)
        
        # Save as Parquet file
        output_file = os.path.join(output_dir, "aqi_data.parquet")
        final_df.to_parquet(output_file, index=False)
        
        # Create summary statistics
        summary = {
            "total_records": int(len(final_df)),
            "cities": list(final_df['city'].unique()),
            "years": [int(year) for year in sorted(final_df['year'].unique())],
            "data_quality": {
                "available": int(len(final_df[final_df['data_quality'] == 'available'])),
                "missing": int(len(final_df[final_df['data_quality'] == 'missing']))
            },
            "missing_data_by_city": {city: [int(year) for year in years] for city, years in missing_data_tracker.items()}
        }
        
        # Save summary
        summary_file = os.path.join(output_dir, "aqi_summary.json")
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"\n✅ Processing completed!")
        print(f"📊 Total records: {len(final_df):,}")
        print(f"🏙️ Cities: {', '.join(summary['cities'])}")
        print(f"📅 Years: {summary['years']}")
        print(f"📁 Output: {output_file}")
        print(f"📋 Summary: {summary_file}")
        
        # Print missing data summary
        if missing_data_tracker:
            print(f"\n⚠️ Missing Data Summary:")
            for city, years in missing_data_tracker.items():
                print(f"  {city}: {years}")
        
        return True
    else:
        print("❌ No data to process")
        return False

if __name__ == "__main__":
    success = process_all_cities()
    if success:
        print("\n🎉 Data processing completed successfully!")
    else:
        print("\n❌ Data processing failed!") 