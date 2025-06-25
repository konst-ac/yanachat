import json
import os
from typing import Dict, List, Optional
from datetime import datetime
from config import Config

class LocationManager:
    def __init__(self):
        self.locations_file = os.path.join(Config.LOCATION_FILE_PATH, "locations.json")
        self.locations = self.load_locations()
    
    def load_locations(self) -> Dict:
        """Load locations from JSON file"""
        if os.path.exists(self.locations_file):
            try:
                with open(self.locations_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading locations: {e}")
                return {}
        return {}
    
    def save_locations(self):
        """Save locations to JSON file"""
        try:
            os.makedirs(os.path.dirname(self.locations_file), exist_ok=True)
            with open(self.locations_file, 'w', encoding='utf-8') as f:
                json.dump(self.locations, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving locations: {e}")
    
    def add_location(self, location_data: Dict) -> bool:
        """Add a new location"""
        try:
            location_name = location_data.get('name', '').strip()
            if not location_name:
                return False
            
            location_id = location_name.lower().replace(' ', '_').replace('-', '_')
            if location_id in self.locations:
                return False  # Location already exists
            
            location_data['id'] = location_id
            location_data['name'] = location_name
            location_data['created_at'] = datetime.now().isoformat()
            location_data['updated_at'] = datetime.now().isoformat()
            
            # Ensure all required fields exist
            location_data.setdefault('description', '')
            location_data.setdefault('objects', [])
            location_data.setdefault('lighting', '')
            location_data.setdefault('date_time', '')
            
            self.locations[location_id] = location_data
            self.save_locations()
            return True
        except Exception as e:
            print(f"Error adding location: {e}")
            return False
    
    def update_location(self, location_id: str, updates: Dict) -> bool:
        """Update an existing location"""
        try:
            if location_id not in self.locations:
                return False
            
            self.locations[location_id].update(updates)
            self.locations[location_id]['updated_at'] = datetime.now().isoformat()
            self.save_locations()
            return True
        except Exception as e:
            print(f"Error updating location: {e}")
            return False
    
    def delete_location(self, location_id: str) -> bool:
        """Delete a location"""
        try:
            if location_id in self.locations:
                del self.locations[location_id]
                self.save_locations()
                return True
            return False
        except Exception as e:
            print(f"Error deleting location: {e}")
            return False
    
    def get_location(self, location_id: str) -> Optional[Dict]:
        """Get a specific location"""
        return self.locations.get(location_id)
    
    def get_all_locations(self) -> Dict:
        """Get all locations"""
        return self.locations
    
    def get_location_names(self) -> List[str]:
        """Get list of all location names"""
        return [loc.get('name', '') for loc in self.locations.values()]
    
    def search_locations(self, query: str) -> List[Dict]:
        """Search locations by name or description"""
        query = query.lower()
        results = []
        
        for location in self.locations.values():
            if (query in location.get('name', '').lower() or 
                query in location.get('description', '').lower()):
                results.append(location)
        
        return results
    
    def add_location_note(self, location_id: str, note: str) -> bool:
        """Add a note to a location"""
        try:
            if location_id not in self.locations:
                return False
            
            if 'notes' not in self.locations[location_id]:
                self.locations[location_id]['notes'] = []
            
            note_data = {
                'text': note,
                'timestamp': datetime.now().isoformat()
            }
            
            self.locations[location_id]['notes'].append(note_data)
            self.locations[location_id]['updated_at'] = datetime.now().isoformat()
            self.save_locations()
            return True
        except Exception as e:
            print(f"Error adding note: {e}")
            return False
    
    def get_locations_by_type(self, location_type: str) -> List[Dict]:
        """Get locations by type (e.g., indoor, outdoor, public, private)"""
        location_type = location_type.lower()
        results = []
        
        for location in self.locations.values():
            if location_type in location.get('type', '').lower():
                results.append(location)
        
        return results 