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