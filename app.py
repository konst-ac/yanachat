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
        options=["Script Manager", "Dashboard", "Characters", "Locations", "Scene Generator", "Scenes", "Script Analysis", "Chat"],
        icons=["folder", "house", "person", "geo-alt", "film", "list", "graph-up", "chat"],
        menu_icon="cast",
        default_index=0,
    )

# Custom CSS for modern styling
st.markdown('''
<style>
body, .stApp {
    background: #f8f5f0 !important;
}

/* Card/Panel outlines and padding, with slightly darker background */
.square-block, .st-expander, .metric-card, .details-section, .stForm, .stDataFrame, .stTable, .stAlert, .stInfo, .stSuccess, .stError {
    background: #f3ede6 !important;
    border-radius: 14px !important;
    box-shadow: 0 2px 12px rgba(0,0,0,0.08) !important;
    border: 1px solid #e0d9ce !important;
    padding: 20px !important;
}
</style>
''', unsafe_allow_html=True)

# Add this function after the imports and before the main app logic
def render_square_blocks(items, item_type, on_click=None):
    if not items:
        return

    if isinstance(items, dict):
        items_list = list(items.items())
    else:
        items_list = items

    for i in range(0, len(items_list), 3):
        row_items = items_list[i:i+3]
        cols = st.columns(3)

        for j, (item_id, item) in enumerate(row_items):
            with cols[j]:
                if item_type == 'character':
                    title = item.get('name', 'Unknown')
                    subtitle = f"Age: {item.get('age', 'Unknown')}"
                    description = item.get('description', 'No description')[:80] + "..." if len(item.get('description', '')) > 80 else item.get('description', 'No description')
                    icon = "👤"
                elif item_type == 'location':
                    title = item.get('name', 'Unknown')
                    subtitle = f"Type: {item.get('type', 'Unknown')}"
                    description = item.get('description', 'No description')[:80] + "..." if len(item.get('description', '')) > 80 else item.get('description', 'No description')
                    icon = "📍"
                elif item_type == 'scene':
                    title = f"Scene {item.get('scene_number', 'N/A')}: {item.get('title', 'No title')}"
                    subtitle = f"Location: {item.get('location', 'Unknown')}"
                    description = item.get('action', 'No content')[:80] + "..." if len(item.get('action', '')) > 80 else item.get('action', 'No content')
                    icon = "🎬"

                block_class = f"square-block {item_type}-block"
                block_id = f"{item_type}_{item_id}"
                st.markdown(f'''
                <div class="{block_class}" id="{block_id}">
                    <div>
                        <h3>{icon} {title}</h3>
                        <p class="subtitle">{subtitle}</p>
                        <p class="description">{description}</p>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
                if st.button("View Details", key=f"block_{item_type}_{item_id}"):
                    if on_click:
                        on_click(item_id, item)
                    else:
                        st.session_state[f"selected_{item_type}"] = item_id
                        st.rerun()

# Script Manager
if selected == "Script Manager":
    st.markdown('<h1 class="section-header">📚 Script Manager</h1>', unsafe_allow_html=True)
    st.markdown('---')
    
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
    st.markdown('---')
    
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
            # Convert to dict format for render_square_blocks
            recent_scenes = {f"recent_{i}": scene for i, scene in enumerate(scenes[-3:])}
            render_square_blocks(recent_scenes, 'scene')
        else:
            st.info("No scenes created yet. Start by adding your first scene!")
    
    with col2:
        st.subheader("👥 Recent Characters")
        characters = script_aware_manager.get_characters(username)
        if characters:
            # Get last 3 characters
            recent_chars = dict(list(characters.items())[-3:])
            render_square_blocks(recent_chars, 'character')
        else:
            st.info("No characters created yet. Start by adding your first character!")

# Characters Management
elif selected == "Characters":
    st.markdown('<h1 class="section-header">👥 Character Management</h1>', unsafe_allow_html=True)
    st.markdown('---')
    
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
        def on_character_click(item_id, item):
            st.session_state["selected_character"] = item_id
            st.rerun()
        
        render_square_blocks(characters, 'character', on_character_click)
        
        # Show selected character details
        if st.session_state.get("selected_character"):
            selected_char_id = st.session_state["selected_character"]
            if selected_char_id in characters:
                selected_char = characters[selected_char_id]
                st.markdown("---")
                st.markdown(f"""
                <div id="details_character_{selected_char_id}" class="details-section">
                    <h3>👤 {selected_char.get('name', 'Unknown')} - Details</h3>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.write(f"**Age:** {selected_char.get('age', 'Unknown')}")
                    st.write(f"**Description:** {selected_char.get('description', 'No description')}")
                    st.write(f"**Personality:** {selected_char.get('personality', 'No personality traits')}")
                    st.write(f"**Goals:** {selected_char.get('goals', 'No goals')}")
                    st.write(f"**Conflicts:** {selected_char.get('conflicts', 'No conflicts')}")
                
                with col2:
                    if st.button("✏️ Edit Character", key="edit_selected_char"):
                        st.session_state.editing_character = selected_char_id
                    
                    if st.button("🔍 Analyze Character", key="analyze_selected_char"):
                        with st.spinner("Analyzing character..."):
                            analysis = llm_client.analyze_character(selected_char)
                            st.text_area("Character Analysis", analysis, height=300)
                    
                    if st.button("🗑️ Delete Character", key="delete_selected_char"):
                        if script_aware_manager.delete_character(username, selected_char_id):
                            st.success(f"Character '{selected_char.get('name')}' deleted!")
                            del st.session_state["selected_character"]
                            st.rerun()
                        else:
                            st.error("Error deleting character.")
                    
                    if st.button("❌ Close Details", key="close_char_details"):
                        del st.session_state["selected_character"]
                        st.rerun()
    else:
        st.info("No characters found. Create your first character to get started!")

# Locations Management
elif selected == "Locations":
    st.markdown('<h1 class="section-header">📍 Location Management</h1>', unsafe_allow_html=True)
    st.markdown('---')
    
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
        def on_location_click(item_id, item):
            st.session_state["selected_location"] = item_id
            st.rerun()
        
        render_square_blocks(locations, 'location', on_location_click)
        
        # Show selected location details
        if st.session_state.get("selected_location"):
            selected_loc_id = st.session_state["selected_location"]
            if selected_loc_id in locations:
                selected_loc = locations[selected_loc_id]
                st.markdown("---")
                st.markdown(f"""
                <div id="details_location_{selected_loc_id}" class="details-section">
                    <h3>📍 {selected_loc.get('name', 'Unknown')} - Details</h3>
                </div>
                """, unsafe_allow_html=True)
                
                if st.session_state.get('editing_location') == selected_loc_id:
                    st.info(f"[DEBUG] Edit mode active for location: {selected_loc_id}")
                    st.markdown('---')
                    st.markdown(f"<h3>Edit Location: {selected_loc.get('name', 'Unknown')}</h3>", unsafe_allow_html=True)
                    with st.form(f"edit_location_form_{selected_loc_id}"):
                        col1, col2 = st.columns(2)
                        with col1:
                            name = st.text_input("Location Name", value=selected_loc.get('name', ''))
                            description = st.text_area("Location Description", value=selected_loc.get('description', ''))
                            objects = st.text_area("Objects (comma-separated)", value=','.join(selected_loc.get('objects', [])) if isinstance(selected_loc.get('objects', []), list) else selected_loc.get('objects', ''))
                        with col2:
                            lighting = st.text_input("Lighting", value=selected_loc.get('lighting', ''))
                            date_time = st.text_input("Date/Time", value=selected_loc.get('date_time', ''))
                            location_type = st.selectbox("Location Type", ["Indoor", "Outdoor", "Public", "Private", "Other"], index=["Indoor", "Outdoor", "Public", "Private", "Other"].index(selected_loc.get('type', 'Other')) if selected_loc.get('type', 'Other') in ["Indoor", "Outdoor", "Public", "Private", "Other"] else 4)
                        save, cancel = st.columns(2)
                        with save:
                            if st.form_submit_button("Save Changes"):
                                updated_location = {
                                    'name': name,
                                    'description': description,
                                    'objects': [obj.strip() for obj in objects.split(',') if obj.strip()],
                                    'lighting': lighting,
                                    'date_time': date_time,
                                    'type': location_type,
                                    'id': selected_loc.get('id'),
                                    'created_at': selected_loc.get('created_at'),
                                    'updated_at': selected_loc.get('updated_at'),
                                }
                                if script_aware_manager.update_location(username, selected_loc_id, updated_location):
                                    st.success("Location updated!")
                                    st.session_state.editing_location = None
                                    st.rerun()
                                else:
                                    st.error("Error updating location.")
                                    st.session_state.editing_location = None
                                    st.rerun()
                        with cancel:
                            if st.form_submit_button("Cancel"):
                                st.session_state.editing_location = None
                                st.rerun()
                else:
                    if st.session_state.get('editing_location'):
                        st.info(f"[DEBUG] Not in edit mode for this location. (editing_location={st.session_state.get('editing_location')}, selected={selected_loc_id})")
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        st.write(f"**Description:** {selected_loc.get('description', 'No description')}")
                        st.write(f"**Objects:** {', '.join(selected_loc.get('objects', [])) if isinstance(selected_loc.get('objects', []), list) else selected_loc.get('objects', 'No objects')}")
                        st.write(f"**Type:** {selected_loc.get('type', 'No type')}")
                        st.write(f"**Lighting:** {selected_loc.get('lighting', 'No lighting info')}")
                        st.write(f"**Time:** {selected_loc.get('date_time', 'No time info')}")
                    with col2:
                        if st.button("✏️ Edit Location", key="edit_selected_loc"):
                            st.session_state.editing_location = selected_loc_id
                        if st.button("🎬 View Scenes", key="view_scenes_selected_loc"):
                            scenes = script_aware_manager.search_scenes(username, selected_loc.get('name'))
                            if scenes:
                                st.subheader(f"Scenes in {selected_loc.get('name')}")
                                for scene_id, scene in scenes.items():
                                    st.write(f"Scene {scene.get('scene_number')}: {scene.get('title', 'No title')}")
                            else:
                                st.info(f"No scenes set in {selected_loc.get('name')}")
                        if st.button("🗑️ Delete Location", key="delete_selected_loc"):
                            if script_aware_manager.delete_location(username, selected_loc_id):
                                st.success(f"Location '{selected_loc.get('name')}' deleted!")
                                del st.session_state["selected_location"]
                                st.rerun()
                            else:
                                st.error("Error deleting location.")
                        if st.button("❌ Close Details", key="close_loc_details"):
                            del st.session_state["selected_location"]
                            st.rerun()
    else:
        st.info("No locations found. Create your first location to get started!")

# Scene Generator
elif selected == "Scene Generator":
    scene_generator.render_scene_generator()

# Scenes Management
elif selected == "Scenes":
    st.markdown('<h1 class="section-header">🎬 Scene Management</h1>', unsafe_allow_html=True)
    st.markdown('---')
    
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
        def on_scene_click(item_id, item):
            st.session_state["selected_scene"] = item_id
            st.rerun()
        
        render_square_blocks(scenes, 'scene', on_scene_click)
        
        # Show selected scene details
        if st.session_state.get("selected_scene"):
            selected_scene_id = st.session_state["selected_scene"]
            if selected_scene_id in scenes:
                selected_scene = scenes[selected_scene_id]
                st.markdown("---")
                st.markdown(f"""
                <div id="details_scene_{selected_scene_id}" class="details-section">
                    <h3>🎬 Scene {selected_scene.get('scene_number', 'N/A')}: {selected_scene.get('title', 'No title')} - Details</h3>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.write(f"**Location:** {selected_scene.get('location', 'No location')}")
                    st.write(f"**Time:** {selected_scene.get('time_of_day', 'No time')}")
                    st.write(f"**Tone/Mood:** {', '.join(selected_scene.get('tone_mood', [])) if isinstance(selected_scene.get('tone_mood', []), list) else selected_scene.get('tone_mood', 'None')}")
                    st.write(f"**Characters:** {', '.join(selected_scene.get('characters', [])) if isinstance(selected_scene.get('characters', []), list) else selected_scene.get('characters', 'None')}")
                    st.write(f"**Goal:** {selected_scene.get('goal', 'No goal')}")
                    st.write(f"**Script Content:** {selected_scene.get('action', 'No content')}")
                
                with col2:
                    if st.button("✏️ Edit Scene", key="edit_selected_scene"):
                        st.session_state.editing_scene = selected_scene_id
                    
                    if st.button("🔍 Analyze Scene", key="analyze_selected_scene"):
                        with st.spinner("Analyzing scene..."):
                            analysis = llm_client.analyze_scene(selected_scene)
                            st.text_area("Scene Analysis", analysis, height=300)
                    
                    if st.button("📥 Export Scene", key="export_selected_scene"):
                        try:
                            filepath = word_exporter.export_single_scene(selected_scene)
                            with open(filepath, 'rb') as f:
                                st.download_button(
                                    label="📥 Download",
                                    data=f.read(),
                                    file_name=os.path.basename(filepath),
                                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                                    key=f"download_selected_scene"
                                )
                            st.success("Scene exported!")
                        except Exception as e:
                            st.error(f"Error exporting: {str(e)}")
                    
                    if st.button("🗑️ Delete Scene", key="delete_selected_scene"):
                        if script_aware_manager.delete_scene(username, selected_scene_id):
                            st.success(f"Scene {selected_scene.get('scene_number')} deleted!")
                            del st.session_state["selected_scene"]
                            st.rerun()
                        else:
                            st.error("Error deleting scene.")
                    
                    if st.button("❌ Close Details", key="close_scene_details"):
                        del st.session_state["selected_scene"]
                        st.rerun()
    else:
        st.info("No scenes found. Create your first scene to get started!")

# Script Analysis
elif selected == "Script Analysis":
    st.markdown('<h1 class="section-header">📊 Script Analysis</h1>', unsafe_allow_html=True)
    st.markdown('---')
    
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
        st.markdown('''
        <div style="max-height: 400px; overflow-y: auto; padding-right: 8px; border: 1px solid #eee; border-radius: 10px; background: #fafbfc; margin-bottom: 1rem;">
        ''', unsafe_allow_html=True)
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
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Chat input
    with st.form("chat_form"):
        # Use a key that changes to clear the input after submission
        chat_input_key = f"chat_input_{st.session_state.get('chat_counter', 0)}"
        user_input = st.text_area(
            "Ask Yana about your script, characters, scenes, or get writing advice:",
            height=100,
            placeholder="How can I improve my protagonist's character arc?",
            value=st.session_state.get('chat_suggestion', ''),
            key=chat_input_key
        )
        
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            submitted = st.form_submit_button("Send Message", type="primary")
        with col2:
            if st.form_submit_button("Clear Chat History"):
                chat_manager.clear_chat_history(username, script_id)
                st.rerun()
        with col3:
            if st.form_submit_button("📝 Text Tools"):
                st.session_state.show_text_tools = True
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
        
        # Increment chat counter to clear input on next render
        st.session_state.chat_counter = st.session_state.get('chat_counter', 0) + 1
        
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

# Text Tools Section (appears when triggered from chat)
if st.session_state.get('show_text_tools', False):
    st.markdown('<h1 class="section-header">✏️ Text Modification Tools</h1>', unsafe_allow_html=True)
    st.markdown('---')
    
    # Close button
    if st.button("❌ Close Text Tools"):
        st.session_state.show_text_tools = False
        st.rerun()
    
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

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>🎬 YanaChat AI Script Assistant | Built with Streamlit and OpenAI</p>
</div>
""", unsafe_allow_html=True) 