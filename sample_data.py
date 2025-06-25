from typing import Dict, List

def get_sample_locations() -> List[Dict]:
    """Generate sample locations for demonstration"""
    return [
        {
            'name': 'Downtown News Office',
            'description': 'A bustling newsroom with rows of desks, computers, and the constant hum of activity. Large windows overlook the city skyline.',
            'objects': ['desks', 'computers', 'newspapers', 'coffee machine', 'whiteboard', 'filing cabinets'],
            'lighting': 'Bright fluorescent lighting with natural light from large windows',
            'date_time': 'Daytime, business hours'
        },
        {
            'name': 'Police Station - Interrogation Room',
            'description': 'A small, dimly lit room with a metal table and chairs. The walls are bare except for a one-way mirror.',
            'objects': ['metal table', 'chairs', 'one-way mirror', 'recording equipment', 'coffee cups'],
            'lighting': 'Dim overhead lighting, creates an atmosphere of tension',
            'date_time': 'Night, after hours'
        },
        {
            'name': 'City Hall - Mayor\'s Office',
            'description': 'An elegant office with mahogany furniture, leather chairs, and city memorabilia. Large windows provide a view of the city.',
            'objects': ['mahogany desk', 'leather chairs', 'city memorabilia', 'flags', 'family photos', 'phone'],
            'lighting': 'Warm, professional lighting with natural light from windows',
            'date_time': 'Daytime, business hours'
        },
        {
            'name': 'Sarah\'s Apartment',
            'description': 'A modest apartment cluttered with research materials, newspapers, and takeout containers. The living room serves as her home office.',
            'objects': ['research materials', 'newspapers', 'takeout containers', 'laptop', 'whiteboard', 'coffee table'],
            'lighting': 'Warm lamp lighting, cozy but cluttered',
            'date_time': 'Night, late hours'
        },
        {
            'name': 'Abandoned Warehouse',
            'description': 'A large, empty warehouse with concrete floors and metal beams. Dust particles float in the air, and the space echoes.',
            'objects': ['concrete floors', 'metal beams', 'dust', 'empty space', 'loading dock'],
            'lighting': 'Minimal lighting, shadows and darkness create tension',
            'date_time': 'Night, dark and dangerous'
        }
    ]

def get_sample_characters() -> List[Dict]:
    """Generate sample characters for demonstration"""
    return [
        {
            'name': 'Sarah Mitchell',
            'age': 28,
            'description': 'A determined investigative journalist with sharp eyes and a quick wit. She wears practical clothing and always carries a notebook.',
            'personality': 'Intelligent, persistent, slightly cynical but with a strong moral compass. She\'s driven by the truth and justice.',
            'goals': 'To expose corruption in the city government and find her missing colleague.',
            'conflicts': 'Internal: Struggles with trust issues after being betrayed by sources. External: Powerful people want to silence her investigation.'
        },
        {
            'name': 'Detective Marcus Chen',
            'age': 42,
            'description': 'A seasoned detective with graying temples and a calm demeanor. He moves with purpose and speaks deliberately.',
            'personality': 'Methodical, patient, and deeply empathetic. He believes in the system but knows its flaws.',
            'goals': 'To solve the case while protecting Sarah and maintaining his integrity.',
            'conflicts': 'Internal: Balancing duty with personal relationships. External: Political pressure to close the case quickly.'
        },
        {
            'name': 'Mayor Richard Blackwood',
            'age': 55,
            'description': 'A charismatic politician with silver hair and expensive suits. He has a practiced smile that doesn\'t reach his eyes.',
            'personality': 'Charming in public, ruthless in private. He\'s used to getting what he wants and doesn\'t like obstacles.',
            'goals': 'To maintain power and cover up his involvement in the corruption scandal.',
            'conflicts': 'Internal: Guilt over his actions but unwilling to face consequences. External: Sarah\'s investigation threatens everything.'
        }
    ]

