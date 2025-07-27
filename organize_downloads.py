#!/usr/bin/env python3
"""
Organize downloaded AQI data files
Moves Excel files from Downloads folder to appropriate city folders
"""

import os
import shutil
import glob
from pathlib import Path

def get_downloads_folder():
    """Get the downloads folder path based on OS"""
    home = Path.home()
    
    # macOS
    if os.name == 'posix':
        return home / "Downloads"
    # Windows
    elif os.name == 'nt':
        return home / "Downloads"
    # Linux
    else:
        return home / "Downloads"

def organize_downloads():
    """Organize downloaded Excel files into city folders"""
    print("🚀 Starting file organization...")
    print("=" * 50)
    
    # Get downloads folder
    downloads_folder = get_downloads_folder()
    print(f"📁 Downloads folder: {downloads_folder}")
    
    if not downloads_folder.exists():
        print("❌ Downloads folder not found")
        return
    
    # Define cities and their patterns
    cities = {
        "Lucknow": ["Lucknow", "lucknow"],
        "Mysuru": ["Mysuru", "mysuru", "Mysore", "mysore"],
        "Delhi": ["Delhi", "delhi"],
        "Dehradun": ["Dehradun", "dehradun"],
        "Chandigarh": ["Chandigarh", "chandigarh"]
    }
    
    # Create data directory
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    organized_files = {}
    total_moved = 0
    
    # Process each city
    for city_name, patterns in cities.items():
        print(f"\n🏙️ Processing {city_name}...")
        
        # Create city folder
        city_folder = data_dir / city_name
        city_folder.mkdir(exist_ok=True)
        
        city_files = []
        
        # Look for Excel files matching city patterns
        for pattern in patterns:
            # Search for files containing the pattern
            search_pattern = f"*{pattern}*.xlsx"
            files = list(downloads_folder.glob(search_pattern))
            
            for file in files:
                # Extract year from filename
                year = None
                for i in range(2017, 2026):
                    if str(i) in file.name:
                        year = i
                        break
                
                if year is None:
                    print(f"  ⚠️ Could not extract year from {file.name}")
                    continue
                
                # Create new filename
                new_filename = f"{city_name}_{year}_AQI_Data.xlsx"
                new_path = city_folder / new_filename
                
                # Check if file already exists
                if new_path.exists():
                    print(f"  ⚠️ File already exists: {new_filename}")
                    continue
                
                try:
                    # Move the file
                    shutil.move(str(file), str(new_path))
                    city_files.append({
                        'original': file.name,
                        'new': new_filename,
                        'year': year
                    })
                    print(f"  ✅ Moved: {file.name} → {new_filename}")
                    total_moved += 1
                except Exception as e:
                    print(f"  ❌ Error moving {file.name}: {e}")
        
        organized_files[city_name] = city_files
        print(f"  📊 Total files for {city_name}: {len(city_files)}")
    
    # Print summary
    print(f"\n{'='*50}")
    print("📋 ORGANIZATION SUMMARY")
    print(f"{'='*50}")
    print(f"✅ Total files moved: {total_moved}")
    
    for city, files in organized_files.items():
        if files:
            print(f"\n🏙️ {city}:")
            for file_info in files:
                print(f"  📄 {file_info['original']} → {file_info['new']} (Year: {file_info['year']})")
        else:
            print(f"\n🏙️ {city}: No files found")
    
    print(f"\n📁 Folder structure:")
    for city in cities.keys():
        city_folder = data_dir / city
        if city_folder.exists():
            files = list(city_folder.glob("*.xlsx"))
            print(f"  📁 {city}/ ({len(files)} files)")
        else:
            print(f"  📁 {city}/ (not created)")
    
    print(f"\n🎉 File organization completed!")

if __name__ == "__main__":
    organize_downloads() 