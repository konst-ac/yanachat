import json
import os
from typing import Dict, List, Optional
from datetime import datetime
from config import Config

class SceneManager:
    def __init__(self):
        self.scenes_file = os.path.join(Config.SCENE_FILE_PATH, "scenes.json")
        self.scenes = self.load_scenes()
    
    def load_scenes(self) -> Dict:
        """Load scenes from JSON file"""
        if os.path.exists(self.scenes_file):
            try:
                with open(self.scenes_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading scenes: {e}")
                return {}
        return {}
    
    def save_scenes(self):
        """Save scenes to JSON file"""
        try:
            with open(self.scenes_file, 'w', encoding='utf-8') as f:
                json.dump(self.scenes, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving scenes: {e}")
    
    def add_scene(self, scene_data: Dict) -> bool:
        """Add a new scene"""
        try:
            scene_number = scene_data.get('scene_number', '1')
            scene_id = f"scene_{scene_number}"
            
            if scene_id in self.scenes:
                return False  # Scene already exists
            
            scene_data['id'] = scene_id
            scene_data['created_at'] = datetime.now().isoformat()
            scene_data['updated_at'] = datetime.now().isoformat()
            
            # Ensure all required fields exist with defaults
            scene_data.setdefault('title', f'Scene {scene_number}')
            scene_data.setdefault('location', '')
            scene_data.setdefault('time_of_day', 'Day')
            scene_data.setdefault('tone_mood', [])
            scene_data.setdefault('characters', [])
            scene_data.setdefault('action', '')
            scene_data.setdefault('dialogue', '')
            scene_data.setdefault('notes', [])
            scene_data.setdefault('beats', [])
            scene_data.setdefault('goal', '')
            scene_data.setdefault('conflict_stakes', '')
            scene_data.setdefault('links_to_scenes', [])
            
            self.scenes[scene_id] = scene_data
            self.save_scenes()
            return True
        except Exception as e:
            print(f"Error adding scene: {e}")
            return False
    
    def update_scene(self, scene_id: str, updates: Dict) -> bool:
        """Update an existing scene"""
        try:
            if scene_id not in self.scenes:
                return False
            
            self.scenes[scene_id].update(updates)
            self.scenes[scene_id]['updated_at'] = datetime.now().isoformat()
            self.save_scenes()
            return True
        except Exception as e:
            print(f"Error updating scene: {e}")
            return False
    
    def delete_scene(self, scene_id: str) -> bool:
        """Delete a scene"""
        try:
            if scene_id in self.scenes:
                del self.scenes[scene_id]
                self.save_scenes()
                return True
            return False
        except Exception as e:
            print(f"Error deleting scene: {e}")
            return False
    
    def get_scene(self, scene_id: str) -> Optional[Dict]:
        """Get a specific scene"""
        return self.scenes.get(scene_id)
    
    def get_all_scenes(self) -> Dict:
        """Get all scenes"""
        return self.scenes
    
    def get_scenes_by_character(self, character_name: str) -> List[Dict]:
        """Get all scenes featuring a specific character"""
        character_name = character_name.lower()
        results = []
        
        for scene in self.scenes.values():
            characters = scene.get('characters', [])
            if isinstance(characters, str):
                characters = [char.strip() for char in characters.split(',')]
            
            if any(character_name in char.lower() for char in characters):
                results.append(scene)
        
        return results
    
    def get_scenes_by_location(self, location: str) -> List[Dict]:
        """Get all scenes in a specific location"""
        location = location.lower()
        results = []
        
        for scene in self.scenes.values():
            scene_location = scene.get('location', '').lower()
            if location in scene_location:
                results.append(scene)
        
        return results
    
    def get_scenes_by_setting(self, setting: str) -> List[Dict]:
        """Get all scenes in a specific setting"""
        setting = setting.lower()
        results = []
        
        for scene in self.scenes.values():
            scene_setting = scene.get('setting', '').lower()
            if setting in scene_setting:
                results.append(scene)
        
        return results
    
    def search_scenes(self, query: str) -> List[Dict]:
        """Search scenes by content"""
        query = query.lower()
        results = []
        
        for scene in self.scenes.values():
            if (query in scene.get('title', '').lower() or
                query in scene.get('location', '').lower() or
                query in scene.get('action', '').lower() or
                query in scene.get('dialogue', '').lower() or
                query in scene.get('goal', '').lower() or
                query in scene.get('conflict_stakes', '').lower()):
                results.append(scene)
        
        return results
    
    def add_scene_note(self, scene_id: str, note: str) -> bool:
        """Add a note to a scene"""
        try:
            if scene_id not in self.scenes:
                return False
            
            if 'notes' not in self.scenes[scene_id]:
                self.scenes[scene_id]['notes'] = []
            
            note_data = {
                'text': note,
                'timestamp': datetime.now().isoformat()
            }
            
            self.scenes[scene_id]['notes'].append(note_data)
            self.scenes[scene_id]['updated_at'] = datetime.now().isoformat()
            self.save_scenes()
            return True
        except Exception as e:
            print(f"Error adding note: {e}")
            return False
    
    def add_scene_beat(self, scene_id: str, beat: str) -> bool:
        """Add a beat to a scene"""
        try:
            if scene_id not in self.scenes:
                return False
            
            if 'beats' not in self.scenes[scene_id]:
                self.scenes[scene_id]['beats'] = []
            
            beat_data = {
                'text': beat,
                'timestamp': datetime.now().isoformat()
            }
            
            self.scenes[scene_id]['beats'].append(beat_data)
            self.scenes[scene_id]['updated_at'] = datetime.now().isoformat()
            self.save_scenes()
            return True
        except Exception as e:
            print(f"Error adding beat: {e}")
            return False
    
    def get_scene_sequence(self) -> List[Dict]:
        """Get scenes in chronological order"""
        sorted_scenes = sorted(
            self.scenes.values(),
            key=lambda x: int(x.get('scene_number', 0))
        )
        return sorted_scenes
    
    def get_scene_statistics(self) -> Dict:
        """Get statistics about scenes"""
        total_scenes = len(self.scenes)
        total_characters = set()
        locations = set()
        
        for scene in self.scenes.values():
            characters = scene.get('characters', [])
            if isinstance(characters, str):
                characters = [char.strip() for char in characters.split(',')]
            total_characters.update(characters)
            locations.add(scene.get('location', ''))
        
        return {
            'total_scenes': total_scenes,
            'unique_characters': len(total_characters),
            'unique_locations': len(locations),
            'average_scene_length': sum(len(scene.get('action', '')) for scene in self.scenes.values()) / total_scenes if total_scenes > 0 else 0
        } 