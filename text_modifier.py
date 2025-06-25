from typing import Dict, List, Optional
from llm_client import LLMClient

class TextModifier:
    def __init__(self):
        self.llm_client = LLMClient()
    
    def modify_tone(self, text: str, new_tone: str, context: str = "") -> str:
        """Modify the tone of text while maintaining meaning"""
        return self.llm_client.modify_text_tone(text, new_tone)
    
    def modify_setting(self, scene_text: str, new_setting: str) -> str:
        """Modify scene to fit a new setting"""
        return self.llm_client.modify_setting(scene_text, new_setting)
    
    def generate_dialogue(self, character_name: str, context: str, emotion: str = "neutral") -> str:
        """Generate dialogue for a character"""
        return self.llm_client.generate_dialogue(character_name, context, emotion)
    
    def expand_scene(self, scene_text: str, expansion_type: str) -> str:
        """Expand a scene with more detail"""
        prompt = f"""
        Expand the following scene with more {expansion_type}:
        
        {scene_text}
        
        Please add more {expansion_type} while maintaining the original structure and meaning.
        """
        return self.llm_client.generate_response(prompt)
    
    def condense_scene(self, scene_text: str) -> str:
        """Condense a scene while maintaining key elements"""
        prompt = f"""
        Condense the following scene while maintaining all key plot points and character development:
        
        {scene_text}
        
        Please create a more concise version that preserves the essential elements.
        """
        return self.llm_client.generate_response(prompt)
    
    def change_perspective(self, scene_text: str, new_perspective: str) -> str:
        """Change the narrative perspective of a scene"""
        prompt = f"""
        Rewrite the following scene from a {new_perspective} perspective:
        
        {scene_text}
        
        Please maintain the same events and dialogue while changing the narrative perspective to {new_perspective}.
        """
        return self.llm_client.generate_response(prompt)
    
    def add_conflict(self, scene_text: str, conflict_type: str) -> str:
        """Add conflict to a scene"""
        prompt = f"""
        Add {conflict_type} conflict to the following scene:
        
        {scene_text}
        
        Please integrate the conflict naturally into the existing scene while maintaining character consistency.
        """
        return self.llm_client.generate_response(prompt)
    
    def improve_dialogue(self, dialogue: str, character_name: str = "") -> str:
        """Improve dialogue to be more natural and character-specific"""
        prompt = f"""
        Improve the following dialogue to be more natural and engaging:
        
        Character: {character_name}
        Dialogue: {dialogue}
        
        Please make the dialogue more realistic, character-specific, and emotionally engaging.
        """
        return self.llm_client.generate_response(prompt)
    
    def add_visual_elements(self, scene_text: str) -> str:
        """Add visual storytelling elements to a scene"""
        prompt = f"""
        Add visual storytelling elements to the following scene:
        
        {scene_text}
        
        Please add cinematic details, visual cues, and atmospheric elements that enhance the visual storytelling.
        """
        return self.llm_client.generate_response(prompt)
    
    def create_transition(self, scene1: str, scene2: str) -> str:
        """Create a smooth transition between two scenes"""
        prompt = f"""
        Create a smooth transition between these two scenes:
        
        Scene 1:
        {scene1}
        
        Scene 2:
        {scene2}
        
        Please write a brief transition that connects these scenes naturally and maintains narrative flow.
        """
        return self.llm_client.generate_response(prompt)
    
    def fix_continuity_issues(self, scene_text: str, previous_scenes: List[str]) -> str:
        """Fix continuity issues in a scene"""
        context = "\n\n".join(previous_scenes)
        prompt = f"""
        Fix any continuity issues in the following scene based on the previous scenes:
        
        Previous scenes:
        {context}
        
        Current scene:
        {scene_text}
        
        Please identify and fix any continuity issues while maintaining the scene's integrity.
        """
        return self.llm_client.generate_response(prompt)
    
    def enhance_character_development(self, scene_text: str, character_name: str) -> str:
        """Enhance character development in a scene"""
        prompt = f"""
        Enhance the character development for {character_name} in the following scene:
        
        {scene_text}
        
        Please add elements that reveal more about {character_name}'s personality, motivations, or growth.
        """
        return self.llm_client.generate_response(prompt) 