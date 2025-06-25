import streamlit as st
from typing import Dict, List, Optional
from datetime import datetime

class SceneGenerator:
    def __init__(self, character_manager, scene_manager, location_manager, llm_client):
        self.character_manager = character_manager
        self.scene_manager = scene_manager
        self.location_manager = location_manager
        self.llm_client = llm_client
    
    def render_scene_generator(self):
        """Render the main scene generator interface"""
        st.markdown('<h1 class="section-header">🎬 Scene Generator</h1>', unsafe_allow_html=True)
        
        # Initialize session state for scene data
        if 'current_scene' not in st.session_state:
            st.session_state.current_scene = {
                'title': '',
                'location': '',
                'time_of_day': 'Day',
                'tone_mood': [],
                'characters': [],
                'action': '',
                'beats': [],
                'goal': '',
                'conflict_stakes': '',
                'links_to_scenes': []
            }
        
        # Main layout with columns
        col1, col2 = st.columns([2, 1])
        
        with col1:
            self.render_scene_overview_panel()
            self.render_script_editor()
        
        with col2:
            self.render_prompt_assistant_sidebar()
            self.render_storyboard_panel()
            self.render_scene_notes_panel()
        
        # Action buttons at the bottom
        self.render_action_buttons()
    
    def render_scene_overview_panel(self):
        """Render the Scene Overview Panel"""
        st.markdown('<h3 class="section-header">📋 Scene Overview</h3>', unsafe_allow_html=True)
        
        with st.container():
            # Title
            st.session_state.current_scene['title'] = st.text_input(
                "Scene Title",
                value=st.session_state.current_scene['title'],
                placeholder="e.g., Scene 3 – Morning at the Lab"
            )
            
            # Location Selector
            locations = self.location_manager.get_location_names()
            if locations:
                selected_location = st.selectbox(
                    "Location",
                    options=[''] + locations,
                    index=0 if not st.session_state.current_scene['location'] else 
                          locations.index(st.session_state.current_scene['location']) + 1
                )
                st.session_state.current_scene['location'] = selected_location
            else:
                st.session_state.current_scene['location'] = st.text_input(
                    "Location",
                    value=st.session_state.current_scene['location'],
                    placeholder="Enter location name"
                )
            
            # Time of Day
            time_options = ['Morning', 'Afternoon', 'Evening', 'Night', 'Custom']
            selected_time = st.selectbox(
                "Time of Day",
                options=time_options,
                index=time_options.index(st.session_state.current_scene['time_of_day']) 
                if st.session_state.current_scene['time_of_day'] in time_options else 0
            )
            st.session_state.current_scene['time_of_day'] = selected_time
            
            # Tone / Mood
            tone_options = ['tense', 'hopeful', 'bleak', 'warm', 'suspenseful', 'comedic', 'dramatic', 'romantic', 'dark', 'lighthearted']
            selected_tones = st.multiselect(
                "Tone / Mood",
                options=tone_options,
                default=st.session_state.current_scene['tone_mood']
            )
            st.session_state.current_scene['tone_mood'] = selected_tones
            
            # Characters Involved
            characters = self.character_manager.get_character_names()
            if characters:
                selected_characters = st.multiselect(
                    "Characters Involved",
                    options=characters,
                    default=st.session_state.current_scene['characters']
                )
                st.session_state.current_scene['characters'] = selected_characters
            else:
                st.info("No characters created yet. Create characters first!")
    
    def render_script_editor(self):
        """Render the Script Editor"""
        st.markdown('<h3 class="section-header">✍️ Script Editor</h3>', unsafe_allow_html=True)
        
        # Combined Text Box for Action and Dialogue
        st.session_state.current_scene['action'] = st.text_area(
            "Script Content (Action & Dialogue)",
            value=st.session_state.current_scene['action'],
            height=500,
            placeholder="Write your scene here, including action, dialogue, character movements, and visual elements. You can mix action and dialogue naturally in the flow of your scene..."
        )
    
    def render_prompt_assistant_sidebar(self):
        """Render the Prompt Assistant Sidebar"""
        st.markdown('<h3 class="section-header">🤖 Prompt Assistant</h3>', unsafe_allow_html=True)
        
        with st.expander("AI Writing Assistant", expanded=True):
            if st.button("📝 Summarize this scene"):
                self.summarize_scene()
            
            if st.button("😊 Make it more emotional"):
                self.modify_tone("emotional")
            
            if st.button("😂 Make it more comedic"):
                self.modify_tone("comedic")
            
            if st.button("⚡ Make it more fast-paced"):
                self.modify_tone("fast-paced")
            
            if st.button("🔍 Check for consistency"):
                self.check_consistency()
            
            if st.button("💡 Suggest next action"):
                self.suggest_next_action()
    
    def render_storyboard_panel(self):
        """Render the Storyboard/Image Panel"""
        st.markdown('<h3 class="section-header">🎨 Storyboard</h3>', unsafe_allow_html=True)
        
        with st.container():
            st.button("🎨 Generate Sketch", disabled=True, help="Image generation feature coming soon!")
            
            # Placeholder for storyboard frames
            st.info("Storyboard frames will appear here once generated.")
    
    def render_scene_notes_panel(self):
        """Render the Scene Notes / Metadata Panel"""
        st.markdown('<h3 class="section-header">📝 Scene Notes</h3>', unsafe_allow_html=True)
        
        with st.container():
            # Beats
            st.subheader("Beats")
            new_beat = st.text_input("Add beat:", key="new_beat")
            if st.button("Add Beat") and new_beat:
                st.session_state.current_scene['beats'].append(new_beat)
                st.rerun()
            
            # Display existing beats
            for i, beat in enumerate(st.session_state.current_scene['beats']):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"• {beat}")
                with col2:
                    if st.button("Delete", key=f"delete_beat_{i}"):
                        st.session_state.current_scene['beats'].pop(i)
                        st.rerun()
            
            # Goal of the Scene
            st.subheader("Goal of the Scene")
            st.session_state.current_scene['goal'] = st.text_area(
                "What is the goal of this scene?",
                value=st.session_state.current_scene['goal'],
                height=80,
                placeholder="e.g., Show character's exhaustion"
            )
            
            # Conflict / Stakes
            st.subheader("Conflict / Stakes")
            st.session_state.current_scene['conflict_stakes'] = st.text_area(
                "What are the conflicts and stakes?",
                value=st.session_state.current_scene['conflict_stakes'],
                height=80,
                placeholder="e.g., Character must choose between duty and family"
            )
            
            # Links to Other Scenes
            st.subheader("Links to Other Scenes")
            scenes = self.scene_manager.get_all_scenes()
            if scenes:
                scene_options = [f"Scene {s.get('scene_number', 'N/A')}: {s.get('title', 'No title')}" 
                               for s in scenes.values()]
                selected_links = st.multiselect(
                    "Connected Scenes",
                    options=scene_options,
                    default=st.session_state.current_scene['links_to_scenes']
                )
                st.session_state.current_scene['links_to_scenes'] = selected_links
            else:
                st.info("No other scenes to link to yet.")
    
    def render_action_buttons(self):
        """Render action buttons at the bottom"""
        st.markdown("---")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("💾 Save Scene", type="primary"):
                self.save_scene()
        
        with col2:
            if st.button("🔄 Clear Form"):
                st.session_state.current_scene = {
                    'title': '',
                    'location': '',
                    'time_of_day': 'Day',
                    'tone_mood': [],
                    'characters': [],
                    'action': '',
                    'beats': [],
                    'goal': '',
                    'conflict_stakes': '',
                    'links_to_scenes': []
                }
                st.rerun()
        
        with col3:
            if st.button("📋 Load Template"):
                self.load_template()
        
        with col4:
            if st.button("🎯 Auto-Generate"):
                self.auto_generate_scene()
    
    def summarize_scene(self):
        """Summarize the current scene"""
        if st.session_state.current_scene['action']:
            scene_text = st.session_state.current_scene['action']
            summary = self.llm_client.generate_response(
                f"Please provide a brief summary of this scene:\n\n{scene_text}"
            )
            st.info(f"**Scene Summary:**\n{summary}")
    
    def modify_tone(self, tone: str):
        """Modify the scene tone"""
        if st.session_state.current_scene['action']:
            scene_text = st.session_state.current_scene['action']
            modified = self.llm_client.modify_text_tone(scene_text, tone)
            st.info(f"**Modified Scene ({tone}):**\n{modified}")
    
    def check_consistency(self):
        """Check scene for consistency"""
        if st.session_state.current_scene['action']:
            scene_text = st.session_state.current_scene['action']
            consistency_check = self.llm_client.generate_response(
                f"Please check this scene for consistency issues:\n\n{scene_text}"
            )
            st.info(f"**Consistency Check:**\n{consistency_check}")
    
    def suggest_next_action(self):
        """Suggest next action for the scene"""
        if st.session_state.current_scene['action']:
            scene_text = st.session_state.current_scene['action']
            suggestion = self.llm_client.generate_response(
                f"Based on this scene, suggest what could happen next:\n\n{scene_text}"
            )
            st.info(f"**Next Action Suggestion:**\n{suggestion}")
    
    def save_scene(self):
        """Save the current scene"""
        if not st.session_state.current_scene['title']:
            st.error("Please provide a scene title!")
            return
        
        # Get next scene number
        existing_scenes = self.scene_manager.get_all_scenes()
        next_scene_number = len(existing_scenes) + 1
        
        scene_data = st.session_state.current_scene.copy()
        scene_data['scene_number'] = next_scene_number
        
        if self.scene_manager.add_scene(scene_data):
            st.success(f"Scene '{scene_data['title']}' saved successfully!")
            # Clear the form
            st.session_state.current_scene = {
                'title': '',
                'location': '',
                'time_of_day': 'Day',
                'tone_mood': [],
                'characters': [],
                'action': '',
                'beats': [],
                'goal': '',
                'conflict_stakes': '',
                'links_to_scenes': []
            }
            st.rerun()
        else:
            st.error("Error saving scene. Scene might already exist.")
    
    def load_template(self):
        """Load a scene template"""
        templates = {
            "Opening Scene": {
                'title': 'Opening Scene',
                'time_of_day': 'Day',
                'tone_mood': ['establishing'],
                'goal': 'Introduce the world and main character',
                'conflict_stakes': 'Establish the central conflict'
            },
            "Conflict Scene": {
                'title': 'Conflict Scene',
                'time_of_day': 'Day',
                'tone_mood': ['tense'],
                'goal': 'Escalate the conflict',
                'conflict_stakes': 'Raise the stakes for the protagonist'
            },
            "Resolution Scene": {
                'title': 'Resolution Scene',
                'time_of_day': 'Day',
                'tone_mood': ['hopeful'],
                'goal': 'Resolve the main conflict',
                'conflict_stakes': 'Final confrontation and resolution'
            }
        }
        
        template_name = st.selectbox("Select Template", list(templates.keys()))
        if st.button("Load Template"):
            template = templates[template_name]
            st.session_state.current_scene.update(template)
            st.rerun()
    
    def auto_generate_scene(self):
        """Auto-generate a scene based on current data"""
        if not st.session_state.current_scene['title']:
            st.error("Please provide a scene title first!")
            return
        
        prompt = f"""
        Generate a scene with the following details:
        Title: {st.session_state.current_scene['title']}
        Location: {st.session_state.current_scene['location']}
        Time: {st.session_state.current_scene['time_of_day']}
        Tone: {', '.join(st.session_state.current_scene['tone_mood'])}
        Characters: {', '.join(st.session_state.current_scene['characters'])}
        Goal: {st.session_state.current_scene['goal']}
        Conflict: {st.session_state.current_scene['conflict_stakes']}
        
        Please generate a complete scene with action and dialogue mixed naturally.
        """
        
        generated_scene = self.llm_client.generate_response(prompt)
        
        # Update the scene with generated content
        st.session_state.current_scene['action'] = generated_scene
        
        st.success("Scene auto-generated! Review and edit as needed.")
        st.rerun() 