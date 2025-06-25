# 🎬 YanaChat - AI Script Assistant for Filmmakers

A comprehensive AI-powered script writing assistant that helps filmmakers develop characters, manage scenes, and enhance their storytelling with intelligent text modifications using Google's Gemini AI.

## ✨ Features

### 👥 Character Management
- **Character Creation & Storage**: Create detailed character profiles with physical descriptions, personality traits, goals, and conflicts
- **Character Analysis**: AI-powered analysis of character development, dialogue style recommendations, and arc suggestions
- **Character Search**: Search through characters by name, description, or personality traits
- **Character Notes**: Add timestamped notes to track character development over time

### 🎬 Scene Management
- **Scene Creation**: Build scenes with settings, characters, action descriptions, and dialogue
- **Scene Organization**: Automatic scene numbering and chronological ordering
- **Scene Analysis**: AI-powered scene analysis for pacing, character interactions, and improvement suggestions
- **Scene Search**: Search scenes by content, setting, or characters
- **Scene Statistics**: Track scene length, character appearances, and setting diversity

### ✏️ Text Modification Tools
- **Tone Modification**: Change the tone of any text (dramatic, comedic, suspenseful, etc.)
- **Setting Adaptation**: Modify scenes to fit new settings while maintaining core elements
- **Dialogue Generation**: Generate character-specific dialogue based on context and emotion
- **Scene Expansion**: Add more detail, dialogue, action, or emotional depth
- **Scene Condensation**: Create concise versions while preserving key elements
- **Perspective Changes**: Rewrite scenes from different narrative perspectives
- **Conflict Addition**: Integrate various types of conflict into existing scenes
- **Visual Enhancement**: Add cinematic details and visual storytelling elements

### 📊 Script Analysis
- **Statistics Dashboard**: Overview of scenes, characters, settings, and average scene length
- **Character Analytics**: Age distribution, description length analysis, and character development tracking
- **Scene Analytics**: Scene length progression, character interaction patterns, and setting diversity
- **AI-Powered Insights**: Comprehensive analysis of characters and scenes with improvement suggestions

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Google Gemini API key (free tier available)

### Installation

1. **Clone or navigate to the yanachat directory:**
   ```bash
   cd yanachat
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your Gemini API key:**
   Create a `.env` file in the yanachat directory with:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   MODEL_NAME=gemini-1.5-flash
   TEMPERATURE=0.7
   MAX_TOKENS=2000
   ```

4. **Run the application:**
   ```bash
   streamlit run app.py
   ```

5. **Open your browser:**
   Navigate to `http://localhost:8501` to access the application.

## 📁 Project Structure

```
yanachat/
├── app.py                 # Main Streamlit application
├── config.py             # Configuration management
├── llm_client.py         # Google Gemini API client
├── character_manager.py  # Character management system
├── scene_manager.py      # Scene management system
├── text_modifier.py      # Text modification tools
├── requirements.txt      # Python dependencies
├── README.md            # This file
├── scripts/             # Script storage directory
├── characters/          # Character data storage
└── scenes/              # Scene data storage
```

## 🎯 How to Use

### 1. Dashboard
- Start with the dashboard to get an overview of your script
- View statistics about scenes, characters, and settings
- See recent activity and quick access to recent items

### 2. Character Management
- Click "Characters" in the sidebar
- Use "Add New Character" to create detailed character profiles
- Search and filter characters as your cast grows
- Use AI analysis to get character development suggestions

### 3. Scene Management
- Click "Scenes" in the sidebar
- Create scenes with scene numbers, settings, characters, and content
- Organize scenes chronologically
- Use AI analysis to improve scene structure and pacing

### 4. Text Tools
- Click "Text Tools" in the sidebar
- Paste any text (scene, dialogue, description) into the text area
- Choose from various modification options:
  - Change tone or style
  - Add visual elements
  - Improve dialogue
  - Expand or condense content
  - Change perspective
  - Add conflict
  - Enhance character development

### 5. Script Analysis
- Click "Script Analysis" in the sidebar
- View comprehensive statistics and analytics
- Generate AI-powered insights for improvement
- Track character and scene development over time

## 🔧 Configuration Options

You can customize the application by modifying the `.env` file:

- `GEMINI_API_KEY`: Your Google Gemini API key
- `MODEL_NAME`: Gemini model to use (default: gemini-1.5-flash)
- `TEMPERATURE`: Creativity level for AI responses (0.0-1.0)
- `MAX_TOKENS`: Maximum tokens for AI responses
- `SCRIPT_FILE_PATH`: Directory for script storage
- `CHARACTER_FILE_PATH`: Directory for character data
- `SCENE_FILE_PATH`: Directory for scene data

## 💡 Tips for Best Results

1. **Character Development**: Start by creating detailed character profiles before writing scenes
2. **Scene Organization**: Use consistent scene numbering for better organization
3. **AI Analysis**: Regularly use AI analysis to get fresh perspectives on your work
4. **Text Modifications**: Use the text tools to experiment with different approaches
5. **Notes**: Add notes to characters and scenes to track development ideas

## 🤝 Contributing

This is a personal project, but suggestions and improvements are welcome! The application is designed to be modular and extensible.

## 📝 License

This project is for educational and personal use. Please respect Google's terms of service when using their API.

## 🆘 Troubleshooting

### Common Issues:

1. **API Key Error**: Make sure your Gemini API key is correctly set in the `.env` file
2. **Import Errors**: Ensure all dependencies are installed with `pip install -r requirements.txt`
3. **File Permissions**: Make sure the application has write permissions for the data directories
4. **Streamlit Issues**: Try clearing Streamlit cache with `streamlit cache clear`

### Getting Help:
- Check that all required packages are installed
- Verify your Gemini API key is valid and has sufficient credits
- Ensure you're running the latest version of Python

---

**Happy Scriptwriting! 🎬✨** 