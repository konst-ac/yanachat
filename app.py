import streamlit as st
import os

# Page configuration - MUST be the first Streamlit command
st.set_page_config(
    page_title="YanaChat - AI Script Assistant",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Now import other modules
import pandas as pd
from datetime import datetime
import plotly.express as px
from streamlit_option_menu import option_menu
import json

# Import our modules
from config import Config
from character_manager import CharacterManager
from scene_manager import SceneManager
from location_manager import LocationManager
from text_modifier import TextModifier
from llm_client import LLMClient
from chat_manager import ChatManager
from word_exporter import WordExporter
from scene_generator import SceneGenerator
from sample_data import add_sample_data_to_managers

# Import new user management modules
from user_manager import UserManager
from login_interface import LoginInterface
from script_selector import ScriptSelector
from script_aware_manager import ScriptAwareManager

# Initialize configuration
Config.create_directories()

# Initialize user manager
@st.cache_resource
def get_user_manager():
    return UserManager()

user_manager = get_user_manager()

# Initialize login interface
login_interface = LoginInterface(user_manager)

# Check authentication
is_authenticated, username = login_interface.render_login()

if not is_authenticated:
    st.stop()

# User is authenticated, show logout in sidebar
login_interface.render_logout()

# Initialize script selector
script_selector = ScriptSelector(user_manager)

# Initialize script-aware manager
script_aware_manager = ScriptAwareManager(user_manager)

# Initialize managers (keeping original for compatibility with other features)
@st.cache_resource
def get_managers():
    return CharacterManager(), SceneManager(), LocationManager(), TextModifier(), LLMClient(), ChatManager(), WordExporter()

character_manager, scene_manager, location_manager, text_modifier, llm_client, chat_manager, word_exporter = get_managers()

# Initialize scene generator with script-aware manager
scene_generator = SceneGenerator(script_aware_manager, script_aware_manager, script_aware_manager, llm_client)

# Sidebar navigation
with st.sidebar:
    st.markdown("## 🎬 YanaChat")
    st.markdown("AI Script Assistant for Filmmakers")
    
    selected = option_menu(
        menu_title="Navigation",
        options=["Script Manager", "Dashboard", "Characters", "Locations", "Scene Generator", "Scenes", "Text Tools", "Script Analysis", "Chat"],
        icons=["folder", "house", "person", "geo-alt", "film", "list", "pencil", "graph-up", "chat"],
        menu_icon="cast",
        default_index=0,
    )

# Custom CSS for modern styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .section-header {
        font-size: 2rem;
        font-weight: bold;
        color: #2c3e50;
        margin-bottom: 1rem;
        border-bottom: 3px solid #3498db;
        padding-bottom: 0.5rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 1rem 0;
    }
    .character-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border-left: 5px solid #3498db;
    }
    .scene-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border-left: 5px solid #e74c3c;
    }
    .chat-message-user {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 12px 16px;
        border-radius: 18px 18px 4px 18px;
        margin: 8px 0;
        max-width: 80%;
        margin-left: auto;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .chat-message-ai {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 12px 16px;
        border-radius: 18px 18px 18px 4px;
        margin: 8px 0;
        max-width: 80%;
        margin-right: auto;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 2rem;
        font-weight: bold;
        min-height: 44px;
        font-size: 0.9rem;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .suggestion-button {
        background: transparent;
        border: 2px solid #667eea;
        color: #667eea;
        border-radius: 15px;
        padding: 8px 16px;
        margin: 4px;
        font-size: 0.9rem;
        transition: all 0.3s ease;
    }
    .suggestion-button:hover {
        background: #667eea;
        color: white;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }
    .chat-suggestion-button {
        background: transparent;
        border: 1px solid #667eea;
        color: #667eea;
        border-radius: 10px;
        padding: 4px 8px;
        margin: 2px;
        font-size: 0.8rem;
        transition: all 0.3s ease;
        width: 100%;
    }
    .chat-suggestion-button:hover {
        background: #667eea;
        color: white;
        transform: translateY(-1px);
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .scene-action-button {
        min-height: 44px;
        font-size: 0.9rem;
        font-weight: 600;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        transition: all 0.3s ease;
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# Script Manager
if selected == "Script Manager":
    st.markdown('<h1 class="section-header">📚 Script Manager</h1>', unsafe_allow_html=True)
    
    # Render script selector
    current_script_id = script_selector.render_script_selector(username)
    
    if current_script_id:
        st.session_state.current_script_id = current_script_id
        script_selector.render_script_actions(username, current_script_id)
    else:
        st.info("Please create or select a script to continue!")
        st.stop()

# Check if script is selected for other sections
if selected != "Script Manager":
    if 'current_script_id' not in st.session_state:
        st.error("Please go to Script Manager and select a script first!")
        st.stop()

# Dashboard
if selected == "Dashboard":
    st.markdown('<h1 class="main-header">🎬 YanaChat AI Script Assistant</h1>', unsafe_allow_html=True)
    
    # Statistics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        stats = script_aware_manager.get_scene_statistics(username)
        st.markdown(f"""
        <div class="metric-card">
            <h3>📊 Total Scenes</h3>
            <h2>{stats['total_scenes']}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3>👥 Characters</h3>
            <h2>{stats['unique_characters']}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h3>📍 Locations</h3>
            <h2>{stats['unique_locations']}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        avg_length = int(stats['average_scene_length'])
        st.markdown(f"""
        <div class="metric-card">
            <h3>📝 Avg Scene Length</h3>
            <h2>{avg_length} chars</h2>
        </div>
        """, unsafe_allow_html=True)
    
    # Recent Activity
    st.markdown('<h2 class="section-header">Recent Activity</h2>', unsafe_allow_html=True)
    
    # Quick export section
    scenes = script_aware_manager.get_scene_sequence(username)
    if scenes:
        st.subheader("📄 Quick Export")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📥 Export All Scenes to Word", type="primary"):
                try:
                    characters = list(script_aware_manager.get_characters(username).values())
                    filepath = word_exporter.export_scenes_to_word(scenes, characters, "My Screenplay", "Screenwriter")
                    
                    with open(filepath, 'rb') as f:
                        st.download_button(
                            label="📥 Download Full Script",
                            data=f.read(),
                            file_name=os.path.basename(filepath),
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                        )
                    st.success("Script exported successfully!")
                except Exception as e:
                    st.error(f"Error exporting: {str(e)}")
        
        with col2:
            st.info(f"📊 {len(scenes)} scenes ready for export")
    else:
        # Sample data generation
        st.subheader("🎬 Get Started")
        st.info("No scenes created yet. Start by adding your first scene!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📝 Recent Scenes")
        scenes = script_aware_manager.get_scene_sequence(username)
        if scenes:
            for scene in scenes[-3:]:
                with st.expander(f"Scene {scene.get('scene_number', 'N/A')}: {scene.get('title', 'No title')}"):
                    st.write(f"**Location:** {scene.get('location', 'No location')}")
                    st.write(f"**Characters:** {', '.join(scene.get('characters', [])) if isinstance(scene.get('characters', []), list) else scene.get('characters', 'None')}")
                    st.write(f"**Action:** {scene.get('action', 'No action')[:100]}...")
        else:
            st.info("No scenes created yet. Start by adding your first scene!")
    
    with col2:
        st.subheader("👥 Recent Characters")
        characters = script_aware_manager.get_characters(username)
        if characters:
            for char_id, char in list(characters.items())[-3:]:
                with st.expander(f"{char.get('name', 'Unknown')}"):
                    st.write(f"**Age:** {char.get('age', 'Unknown')}")
                    st.write(f"**Description:** {char.get('description', 'No description')[:100]}...")
        else:
            st.info("No characters created yet. Start by adding your first character!")

# Characters Management
elif selected == "Characters":
    st.markdown('<h1 class="section-header">👥 Character Management</h1>', unsafe_allow_html=True)
    
    # Character creation
    with st.expander("➕ Add New Character", expanded=False):
        with st.form("add_character"):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Character Name")
                age = st.number_input("Age", min_value=0, max_value=120, value=25)
                description = st.text_area("Physical Description")
            
            with col2:
                personality = st.text_area("Personality Traits")
                goals = st.text_area("Character Goals")
                conflicts = st.text_area("Internal/External Conflicts")
            
            if st.form_submit_button("Add Character"):
                if name:
                    character_data = {
                        'name': name,
                        'age': age,
                        'description': description,
                        'personality': personality,
                        'goals': goals,
                        'conflicts': conflicts
                    }
                    
                    if script_aware_manager.add_character(username, character_data):
                        st.success(f"Character '{name}' added successfully!")
                        st.rerun()
                    else:
                        st.error("Character already exists or error occurred.")
                else:
                    st.error("Please enter a character name.")
    
    # Character list and management
    st.subheader("📋 Character List")
    
    # Search functionality
    search_query = st.text_input("🔍 Search characters...")
    
    if search_query:
        characters = script_aware_manager.search_characters(username, search_query)
    else:
        characters = script_aware_manager.get_characters(username)
    
    if characters:
        for character_id, character in characters.items():
            with st.container():
                st.markdown(f"""
                <div class="character-card">
                    <h3>{character.get('name', 'Unknown')}</h3>
                    <p><strong>Age:</strong> {character.get('age', 'Unknown')}</p>
                    <p><strong>Description:</strong> {character.get('description', 'No description')}</p>
                    <p><strong>Personality:</strong> {character.get('personality', 'No personality traits')}</p>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button(f"Edit {character.get('name')}", key=f"edit_{character_id}"):
                        st.session_state.editing_character = character_id
                
                with col2:
                    if st.button(f"Analyze {character.get('name')}", key=f"analyze_{character_id}"):
                        with st.spinner("Analyzing character..."):
                            analysis = llm_client.analyze_character(character)
                            st.text_area("Character Analysis", analysis, height=300)
                
                with col3:
                    if st.button(f"Delete {character.get('name')}", key=f"delete_{character_id}"):
                        if script_aware_manager.delete_character(username, character_id):
                            st.success(f"Character '{character.get('name')}' deleted!")
                            st.rerun()
                        else:
                            st.error("Error deleting character.")
                
                # Character notes
                if 'notes' in character and character['notes']:
                    st.subheader("📝 Notes")
                    for note in character['notes']:
                        st.info(f"{note['text']} - {note['timestamp'][:10]}")
                
                st.divider()
    else:
        st.info("No characters found. Create your first character to get started!")

# Locations Management
elif selected == "Locations":
    st.markdown('<h1 class="section-header">📍 Location Management</h1>', unsafe_allow_html=True)
    
    # Location creation
    with st.expander("➕ Add New Location", expanded=False):
        with st.form("add_location"):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Location Name")
                description = st.text_area("Location Description")
                objects = st.text_area("Objects (comma-separated)")
            
            with col2:
                lighting = st.text_input("Lighting")
                date_time = st.text_input("Date/Time")
                location_type = st.selectbox("Location Type", ["Indoor", "Outdoor", "Public", "Private", "Other"])
            
            if st.form_submit_button("Add Location"):
                if name:
                    location_data = {
                        'name': name,
                        'description': description,
                        'objects': [obj.strip() for obj in objects.split(',') if obj.strip()],
                        'lighting': lighting,
                        'date_time': date_time,
                        'type': location_type
                    }
                    
                    if script_aware_manager.add_location(username, location_data):
                        st.success(f"Location '{name}' added successfully!")
                        st.rerun()
                    else:
                        st.error("Location already exists or error occurred.")
                else:
                    st.error("Please enter a location name.")
    
    # Location list and management
    st.subheader("🗺️ Location List")
    
    # Search functionality
    location_search = st.text_input("🔍 Search locations...")
    
    if location_search:
        locations = script_aware_manager.search_locations(username, location_search)
    else:
        locations = script_aware_manager.get_locations(username)
    
    if locations:
        for location_id, location in locations.items():
            with st.container():
                st.markdown(f"""
                <div class="location-card">
                    <h3>{location.get('name', 'No name')}</h3>
                    <p><strong>Description:</strong> {location.get('description', 'No description')}</p>
                    <p><strong>Objects:</strong> {', '.join(location.get('objects', [])) if isinstance(location.get('objects', []), list) else location.get('objects', 'No objects')}</p>
                    <p><strong>Type:</strong> {location.get('type', 'No type')}</p>
                    <p><strong>Lighting:</strong> {location.get('lighting', 'No lighting info')}</p>
                    <p><strong>Time:</strong> {location.get('date_time', 'No time info')}</p>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button(f"Edit {location.get('name')}", key=f"edit_loc_{location_id}"):
                        st.session_state.editing_location = location_id
                
                with col2:
                    if st.button(f"View Scenes {location.get('name')}", key=f"view_scenes_{location_id}"):
                        scenes = script_aware_manager.search_scenes(username, location.get('name'))
                        if scenes:
                            st.subheader(f"Scenes in {location.get('name')}")
                            for scene in scenes:
                                st.write(f"Scene {scene.get('scene_number')}: {scene.get('title', 'No title')}")
                        else:
                            st.info(f"No scenes set in {location.get('name')}")
                
                with col3:
                    if st.button(f"Delete {location.get('name')}", key=f"delete_loc_{location_id}"):
                        if script_aware_manager.delete_location(username, location_id):
                            st.success(f"Location '{location.get('name')}' deleted!")
                            st.rerun()
                        else:
                            st.error("Error deleting location.")
                
                # Location notes
                if 'notes' in location and location['notes']:
                    st.subheader("📝 Notes")
                    for note in location['notes']:
                        st.info(f"{note['text']} - {note['timestamp'][:10]}")
                
                st.divider()
    else:
        st.info("No locations found. Create your first location to get started!")

# Scene Generator
elif selected == "Scene Generator":
    scene_generator.render_scene_generator()

# Scenes Management
elif selected == "Scenes":
    st.markdown('<h1 class="section-header">🎬 Scene Management</h1>', unsafe_allow_html=True)
    
    # Export options
    with st.expander("📄 Export to Word", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Export Single Scene")
            scenes = script_aware_manager.get_scene_sequence(username)
            if scenes:
                scene_options = [f"Scene {s.get('scene_number', 'N/A')}: {s.get('title', 'No title')}" for s in scenes]
                selected_scene_index = st.selectbox("Select scene to export:", range(len(scenes)), format_func=lambda x: scene_options[x])
                
                if st.button("Export Single Scene"):
                    try:
                        selected_scene = scenes[selected_scene_index]
                        filepath = word_exporter.export_single_scene(selected_scene)
                        
                        # Read the file for download
                        with open(filepath, 'rb') as f:
                            st.download_button(
                                label="📥 Download Scene",
                                data=f.read(),
                                file_name=os.path.basename(filepath),
                                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                            )
                        st.success(f"Scene exported successfully!")
                    except Exception as e:
                        st.error(f"Error exporting scene: {str(e)}")
            else:
                st.info("No scenes to export.")
        
        with col2:
            st.subheader("Export Full Script")
            if scenes:
                title = st.text_input("Script Title:", value="My Screenplay")
                author = st.text_input("Author:", value="Screenwriter")
                
                if st.button("Export Full Script"):
                    try:
                        characters = list(script_aware_manager.get_characters(username).values())
                        filepath = word_exporter.export_scenes_to_word(scenes, characters, title, author)
                        
                        # Read the file for download
                        with open(filepath, 'rb') as f:
                            st.download_button(
                                label="📥 Download Full Script",
                                data=f.read(),
                                file_name=os.path.basename(filepath),
                                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                            )
                        st.success(f"Full script exported successfully!")
                    except Exception as e:
                        st.error(f"Error exporting script: {str(e)}")
            else:
                st.info("No scenes to export.")
    
    # Scene creation
    with st.expander("➕ Add New Scene", expanded=False):
        with st.form("add_scene"):
            col1, col2 = st.columns(2)
            
            with col1:
                scene_number = st.number_input("Scene Number", min_value=1, value=1)
                title = st.text_input("Scene Title")
                location = st.text_input("Location")
                time_of_day = st.selectbox("Time of Day", ["Morning", "Afternoon", "Evening", "Night", "Custom"])
                tone_mood = st.multiselect("Tone/Mood", ["tense", "hopeful", "bleak", "warm", "suspenseful", "comedic", "dramatic", "romantic", "dark", "lighthearted"])
            
            with col2:
                characters = st.multiselect("Characters", script_aware_manager.get_character_names(username))
                action = st.text_area("Script Content (Action & Dialogue)")
                goal = st.text_area("Goal of the Scene")
            
            if st.form_submit_button("Add Scene"):
                scene_data = {
                    'scene_number': scene_number,
                    'title': title,
                    'location': location,
                    'time_of_day': time_of_day,
                    'tone_mood': tone_mood,
                    'characters': characters,
                    'action': action,
                    'goal': goal
                }
                
                if script_aware_manager.add_scene(username, scene_data):
                    st.success(f"Scene {scene_number} added successfully!")
                    st.rerun()
                else:
                    st.error("Scene already exists or error occurred.")
    
    # Scene list and management
    st.subheader("📋 Scene List")
    
    # Search functionality
    scene_search = st.text_input("🔍 Search scenes...")
    
    if scene_search:
        scenes = script_aware_manager.search_scenes(username, scene_search)
    else:
        scenes = script_aware_manager.get_scenes(username)
    
    if scenes:
        for scene_id, scene in scenes.items():
            with st.container():
                st.markdown(f"""
                <div class="scene-card">
                    <h3>Scene {scene.get('scene_number', 'N/A')}: {scene.get('title', 'No title')}</h3>
                    <p><strong>Location:</strong> {scene.get('location', 'No location')}</p>
                    <p><strong>Time:</strong> {scene.get('time_of_day', 'No time')}</p>
                    <p><strong>Tone/Mood:</strong> {', '.join(scene.get('tone_mood', [])) if isinstance(scene.get('tone_mood', []), list) else scene.get('tone_mood', 'None')}</p>
                    <p><strong>Characters:</strong> {', '.join(scene.get('characters', [])) if isinstance(scene.get('characters', []), list) else scene.get('characters', 'None')}</p>
                    <p><strong>Goal:</strong> {scene.get('goal', 'No goal')}</p>
                    <p><strong>Script Content:</strong> {scene.get('action', 'No content')}</p>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    if st.button(f"Edit Scene {scene.get('scene_number')}", key=f"edit_scene_{scene_id}"):
                        st.session_state.editing_scene = scene_id
                
                with col2:
                    if st.button(f"Analyze Scene {scene.get('scene_number')}", key=f"analyze_scene_{scene_id}"):
                        with st.spinner("Analyzing scene..."):
                            analysis = llm_client.analyze_scene(scene)
                            st.text_area("Scene Analysis", analysis, height=300)
                
                with col3:
                    if st.button(f"Export Scene {scene.get('scene_number')}", key=f"export_scene_{scene_id}"):
                        try:
                            filepath = word_exporter.export_single_scene(scene)
                            with open(filepath, 'rb') as f:
                                st.download_button(
                                    label="📥 Download",
                                    data=f.read(),
                                    file_name=os.path.basename(filepath),
                                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                                    key=f"download_scene_{scene_id}"
                                )
                            st.success("Scene exported!")
                        except Exception as e:
                            st.error(f"Error exporting: {str(e)}")
                
                with col4:
                    if st.button(f"Delete Scene {scene.get('scene_number')}", key=f"delete_scene_{scene_id}"):
                        if script_aware_manager.delete_scene(username, scene_id):
                            st.success(f"Scene {scene.get('scene_number')} deleted!")
                            st.rerun()
                        else:
                            st.error("Error deleting scene.")
                
                st.divider()
    else:
        st.info("No scenes found. Create your first scene to get started!")

# Text Tools
elif selected == "Text Tools":
    st.markdown('<h1 class="section-header">✏️ Text Modification Tools</h1>', unsafe_allow_html=True)
    
    # Text input
    text_input = st.text_area("Enter your text here:", height=200, placeholder="Paste your scene, dialogue, or any text you want to modify...")
    
    # Show modification options regardless of text input
    st.subheader("🛠️ Modification Options")
    
    if not text_input:
        st.info("Enter some text above to start modifying it!")
        # Add a sample text for testing
        if st.button("Load Sample Text"):
            st.session_state.sample_text = "Sarah sits at her desk, surrounded by newspaper clippings. She's been working late, and the office is nearly empty. Her phone rings with an anonymous tip about government corruption."
            st.rerun()
        
        if 'sample_text' in st.session_state:
            text_input = st.session_state.sample_text
            st.text_area("Sample Text:", text_input, height=100, disabled=True)
    
    if text_input:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Tone & Style")
            
            # Tone modification
            tone_options = ["dramatic", "comedic", "suspenseful", "romantic", "dark", "lighthearted", "formal", "casual"]
            selected_tone = st.selectbox("Select tone to change to:", tone_options)
            
            if st.button("🎭 Change Tone"):
                with st.spinner("Modifying tone..."):
                    modified_text = text_modifier.modify_tone(text_input, selected_tone)
                    st.text_area("Modified Text:", modified_text, height=200)
            
            # Visual elements
            if st.button("🎬 Add Visual Elements"):
                with st.spinner("Adding visual elements..."):
                    enhanced_text = text_modifier.add_visual_elements(text_input)
                    st.text_area("Enhanced Text:", enhanced_text, height=200)
            
            # Dialogue improvement
            character_name = st.text_input("Character name (optional):", key="dialogue_char")
            if st.button("💬 Improve Dialogue"):
                with st.spinner("Improving dialogue..."):
                    improved_dialogue = text_modifier.improve_dialogue(text_input, character_name)
                    st.text_area("Improved Dialogue:", improved_dialogue, height=200)
        
        with col2:
            st.subheader("Structure & Content")
            
            # Scene expansion
            expansion_types = ["detail", "dialogue", "action", "description", "emotion"]
            expansion_type = st.selectbox("What to expand:", expansion_types)
            
            if st.button("📈 Expand Scene"):
                with st.spinner("Expanding scene..."):
                    expanded_text = text_modifier.expand_scene(text_input, expansion_type)
                    st.text_area("Expanded Text:", expanded_text, height=200)
            
            # Scene condensation
            if st.button("📉 Condense Scene"):
                with st.spinner("Condensing scene..."):
                    condensed_text = text_modifier.condense_scene(text_input)
                    st.text_area("Condensed Text:", condensed_text, height=200)
            
            # Perspective change
            perspectives = ["first person", "third person limited", "third person omniscient", "second person"]
            new_perspective = st.selectbox("Select perspective:", perspectives)
            
            if st.button("🔄 Change Perspective"):
                with st.spinner("Changing perspective..."):
                    new_text = text_modifier.change_perspective(text_input, new_perspective)
                    st.text_area("New Perspective:", new_text, height=200)
        
        # Advanced tools
        st.subheader("🔧 Advanced Tools")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Add conflict
            conflict_types = ["internal", "external", "interpersonal", "environmental", "societal"]
            conflict_type = st.selectbox("Conflict type:", conflict_types)
            
            if st.button("⚔️ Add Conflict"):
                with st.spinner("Adding conflict..."):
                    conflict_text = text_modifier.add_conflict(text_input, conflict_type)
                    st.text_area("Text with Conflict:", conflict_text, height=200)
        
        with col2:
            # Character development
            character_name_dev = st.text_input("Character to develop:", key="dev_char")
            if st.button("🎭 Enhance Character Development"):
                with st.spinner("Enhancing character development..."):
                    enhanced_text = text_modifier.enhance_character_development(text_input, character_name_dev)
                    st.text_area("Enhanced Text:", enhanced_text, height=200)

# Script Analysis
elif selected == "Script Analysis":
    st.markdown('<h1 class="section-header">📊 Script Analysis</h1>', unsafe_allow_html=True)
    
    # Overall statistics
    st.subheader("📈 Overall Statistics")
    
    stats = script_aware_manager.get_scene_statistics(username)
    characters = script_aware_manager.get_characters(username)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Character analysis
        st.subheader("👥 Character Analysis")
        
        if characters:
            char_data = []
            for char in characters.values():
                char_data.append({
                    'Name': char.get('name', 'Unknown'),
                    'Description Length': len(char.get('description', '')),
                    'Personality': len(char.get('personality', ''))
                })
            
            df_char = pd.DataFrame(char_data)
            st.dataframe(df_char)
        else:
            st.info("No characters to analyze.")
    
    with col2:
        # Location analysis
        st.subheader("📍 Location Analysis")
        
        locations = script_aware_manager.get_all_locations(username)
        if locations:
            loc_data = []
            for loc in locations.values():
                loc_data.append({
                    'Name': loc.get('name', 'Unknown'),
                    'Description Length': len(loc.get('description', '')),
                    'Type': loc.get('type', 'Unknown')
                })
            
            df_loc = pd.DataFrame(loc_data)
            st.dataframe(df_loc)
        else:
            st.info("No locations to analyze.")
    
    # Scene analysis
    st.subheader("🎬 Scene Analysis")
    
    scenes = script_aware_manager.get_scene_sequence(username)
    if scenes:
        scene_data = []
        for scene in scenes:
            characters_count = len(scene.get('characters', [])) if isinstance(scene.get('characters', []), list) else 0
            scene_data.append({
                'Scene': scene.get('scene_number', 0),
                'Title': scene.get('title', 'No title'),
                'Location': scene.get('location', 'Unknown'),
                'Characters': characters_count,
                'Content Length': len(scene.get('action', '')),
                'Time': scene.get('time_of_day', 'Unknown')
            })
        
        df_scene = pd.DataFrame(scene_data)
        st.dataframe(df_scene)
        
        # Scene length analysis
        if not df_scene.empty:
            fig_length = px.line(df_scene, x='Scene', y='Content Length', title='Scene Length Progression')
            st.plotly_chart(fig_length, use_container_width=True)
    else:
        st.info("No scenes to analyze.")
    
    # AI-powered insights
    st.subheader("🤖 AI-Powered Insights")
    
    if st.button("Generate AI Analysis"):
        with st.spinner("Generating comprehensive analysis..."):
            # Analyze characters
            character_insights = []
            for char in list(characters.values())[:3]:  # Limit to first 3 characters
                insight = llm_client.analyze_character(char)
                character_insights.append(f"**{char.get('name', 'Unknown')}:** {insight[:200]}...")
            
            # Analyze scenes
            scene_insights = []
            for scene in scenes[:3]:  # Limit to first 3 scenes
                insight = llm_client.analyze_scene(scene)
                scene_insights.append(f"**Scene {scene.get('scene_number', 'N/A')}:** {insight[:200]}...")
            
            # Display insights
            st.subheader("Character Insights")
            for insight in character_insights:
                st.markdown(insight)
                st.divider()
            
            st.subheader("Scene Insights")
            for insight in scene_insights:
                st.markdown(insight)
                st.divider()

# Chat
elif selected == "Chat":
    st.markdown('<h1 class="section-header">💬 Chat with Yana</h1>', unsafe_allow_html=True)
    
    # Get current script ID for chat context
    script_id = st.session_state.get('current_script_id', None)
    
    # Display chat history
    chat_history = chat_manager.get_chat_history(username, script_id)
    
    if chat_history:
        st.subheader("📝 Chat History")
        for message in chat_history[-10:]:  # Show last 10 messages
            if message['role'] == 'user':
                st.markdown(f"""
                <div class="chat-message-user">
                    <strong>You:</strong> {message['content']}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chat-message-ai">
                    <strong>Yana:</strong> {message['content']}
                </div>
                """, unsafe_allow_html=True)
    
    # Chat input
    with st.form("chat_form"):
        user_input = st.text_area(
            "Ask Yana about your script, characters, scenes, or get writing advice:",
            height=100,
            placeholder="How can I improve my protagonist's character arc?",
            value=st.session_state.get('chat_suggestion', '')
        )
        
        col1, col2 = st.columns([3, 1])
        with col1:
            submitted = st.form_submit_button("Send Message", type="primary")
        with col2:
            if st.form_submit_button("Clear Chat History"):
                chat_manager.clear_chat_history(username, script_id)
                st.rerun()
    
    # Show context summary
    with st.expander("📋 Current Script Context"):
        context_summary = chat_manager.get_context_summary(
            character_manager=script_aware_manager, 
            scene_manager=script_aware_manager, 
            location_manager=script_aware_manager, 
            username=username
        )
        if context_summary:
            st.text(context_summary)
        else:
            st.info("No characters or scenes created yet. Start by adding some content!")
    
    # Chat suggestions
    with st.expander("💡 Chat Suggestions", expanded=False):
        suggestions = [
            "How can I improve the pacing of my script?",
            "What conflicts would work well for my protagonist?",
            "How can I make the dialogue more natural?",
            "What visual elements should I add to Scene 3?",
            "How can I develop my antagonist further?",
            "What plot holes should I watch out for?"
        ]
        
        # Use smaller buttons in a more compact layout
        for i, suggestion in enumerate(suggestions):
            if st.button(suggestion, key=f"suggestion_{i}", help="Click to use this suggestion"):
                # Set the suggestion in session state and rerun to populate the form
                st.session_state.chat_suggestion = suggestion
                st.rerun()
    
    # Check if there's a suggestion to populate
    if 'chat_suggestion' in st.session_state and st.session_state.chat_suggestion:
        # This will be handled in the form above
        pass
    
    # Clear the suggestion after it's been used
    if 'chat_suggestion' in st.session_state:
        del st.session_state.chat_suggestion
    
    # Process chat input
    if submitted and user_input.strip():
        # Add user message to chat history
        chat_manager.add_message(username, 'user', user_input, script_id)
        
        # Show user message immediately
        st.markdown(f"""
        <div class="chat-message-user">
            <strong>You:</strong> {user_input}
        </div>
        """, unsafe_allow_html=True)
        
        # Get AI response with context
        with st.spinner("Yana is thinking..."):
            context = chat_manager.get_full_context_for_ai(
                character_manager=script_aware_manager,
                scene_manager=script_aware_manager,
                location_manager=script_aware_manager,
                user_message=user_input,
                username=username,
                script_id=script_id
            )
            
            ai_response = llm_client.chat_with_context(user_input, context)
            
            # Add AI response to chat history
            chat_manager.add_message(username, 'assistant', ai_response, script_id)
            
            # Show AI response
            st.markdown(f"""
            <div class="chat-message-ai">
                <strong>Yana:</strong> {ai_response}
            </div>
            """, unsafe_allow_html=True)
            
            # Rerun to update chat history display
            st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>🎬 YanaChat AI Script Assistant | Built with Streamlit and OpenAI</p>
</div>
""", unsafe_allow_html=True) 