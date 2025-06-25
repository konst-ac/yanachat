import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    # Google Gemini Configuration
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
    MODEL_NAME = os.getenv('MODEL_NAME', 'gemini-1.5-flash')
    TEMPERATURE = float(os.getenv('TEMPERATURE', '0.7'))
    MAX_TOKENS = int(os.getenv('MAX_TOKENS', '2000'))
    
    # File Paths
    SCRIPT_FILE_PATH = os.getenv('SCRIPT_FILE_PATH', './scripts/')
    CHARACTER_FILE_PATH = os.getenv('CHARACTER_FILE_PATH', './characters/')
    SCENE_FILE_PATH = os.getenv('SCENE_FILE_PATH', './scenes/')
    LOCATION_FILE_PATH = os.getenv('LOCATION_FILE_PATH', './locations/')
    
    # Ensure directories exist
    @staticmethod
    def create_directories():
        """Create necessary directories if they don't exist"""
        directories = [
            Config.SCRIPT_FILE_PATH,
            Config.CHARACTER_FILE_PATH,
            Config.SCENE_FILE_PATH,
            Config.LOCATION_FILE_PATH
        ]
        for directory in directories:
            os.makedirs(directory, exist_ok=True) 