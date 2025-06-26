import json
import os
import hashlib
from typing import Dict, List, Optional
from datetime import datetime

class UserManager:
    def __init__(self):
        self.users_file = os.path.join("data", "users.json")
        self.scripts_file = os.path.join("data", "scripts.json")
        self.ensure_data_directory()
        self.load_users()
        self.load_scripts()
    
    def ensure_data_directory(self):
        """Ensure the data directory exists"""
        os.makedirs("data", exist_ok=True)
    
    def load_users(self):
        """Load users from JSON file"""
        if os.path.exists(self.users_file):
            try:
                with open(self.users_file, 'r') as f:
                    self.users = json.load(f)
            except:
                self.users = {}
        else:
            self.users = {}
    
    def load_scripts(self):
        """Load scripts from JSON file"""
        if os.path.exists(self.scripts_file):
            try:
                with open(self.scripts_file, 'r') as f:
                    self.scripts = json.load(f)
            except:
                self.scripts = {}
        else:
            self.scripts = {}
    
    def save_users(self):
        """Save users to JSON file"""
        with open(self.users_file, 'w') as f:
            json.dump(self.users, f, indent=2)
    
    def save_scripts(self):
        """Save scripts to JSON file"""
        with open(self.scripts_file, 'w') as f:
            json.dump(self.scripts, f, indent=2)
    
    def hash_password(self, password: str) -> str:
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register_user(self, username: str, password: str, email: str = "") -> bool:
        """Register a new user"""
        if username in self.users:
            return False  # User already exists
        
        hashed_password = self.hash_password(password)
        self.users[username] = {
            'password': hashed_password,
            'email': email,
            'created_at': datetime.now().isoformat(),
            'last_login': None
        }
        
        # Initialize user's scripts
        self.scripts[username] = []
        
        self.save_users()
        self.save_scripts()
        return True
    
    def authenticate_user(self, username: str, password: str) -> bool:
        """Authenticate a user"""
        if username not in self.users:
            return False
        
        hashed_password = self.hash_password(password)
        if self.users[username]['password'] == hashed_password:
            # Update last login
            self.users[username]['last_login'] = datetime.now().isoformat()
            self.save_users()
            return True
        
        return False
    
    def create_script(self, username: str, script_name: str, description: str = "") -> str:
        """Create a new script for a user"""
        if username not in self.scripts:
            self.scripts[username] = []
        
        script_id = f"{username}_{len(self.scripts[username]) + 1}_{int(datetime.now().timestamp())}"
        
        script_data = {
            'id': script_id,
            'name': script_name,
            'description': description,
            'created_at': datetime.now().isoformat(),
            'last_modified': datetime.now().isoformat(),
            'characters': {},
            'scenes': {},
            'locations': {}
        }
        
        self.scripts[username].append(script_data)
        self.save_scripts()
        return script_id
    
    def get_user_scripts(self, username: str) -> List[Dict]:
        """Get all scripts for a user"""
        return self.scripts.get(username, [])
    
    def get_script(self, username: str, script_id: str) -> Optional[Dict]:
        """Get a specific script"""
        user_scripts = self.get_user_scripts(username)
        for script in user_scripts:
            if script['id'] == script_id:
                return script
        return None
    
    def update_script(self, username: str, script_id: str, script_data: Dict) -> bool:
        """Update a script"""
        user_scripts = self.get_user_scripts(username)
        for i, script in enumerate(user_scripts):
            if script['id'] == script_id:
                script_data['last_modified'] = datetime.now().isoformat()
                self.scripts[username][i] = script_data
                self.save_scripts()
                return True
        return False
    
    def delete_script(self, username: str, script_id: str) -> bool:
        """Delete a script"""
        user_scripts = self.get_user_scripts(username)
        for i, script in enumerate(user_scripts):
            if script['id'] == script_id:
                del self.scripts[username][i]
                self.save_scripts()
                return True
        return False
    
    def user_exists(self, username: str) -> bool:
        """Check if user exists"""
        return username in self.users
    
    def create_test_user_with_sample_data(self):
        """Create Test user with sample data"""
        # Create Test user if it doesn't exist
        if not self.user_exists("Test"):
            self.register_user("Test", "test123", "test@example.com")
        
        # Create a sample script
        script_id = self.create_script("Test", "The Investigation", "A journalist uncovers government corruption")
        
        # Sample characters
        characters = {
            "1": {
                "name": "Sarah Chen",
                "age": 32,
                "description": "Investigative journalist with sharp eyes and determination",
                "personality": "Tenacious, curious, slightly cynical",
                "goals": "Expose the truth about government corruption",
                "conflicts": "Balancing career with personal safety"
            },
            "2": {
                "name": "Detective Mike Rodriguez",
                "age": 45,
                "description": "Veteran detective with a weathered face and kind eyes",
                "personality": "Wise, protective, slightly jaded",
                "goals": "Solve the case and protect Sarah",
                "conflicts": "Department politics vs. doing what's right"
            },
            "3": {
                "name": "Senator James Whitmore",
                "age": 58,
                "description": "Powerful politician with expensive suits and cold demeanor",
                "personality": "Calculating, ruthless, charming when needed",
                "goals": "Maintain power and cover up corruption",
                "conflicts": "Growing paranoia about being exposed"
            }
        }
        
        # Sample locations
        locations = {
            "1": {
                "name": "City News Office",
                "description": "Busy newsroom with desks, computers, and coffee machines",
                "objects": ["desks", "computers", "coffee machines", "whiteboards"],
                "lighting": "Fluorescent overhead lighting",
                "date_time": "Day",
                "type": "Indoor"
            },
            "2": {
                "name": "Police Station",
                "description": "Old building with worn furniture and case files everywhere",
                "objects": ["desks", "filing cabinets", "evidence bags", "coffee pot"],
                "lighting": "Dim fluorescent lighting",
                "date_time": "Day",
                "type": "Indoor"
            },
            "3": {
                "name": "Senate Building",
                "description": "Imposing government building with marble floors and security",
                "objects": ["marble floors", "security cameras", "expensive furniture", "portraits"],
                "lighting": "Elegant chandeliers",
                "date_time": "Day",
                "type": "Indoor"
            },
            "4": {
                "name": "Dark Alley",
                "description": "Narrow alley with dumpsters and graffiti-covered walls",
                "objects": ["dumpsters", "graffiti", "trash cans", "fire escapes"],
                "lighting": "Street lights and shadows",
                "date_time": "Night",
                "type": "Outdoor"
            }
        }
        
        # Sample scenes
        scenes = {
            "1": {
                "id": "1",
                "scene_number": 1,
                "title": "The Tip",
                "location": "City News Office",
                "time_of_day": "Day",
                "tone_mood": ["tense", "mysterious"],
                "characters": ["Sarah Chen"],
                "action": "Sarah sits at her desk, surrounded by newspaper clippings. She's been working late, and the office is nearly empty. Her phone rings with an anonymous tip about government corruption.",
                "goal": "Introduce Sarah and the central mystery"
            },
            "2": {
                "id": "2",
                "scene_number": 2,
                "title": "Meeting the Detective",
                "location": "Police Station",
                "time_of_day": "Day",
                "tone_mood": ["professional", "suspenseful"],
                "characters": ["Sarah Chen", "Detective Mike Rodriguez"],
                "action": "Sarah meets Detective Rodriguez to discuss the case. He's initially skeptical but becomes intrigued by her evidence. They form an uneasy alliance.",
                "goal": "Establish the partnership between Sarah and Mike"
            },
            "3": {
                "id": "3",
                "scene_number": 3,
                "title": "The Senator's Office",
                "location": "Senate Building",
                "time_of_day": "Day",
                "tone_mood": ["tense", "powerful"],
                "characters": ["Sarah Chen", "Senator James Whitmore"],
                "action": "Sarah confronts Senator Whitmore with her findings. He denies everything but his nervous behavior reveals the truth. The tension builds as they engage in a verbal chess match.",
                "goal": "Show the confrontation and establish the antagonist"
            },
            "4": {
                "id": "4",
                "scene_number": 4,
                "title": "The Chase",
                "location": "Dark Alley",
                "time_of_day": "Night",
                "tone_mood": ["action", "dangerous"],
                "characters": ["Sarah Chen", "Detective Mike Rodriguez"],
                "action": "Sarah and Mike are chased through the dark alley by unknown assailants. They must work together to escape, revealing their growing trust and the danger they're in.",
                "goal": "Create action and show the stakes"
            }
        }
        
        # Update the script with sample data
        script = self.get_script("Test", script_id)
        if script:
            script['characters'] = characters
            script['locations'] = locations
            script['scenes'] = scenes
            self.update_script("Test", script_id, script)
        
        return script_id 