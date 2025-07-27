#!/usr/bin/env python3
"""
Setup script for AQI Dashboard project
"""

import os
import sys
import subprocess
import platform

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required. Current version:", sys.version)
        return False
    print(f"✅ Python version: {sys.version}")
    return True

def create_virtual_environment():
    """Create virtual environment if it doesn't exist"""
    venv_path = "venv-aqi"
    
    if os.path.exists(venv_path):
        print(f"✅ Virtual environment already exists: {venv_path}")
        return True
    
    print("📦 Creating virtual environment...")
    try:
        subprocess.run([sys.executable, "-m", "venv", venv_path], check=True)
        print(f"✅ Virtual environment created: {venv_path}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error creating virtual environment: {e}")
        return False

def install_dependencies():
    """Install project dependencies"""
    print("📦 Installing dependencies...")
    
    # Determine the correct pip path
    if platform.system() == "Windows":
        pip_path = "venv-aqi\\Scripts\\pip"
    else:
        pip_path = "venv-aqi/bin/pip"
    
    try:
        subprocess.run([pip_path, "install", "-r", "requirements.txt"], check=True)
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def check_data_files():
    """Check if data files exist"""
    data_path = "data/processed/aqi_data.parquet"
    
    if os.path.exists(data_path):
        print(f"✅ Data files found: {data_path}")
        return True
    else:
        print(f"⚠️  Data files not found: {data_path}")
        print("   Run the data collection and processing scripts to generate data")
        return False

def print_next_steps():
    """Print next steps for the user"""
    print("\n" + "="*60)
    print("🎉 SETUP COMPLETE!")
    print("="*60)
    
    print("\n📋 Next Steps:")
    print("1. Activate virtual environment:")
    if platform.system() == "Windows":
        print("   venv-aqi\\Scripts\\activate")
    else:
        print("   source venv-aqi/bin/activate")
    
    print("\n2. If you don't have data yet, collect it:")
    print("   python aqi_scraper.py")
    print("   python organize_downloads.py")
    print("   python process_aqi_data.py")
    
    print("\n3. Start the dashboard:")
    print("   streamlit run dashboard.py")
    
    print("\n4. Open your browser to: http://localhost:8501")
    
    print("\n📚 For more information, see README.md")

def main():
    """Main setup function"""
    print("🌬️ AQI Dashboard Setup")
    print("="*40)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Create virtual environment
    if not create_virtual_environment():
        return False
    
    # Install dependencies
    if not install_dependencies():
        return False
    
    # Check data files
    check_data_files()
    
    # Print next steps
    print_next_steps()
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 