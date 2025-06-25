import json
import os
from typing import Dict, List, Optional
from datetime import datetime
from config import Config

class CharacterManager:
    def __init__(self):
        self.characters_file = os.path.join(Config.CHARACTER_FILE_PATH, "characters.json")
        self.characters = self.load_characters()
    
    def load_characters(self) -> Dict:
        """Load characters from JSON file"""
        if os.path.exists(self.characters_file):
            try:
                with open(self.characters_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading characters: {e}")
                return {}
        return {}
    
    def save_characters(self):
        """Save characters to JSON file"""
        try:
            with open(self.characters_file, 'w', encoding='utf-8') as f:
                json.dump(self.characters, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving characters: {e}")
    
    def add_character(self, character_data: Dict) -> bool:
        """Add a new character"""
        try:
            character_id = character_data.get('name', '').lower().replace(' ', '_')
            if character_id in self.characters:
                return False  # Character already exists
            
            character_data['id'] = character_id
            character_data['created_at'] = datetime.now().isoformat()
            character_data['updated_at'] = datetime.now().isoformat()
            
            self.characters[character_id] = character_data
            self.save_characters()
            return True
        except Exception as e:
            print(f"Error adding character: {e}")
            return False
    
    def update_character(self, character_id: str, updates: Dict) -> bool:
        """Update an existing character"""
        try:
            if character_id not in self.characters:
                return False
            
            self.characters[character_id].update(updates)
            self.characters[character_id]['updated_at'] = datetime.now().isoformat()
            self.save_characters()
            return True
        except Exception as e:
            print(f"Error updating character: {e}")
            return False
    
    def delete_character(self, character_id: str) -> bool:
        """Delete a character"""
        try:
            if character_id in self.characters:
                del self.characters[character_id]
                self.save_characters()
                return True
            return False
        except Exception as e:
            print(f"Error deleting character: {e}")
            return False
    
    def get_character(self, character_id: str) -> Optional[Dict]:
        """Get a specific character"""
        return self.characters.get(character_id)
    
    def get_all_characters(self) -> Dict:
        """Get all characters"""
        return self.characters
    
    def search_characters(self, query: str) -> List[Dict]:
        """Search characters by name or description"""
        query = query.lower()
        results = []
        
        for character in self.characters.values():
            if (query in character.get('name', '').lower() or 
                query in character.get('description', '').lower() or
                query in character.get('personality', '').lower()):
                results.append(character)
        
        return results
    
    def get_character_names(self) -> List[str]:
        """Get list of all character names"""
        return [char.get('name', '') for char in self.characters.values()]
    
    def add_character_note(self, character_id: str, note: str) -> bool:
        """Add a note to a character"""
        try:
            if character_id not in self.characters:
                return False
            
            if 'notes' not in self.characters[character_id]:
                self.characters[character_id]['notes'] = []
            
            note_data = {
                'text': note,
                'timestamp': datetime.now().isoformat()
            }
            
            self.characters[character_id]['notes'].append(note_data)
            self.characters[character_id]['updated_at'] = datetime.now().isoformat()
            self.save_characters()
            return True
        except Exception as e:
            print(f"Error adding note: {e}")
            return False 