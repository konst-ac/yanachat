#!/usr/bin/env python3
"""
YanaChat AI Script Assistant - Startup Script
"""

import os
import sys
import subprocess

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import streamlit
        import openai
        import pandas
        import plotly
        print("✅ All dependencies are installed!")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def check_env_file():
    """Check if .env file exists"""
    if not os.path.exists('.env'):
        print("⚠️  No .env file found!")
        print("Please create a .env file with your OpenAI API key:")
        print("OPENAI_API_KEY=your_openai_api_key_here")
        print("MODEL_NAME=gpt-4")
        print("TEMPERATURE=0.7")
        print("MAX_TOKENS=2000")
        return False
    else:
        print("✅ .env file found!")
        return True

def main():
    """Main startup function"""
    print("🎬 YanaChat AI Script Assistant")
    print("=" * 40)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check environment file
    if not check_env_file():
        print("\nYou can still run the app, but AI features won't work without an API key.")
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            sys.exit(1)
    
    # Create directories if they don't exist
    directories = ['./scripts', './characters', './scenes']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    
    print("✅ Directories created!")
    print("\n🚀 Starting YanaChat...")
    print("The app will open in your browser at http://localhost:8501")
    print("Press Ctrl+C to stop the application")
    print("-" * 40)
    
    # Run Streamlit app
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"], check=True)
    except KeyboardInterrupt:
        print("\n👋 YanaChat stopped. Goodbye!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running Streamlit: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 