def get_sample_scenes() -> List[Dict]:
    """Generate sample scenes for demonstration"""
    return [
        {
            'scene_number': 1,
            'title': 'Scene 1 – Morning at the Lab',
            'location': 'Downtown News Office',
            'time_of_day': 'Morning',
            'tone_mood': ['tense', 'determined'],
            'characters': ['Sarah Mitchell', 'Editor Tom'],
            'action': 'Sarah sits at her desk, surrounded by newspaper clippings and photos. She\'s been working late, and the office is nearly empty. Her phone rings with an anonymous tip about government corruption.\n\nSARAH: "I need to follow this lead, Tom. It could be the biggest story of my career."\n\nTOM: "Be careful, Sarah. These people play dirty."\n\nSarah nods, determination in her eyes as she starts gathering her research materials.',
            'beats': [
                'Sarah receives anonymous tip',
                'Tom warns her about danger',
                'Sarah decides to investigate'
            ],
            'goal': 'Establish Sarah\'s determination and the dangerous nature of her investigation',
            'conflict_stakes': 'Sarah\'s career and safety vs. exposing corruption',
            'links_to_scenes': ['scene_2']
        },
        {
            'scene_number': 2,
            'title': 'Scene 2 – The Interrogation',
            'location': 'Police Station - Interrogation Room',
            'time_of_day': 'Night',
            'tone_mood': ['suspenseful', 'professional'],
            'characters': ['Detective Marcus Chen', 'Sarah Mitchell'],
            'action': 'Sarah is being questioned about her colleague\'s disappearance. Marcus is sympathetic but professional. The room is dimly lit, creating an atmosphere of tension.\n\nMARCUS: "When was the last time you saw your colleague?"\n\nSARAH: "Yesterday morning. He was working on the same story I am."\n\nMARCUS: "What story is that?"\n\nSARAH: "The one that got him killed."\n\nMarcus leans forward, his expression becoming more serious.',
            'beats': [
                'Marcus questions Sarah',
                'Sarah reveals colleague\'s disappearance',
                'Connection to investigation established'
            ],
            'goal': 'Introduce Marcus and establish the connection between Sarah\'s investigation and her colleague\'s disappearance',
            'conflict_stakes': 'Finding the missing colleague vs. political pressure',
            'links_to_scenes': ['scene_1', 'scene_3']
        },
        {
            'scene_number': 3,
            'title': 'Scene 3 – The Mayor\'s Response',
            'location': 'City Hall - Mayor\'s Office',
            'time_of_day': 'Day',
            'tone_mood': ['tense', 'political'],
            'characters': ['Mayor Richard Blackwood', 'Chief of Staff Lisa'],
            'action': 'The mayor receives news about Sarah\'s investigation. He\'s outwardly calm but his hands betray his nervousness. He gives orders to his staff.\n\nBLACKWOOD: "Handle this situation, Lisa. I don\'t care how."\n\nLISA: "The detective assigned to the case is Marcus Chen."\n\nBLACKWOOD: "Marcus Chen? That could be a problem."\n\nHe paces behind his desk, clearly agitated by this development.',
            'beats': [
                'Mayor learns about investigation',
                'Lisa reports on detective assignment',
                'Mayor shows concern about Marcus'
            ],
            'goal': 'Introduce the antagonist and show his reaction to the investigation threat',
            'conflict_stakes': 'Mayor\'s political career vs. justice',
            'links_to_scenes': ['scene_2', 'scene_4']
        },
        {
            'scene_number': 4,
            'title': 'Scene 4 – The Breakthrough',
            'location': 'Sarah\'s Apartment',
            'time_of_day': 'Night',
            'tone_mood': ['hopeful', 'intense'],
            'characters': ['Sarah Mitchell'],
            'action': 'Sarah works late into the night, piecing together evidence. Her apartment is cluttered with research materials. She discovers a crucial connection.\n\nSARAH: (to herself) "Blackwood Construction... city contracts... missing money... It all connects."\n\nShe frantically writes notes, connecting the dots between the various pieces of evidence spread across her table.',
            'beats': [
                'Sarah works through evidence',
                'Discovers crucial connection',
                'Realizes the scope of corruption'
            ],
            'goal': 'Show Sarah\'s investigative process and the breakthrough moment',
            'conflict_stakes': 'Finding the truth vs. personal safety',
            'links_to_scenes': ['scene_3', 'scene_5']
        },
        {
            'scene_number': 5,
            'title': 'Scene 5 – The Confrontation',
            'location': 'Abandoned Warehouse',
            'time_of_day': 'Night',
            'tone_mood': ['climactic', 'dangerous'],
            'characters': ['Sarah Mitchell', 'Detective Marcus Chen', 'Mayor Blackwood'],
            'action': 'The final confrontation. Sarah and Marcus have evidence, but Blackwood has backup. Tense standoff with guns drawn.\n\nBLACKWOOD: "You should have left well enough alone."\n\nSARAH: "The truth always comes out, Mayor."\n\nMARCUS: "It\'s over, Blackwood. We have everything."\n\nBlackwood\'s men lower their weapons as the sound of police sirens approaches.',
            'beats': [
                'Final confrontation begins',
                'Evidence is presented',
                'Justice prevails'
            ],
            'goal': 'Climactic scene with all major characters. High stakes confrontation',
            'conflict_stakes': 'Justice vs. corruption, life and death',
            'links_to_scenes': ['scene_4']
        }
    ]

def add_sample_data_to_managers(character_manager, scene_manager, location_manager):
    """Add sample data to the managers"""
    # Add sample locations
    sample_locations = get_sample_locations()
    for loc in sample_locations:
        location_manager.add_location(loc)
    
    # Add sample characters
    sample_characters = get_sample_characters()
    for char in sample_characters:
        character_manager.add_character(char)
    
    # Add sample scenes
    sample_scenes = get_sample_scenes()
    for scene in sample_scenes:
        scene_manager.add_scene(scene)
    
    return len(sample_characters), len(sample_scenes), len(sample_locations) 