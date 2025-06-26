import google.generativeai as genai
import json
from typing import Dict, List, Optional
from config import Config

class LLMClient:
    def __init__(self):
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(Config.MODEL_NAME)
        self.temperature = Config.TEMPERATURE
        self.max_tokens = Config.MAX_TOKENS
    
    def generate_response(self, prompt: str, context: str = "") -> str:
        """Generate response from Gemini with context"""
        try:
            full_prompt = f"{context}\n\n{prompt}" if context else prompt
            
            # Add system prompt for screenwriting expertise
            system_prompt = "You are an expert screenwriting assistant. Help filmmakers with script development, character development, scene writing, and story structure."
            full_prompt = f"{system_prompt}\n\n{full_prompt}"
            
            response = self.model.generate_content(
                full_prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=self.temperature,
                    max_output_tokens=self.max_tokens
                )
            )
            return response.text
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    def chat_with_context(self, user_message: str, context: str) -> str:
        """Chat with full context from characters, scenes, and chat history"""
        try:
            full_prompt = f"""
You are an expert screenwriting assistant with full knowledge of the filmmaker's script. Use the context below to provide personalized, relevant advice.

IMPORTANT: Keep your responses short and concise (2-3 sentences maximum). Only answer if the user is asking a question.

CONTEXT:
{context}

USER MESSAGE: {user_message}

Please respond as a helpful screenwriting assistant, referencing specific characters, scenes, and previous conversation when relevant. Be conversational but professional. Keep answers brief and to the point.
"""
            
            response = self.model.generate_content(
                full_prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=self.temperature,
                    max_output_tokens=150  # Reduced for shorter responses
                )
            )
            return response.text
        except Exception as e:
            return f"Error generating chat response: {str(e)}"
    
    def analyze_character(self, character_data: Dict) -> str:
        """Analyze character and provide development suggestions"""
        prompt = f"""
        Analyze this character and provide development suggestions:
        
        Name: {character_data.get('name', 'Unknown')}
        Age: {character_data.get('age', 'Unknown')}
        Description: {character_data.get('description', 'No description')}
        Personality: {character_data.get('personality', 'No personality traits')}
        Goals: {character_data.get('goals', 'No goals specified')}
        Conflicts: {character_data.get('conflicts', 'No conflicts specified')}
        
        Please provide:
        1. Character arc suggestions
        2. Dialogue style recommendations
        3. Potential conflicts and obstacles
        4. Character development opportunities
        """
        return self.generate_response(prompt)
    
    def modify_text_tone(self, text: str, new_tone: str) -> str:
        """Modify text to match a specific tone"""
        prompt = f"""
        Rewrite the following text to match the tone: {new_tone}
        
        Original text:
        {text}
        
        Please maintain the same meaning and structure while changing the tone to {new_tone}.
        """
        return self.generate_response(prompt)
    
    def modify_setting(self, scene_text: str, new_setting: str) -> str:
        """Modify scene to fit a new setting"""
        prompt = f"""
        Adapt the following scene to the new setting: {new_setting}
        
        Original scene:
        {scene_text}
        
        Please rewrite the scene to fit the new setting while maintaining the core action and dialogue.
        """
        return self.generate_response(prompt)
    
    def generate_dialogue(self, character_name: str, context: str, emotion: str = "neutral") -> str:
        """Generate dialogue for a character"""
        prompt = f"""
        Generate dialogue for {character_name} in the following context:
        
        Context: {context}
        Emotion: {emotion}
        
        Please write natural, character-appropriate dialogue that fits the context and emotion.
        """
        return self.generate_response(prompt)
    
    def analyze_scene(self, scene_data: Dict) -> str:
        """Analyze scene and provide improvement suggestions"""
        characters_str = ', '.join(scene_data.get('characters', [])) if isinstance(scene_data.get('characters', []), list) else scene_data.get('characters', 'No characters')
        tone_str = ', '.join(scene_data.get('tone_mood', [])) if isinstance(scene_data.get('tone_mood', []), list) else scene_data.get('tone_mood', 'No tone')
        
        prompt = f"""
        Analyze this scene and provide improvement suggestions:
        
        Scene: {scene_data.get('scene_number', 'Unknown')} - {scene_data.get('title', 'No title')}
        Location: {scene_data.get('location', 'No location')}
        Time of Day: {scene_data.get('time_of_day', 'No time')}
        Tone/Mood: {tone_str}
        Characters: {characters_str}
        Goal: {scene_data.get('goal', 'No goal')}
        Conflict/Stakes: {scene_data.get('conflict_stakes', 'No conflict')}
        Script Content: {scene_data.get('action', 'No content')}
        
        Please provide:
        1. Pacing analysis
        2. Character interaction suggestions
        3. Visual storytelling opportunities
        4. Dialogue improvements
        5. Scene structure recommendations
        6. Location utilization suggestions
        7. Tone and mood consistency
        8. Goal and conflict clarity
        """
        return self.generate_response(prompt) 