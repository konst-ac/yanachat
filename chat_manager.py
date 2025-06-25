import json
import os
from typing import Dict, List, Optional
from datetime import datetime
from config import Config

class ChatManager:
    def __init__(self):
        self.chat_file = os.path.join(Config.SCRIPT_FILE_PATH, "chat_history.json")
        self.chat_history = self.load_chat_history()
    
    def load_chat_history(self) -> List[Dict]:
        """Load chat history from JSON file"""
        if os.path.exists(self.chat_file):
            try:
                with open(self.chat_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading chat history: {e}")
                return []
        return []
    
    def save_chat_history(self):
        """Save chat history to JSON file"""
        try:
            with open(self.chat_file, 'w', encoding='utf-8') as f:
                json.dump(self.chat_history, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving chat history: {e}")
    
    def add_message(self, role: str, content: str, timestamp: str = None):
        """Add a message to chat history"""
        if timestamp is None:
            timestamp = datetime.now().isoformat()
        
        message = {
            'role': role,
            'content': content,
            'timestamp': timestamp
        }
        
        self.chat_history.append(message)
        self.save_chat_history()
    
    def get_chat_history(self) -> List[Dict]:
        """Get all chat history"""
        return self.chat_history
    
    def clear_chat_history(self):
        """Clear all chat history"""
        self.chat_history = []
        self.save_chat_history()
    
    def get_context_summary(self, character_manager, scene_manager, location_manager) -> str:
        """Generate a context summary from characters, scenes, and locations for AI memory"""
        context_parts = []
        
        # Add character information
        characters = character_manager.get_all_characters()
        if characters:
            context_parts.append("CHARACTERS:")
            for char_id, char in characters.items():
                char_info = f"- {char.get('name', 'Unknown')} (Age: {char.get('age', 'Unknown')}): {char.get('description', 'No description')}. Personality: {char.get('personality', 'No personality')}. Goals: {char.get('goals', 'No goals')}. Conflicts: {char.get('conflicts', 'No conflicts')}"
                context_parts.append(char_info)
        
        # Add location information
        locations = location_manager.get_all_locations()
        if locations:
            context_parts.append("\nLOCATIONS:")
            for loc_id, loc in locations.items():
                objects_str = ', '.join(loc.get('objects', []))
                loc_info = f"- {loc.get('name', 'Unknown')}: {loc.get('description', 'No description')}. Objects: {objects_str}. Lighting: {loc.get('lighting', 'No lighting info')}. Time: {loc.get('date_time', 'No time info')}"
                context_parts.append(loc_info)
        
        # Add scene information
        scenes = scene_manager.get_scene_sequence()
        if scenes:
            context_parts.append("\nSCENES:")
            for scene in scenes:
                characters_str = ', '.join(scene.get('characters', [])) if isinstance(scene.get('characters', []), list) else scene.get('characters', 'None')
                tone_str = ', '.join(scene.get('tone_mood', [])) if isinstance(scene.get('tone_mood', []), list) else scene.get('tone_mood', 'None')
                scene_info = f"- Scene {scene.get('scene_number', 'N/A')} ({scene.get('title', 'No title')}): Location: {scene.get('location', 'No location')}. Time: {scene.get('time_of_day', 'No time')}. Characters: {characters_str}. Tone: {tone_str}. Goal: {scene.get('goal', 'No goal')}. Content: {scene.get('action', 'No content')[:200]}..."
                context_parts.append(scene_info)
        
        # Add recent chat context
        if self.chat_history:
            context_parts.append("\nRECENT CONVERSATION:")
            recent_messages = self.chat_history[-6:]  # Last 6 messages
            for msg in recent_messages:
                role = "You" if msg['role'] == 'user' else "AI"
                context_parts.append(f"{role}: {msg['content'][:150]}...")
        
        return "\n".join(context_parts)
    
    def get_full_context_for_ai(self, character_manager, scene_manager, location_manager, user_message: str) -> str:
        """Get full context including characters, scenes, locations, and chat history for AI"""
        context = self.get_context_summary(character_manager, scene_manager, location_manager)
        
        full_context = f"""
You are an expert screenwriting assistant for a filmmaker. You have access to the following information about their script:

{context}

Current user message: {user_message}

Please respond as a helpful screenwriting assistant, using the context above to provide relevant, personalized advice about their script, characters, scenes, and locations.
"""
        return full_context 