import json
import os
from typing import Dict, List, Optional
from datetime import datetime
from config import Config

class ChatManager:
    def __init__(self):
        self.chat_file = os.path.join(Config.SCRIPT_FILE_PATH, "chat_history.json")
        self.chat_history = self.load_chat_history()
    
    def load_chat_history(self) -> Dict:
        """Load chat history from JSON file"""
        if os.path.exists(self.chat_file):
            try:
                with open(self.chat_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Ensure we always return a dictionary
                    if isinstance(data, dict):
                        return data
                    else:
                        print(f"Warning: chat_history.json contains {type(data)}, expected dict. Resetting to empty dict.")
                        return {}
            except Exception as e:
                print(f"Error loading chat history: {e}")
                return {}
        return {}
    
    def save_chat_history(self):
        """Save chat history to JSON file"""
        try:
            with open(self.chat_file, 'w', encoding='utf-8') as f:
                json.dump(self.chat_history, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving chat history: {e}")
    
    def get_user_chat_key(self, username: str, script_id: str = None) -> str:
        """Get the key for user's chat history"""
        if script_id:
            return f"{username}_{script_id}"
        return username
    
    def add_message(self, username: str, role: str, content: str, script_id: str = None, timestamp: str = None):
        """Add a message to user's chat history"""
        if timestamp is None:
            timestamp = datetime.now().isoformat()
        
        chat_key = self.get_user_chat_key(username, script_id)
        
        if chat_key not in self.chat_history:
            self.chat_history[chat_key] = []
        
        message = {
            'role': role,
            'content': content,
            'timestamp': timestamp
        }
        
        self.chat_history[chat_key].append(message)
        self.save_chat_history()
    
    def get_chat_history(self, username: str, script_id: str = None) -> List[Dict]:
        """Get user's chat history"""
        chat_key = self.get_user_chat_key(username, script_id)
        return self.chat_history.get(chat_key, [])
    
    def clear_chat_history(self, username: str, script_id: str = None):
        """Clear user's chat history"""
        chat_key = self.get_user_chat_key(username, script_id)
        if chat_key in self.chat_history:
            self.chat_history[chat_key] = []
            self.save_chat_history()
    
    def get_context_summary(self, character_manager, scene_manager, location_manager, username: str = None) -> str:
        """Get a summary of the current script context"""
        if not username:
            return "No user context available."
        
        characters = character_manager.get_characters(username)
        scenes = scene_manager.get_scene_sequence(username)
        locations = location_manager.get_locations(username)
        
        summary = []
        
        if characters:
            char_names = [char.get('name', 'Unknown') for char in characters.values()]
            summary.append(f"Characters: {', '.join(char_names)}")
        
        if scenes:
            scene_titles = [f"Scene {scene.get('scene_number', 'N/A')}: {scene.get('title', 'No title')}" for scene in scenes]
            summary.append(f"Scenes: {', '.join(scene_titles)}")
        
        if locations:
            loc_names = [loc.get('name', 'Unknown') for loc in locations.values()]
            summary.append(f"Locations: {', '.join(loc_names)}")
        
        return " | ".join(summary) if summary else "No content created yet."
    
    def get_full_context_for_ai(self, character_manager, scene_manager, location_manager, user_message: str, username: str = None, script_id: str = None) -> str:
        """Get full context for AI processing"""
        if not username:
            return "No user context available."
        
        characters = character_manager.get_characters(username)
        scenes = scene_manager.get_scene_sequence(username)
        locations = location_manager.get_locations(username)
        
        context_parts = []
        
        # Character context
        if characters:
            char_context = "CHARACTERS:\n"
            for char in characters.values():
                char_context += f"- {char.get('name', 'Unknown')}: {char.get('description', 'No description')}\n"
            context_parts.append(char_context)
        
        # Scene context
        if scenes:
            scene_context = "SCENES:\n"
            for scene in scenes:
                scene_context += f"- Scene {scene.get('scene_number', 'N/A')}: {scene.get('title', 'No title')} at {scene.get('location', 'Unknown location')}\n"
            context_parts.append(scene_context)
        
        # Location context
        if locations:
            loc_context = "LOCATIONS:\n"
            for loc in locations.values():
                loc_context += f"- {loc.get('name', 'Unknown')}: {loc.get('description', 'No description')}\n"
            context_parts.append(loc_context)
        
        # Chat history context
        chat_history = self.get_chat_history(username, script_id)
        if chat_history:
            history_context = "RECENT CHAT HISTORY:\n"
            for message in chat_history[-5:]:  # Last 5 messages
                role = "User" if message['role'] == 'user' else "Assistant"
                history_context += f"- {role}: {message['content'][:100]}...\n"
            context_parts.append(history_context)
        
        return "\n\n".join(context_parts) if context_parts else "No context available." 