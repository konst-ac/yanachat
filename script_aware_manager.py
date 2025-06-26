import streamlit as st
from typing import Dict, List, Optional
from user_manager import UserManager

class ScriptAwareManager:
    """Wrapper to make managers work with script-specific data"""
    
    def __init__(self, user_manager: UserManager):
        self.user_manager = user_manager
    
    def get_current_script_data(self, username: str) -> Optional[Dict]:
        """Get current script data for the user"""
        if 'current_script_id' not in st.session_state:
            return None
        
        script_id = st.session_state.current_script_id
        return self.user_manager.get_script(username, script_id)
    
    def update_script_data(self, username: str, data_type: str, data: Dict) -> bool:
        """Update script data (characters, scenes, locations)"""
        script = self.get_current_script_data(username)
        if not script:
            return False
        
        script[data_type] = data
        return self.user_manager.update_script(username, script['id'], script)
    
    def get_script_data(self, username: str, data_type: str) -> Dict:
        """Get script data (characters, scenes, locations)"""
        script = self.get_current_script_data(username)
        if not script:
            return {}
        return script.get(data_type, {})
    
    def add_character(self, username: str, character_data: Dict) -> bool:
        """Add character to current script"""
        characters = self.get_script_data(username, 'characters')
        character_id = str(len(characters) + 1)
        characters[character_id] = character_data
        return self.update_script_data(username, 'characters', characters)
    
    def get_characters(self, username: str) -> Dict:
        """Get all characters for current script"""
        return self.get_script_data(username, 'characters')
    
    def update_character(self, username: str, character_id: str, character_data: Dict) -> bool:
        """Update character in current script"""
        characters = self.get_script_data(username, 'characters')
        if character_id in characters:
            characters[character_id] = character_data
            return self.update_script_data(username, 'characters', characters)
        return False
    
    def delete_character(self, username: str, character_id: str) -> bool:
        """Delete character from current script"""
        characters = self.get_script_data(username, 'characters')
        if character_id in characters:
            del characters[character_id]
            return self.update_script_data(username, 'characters', characters)
        return False
    
    def add_scene(self, username: str, scene_data: Dict) -> bool:
        """Add scene to current script"""
        scenes = self.get_script_data(username, 'scenes')
        scene_id = str(len(scenes) + 1)
        scenes[scene_id] = scene_data
        return self.update_script_data(username, 'scenes', scenes)
    
    def get_scenes(self, username: str) -> Dict:
        """Get all scenes for current script"""
        return self.get_script_data(username, 'scenes')
    
    def update_scene(self, username: str, scene_id: str, scene_data: Dict) -> bool:
        """Update scene in current script"""
        scenes = self.get_script_data(username, 'scenes')
        if scene_id in scenes:
            scenes[scene_id] = scene_data
            return self.update_script_data(username, 'scenes', scenes)
        return False
    
    def delete_scene(self, username: str, scene_id: str) -> bool:
        """Delete scene from current script"""
        scenes = self.get_script_data(username, 'scenes')
        if scene_id in scenes:
            del scenes[scene_id]
            return self.update_script_data(username, 'scenes', scenes)
        return False
    
    def add_location(self, username: str, location_data: Dict) -> bool:
        """Add location to current script"""
        locations = self.get_script_data(username, 'locations')
        location_id = str(len(locations) + 1)
        locations[location_id] = location_data
        return self.update_script_data(username, 'locations', locations)
    
    def get_locations(self, username: str) -> Dict:
        """Get all locations for current script"""
        return self.get_script_data(username, 'locations')
    
    def update_location(self, username: str, location_id: str, location_data: Dict) -> bool:
        """Update location in current script"""
        locations = self.get_script_data(username, 'locations')
        if location_id in locations:
            locations[location_id] = location_data
            return self.update_script_data(username, 'locations', locations)
        return False
    
    def delete_location(self, username: str, location_id: str) -> bool:
        """Delete location from current script"""
        locations = self.get_script_data(username, 'locations')
        if location_id in locations:
            del locations[location_id]
            return self.update_script_data(username, 'locations', locations)
        return False 