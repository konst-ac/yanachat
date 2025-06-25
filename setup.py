#!/usr/bin/env python3
"""
YanaChat AI Script Assistant - Setup Script
"""

import os
import sys
import subprocess
import shutil

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def create_env_file():
    """Create .env file from template"""
    if os.path.exists('.env'):
        print("✅ .env file already exists!")
        return True
    
    if os.path.exists('env_template.txt'):
        shutil.copy('env_template.txt', '.env')
        print("✅ Created .env file from template!")
        print("⚠️  Please edit .env file and add your OpenAI API key!")
        return True
    else:
        print("❌ env_template.txt not found!")
        return False

def create_directories():
    """Create necessary directories"""
    directories = ['./scripts', './characters', './scenes']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    print("✅ Created necessary directories!")

def main():
    """Main setup function"""
    print("🎬 YanaChat AI Script Assistant - Setup")
    print("=" * 50)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Create .env file
    create_env_file()
    
    # Create directories
    create_directories()
    
    print("\n🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Edit the .env file and add your OpenAI API key")
    print("2. Run the application with: python run.py")
    print("   or: streamlit run app.py")
    print("\nFor help, see README.md")

if __name__ == "__main__":
    main() 