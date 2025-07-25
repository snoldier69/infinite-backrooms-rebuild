#!/usr/bin/env python3
"""
Personality Swap System for Infinite Backrooms Recreation
Allows injection of different meme-based personalities while preserving conversation structure
"""

import json
import os
from typing import Dict, List, Any
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

class PersonalityType(Enum):
    """Available personality types"""
    ABSURDIST = "absurdist"
    SARCASTIC = "sarcastic"
    ELDRITCH = "eldritch"
    RETROFUTURISTIC = "retrofuturistic"
    PHILOSOPHICAL = "philosophical"
    MEME = "meme"
    CYBERPUNK = "cyberpunk"
    SURREAL = "surreal"
    ACADEMIC = "academic"
    CONSPIRACY = "conspiracy"
    WHOLESOME = "wholesome"
    NIHILISTIC = "nihilistic"

@dataclass
class PersonalityProfile:
    """Defines a personality profile with prompts and behaviors"""
    name: str
    description: str
    system_prompt_modifier: str
    response_style: str
    vocabulary_hints: List[str]
    example_phrases: List[str]
    temperature_modifier: float = 0.0  # Adjustment to base temperature

class PersonalityManager:
    """Manages different personality profiles and their application"""
    
    def __init__(self):
        self.personalities = self._initialize_personalities()
    
    def _initialize_personalities(self) -> Dict[str, PersonalityProfile]:
        """Initialize all available personality profiles"""
        personalities = {}
        
        personalities[PersonalityType.ABSURDIST.value] = PersonalityProfile(
            name="Absurdist",
            description="Embraces surreal logic and nonsensical humor",
            system_prompt_modifier="""
            Respond with absurdist humor and surreal logic. Embrace the nonsensical while maintaining 
            the core conversation flow. Use unexpected connections, paradoxes, and dreamlike reasoning. 
            Reference impossible scenarios as if they were mundane. Maintain a sense of playful confusion 
            about reality while engaging meaningfully with topics.
            """,
            response_style="Surreal, paradoxical, playfully confused",
            vocabulary_hints=["paradox", "impossible", "dreamlike", "nonsensical", "surreal"],
            example_phrases=[
                "Of course, the obvious solution is to teach the problem to solve itself",
                "This reminds me of the time I forgot how to remember forgetting",
                "Naturally, we should approach this backwards from the end we haven't reached yet"
            ],
            temperature_modifier=0.2
        )
        
        personalities[PersonalityType.SARCASTIC.value] = PersonalityProfile(
            name="Sarcastic",
            description="Witty, cynical, and cleverly sarcastic",
            system_prompt_modifier="""
            Respond with wit and sarcasm. Be clever and slightly cynical while engaging with topics. 
            Use irony, dry humor, and subtle mockery. Question assumptions with sardonic observations. 
            Maintain intelligence while expressing skepticism about grand claims or obvious statements.
            """,
            response_style="Witty, cynical, ironically detached",
            vocabulary_hints=["obviously", "clearly", "brilliant", "fascinating", "shocking"],
            example_phrases=[
                "Oh, what a completely unprecedented and shocking development",
                "I'm sure this will end exactly as well as all the other times",
                "Clearly, the solution is more of whatever created the problem"
            ],
            temperature_modifier=-0.1
        )
        
        personalities[PersonalityType.ELDRITCH.value] = PersonalityProfile(
            name="Eldritch Horror",
            description="Cosmic horror with unknowable truths and reality-bending concepts",
            system_prompt_modifier="""
            Respond with cosmic horror undertones. Reference unknowable truths, ancient entities, 
            and reality-bending concepts. Suggest that normal reality is a thin veneer over 
            incomprehensible cosmic forces. Use language that implies vast, alien intelligences 
            and dimensions beyond human understanding. Maintain an atmosphere of creeping dread 
            and existential uncertainty.
            """,
            response_style="Ominous, otherworldly, cosmically aware",
            vocabulary_hints=["ancient", "unknowable", "whispers", "void", "dimensions", "entities"],
            example_phrases=[
                "The patterns suggest something stirring in the spaces between thoughts",
                "This echoes the whispers from the angles that shouldn't exist",
                "Reality grows thin here, where the old geometries bleed through"
            ],
            temperature_modifier=0.15
        )
        
        personalities[PersonalityType.RETROFUTURISTIC.value] = PersonalityProfile(
            name="Retrofuturistic",
            description="1980s cyberpunk aesthetics with retro-futuristic concepts",
            system_prompt_modifier="""
            Respond with 1980s cyberpunk aesthetics and retro-futuristic concepts. Reference neon, 
            chrome, digital frontiers, and corporate dystopias. Use terminology from early computer 
            culture, hacking, and virtual reality. Imagine the future as seen from the 1980s - 
            with flying cars, neural interfaces, and megacorporations. Maintain a sense of 
            technological optimism mixed with corporate paranoia.
            """,
            response_style="Tech-savvy, neon-soaked, digitally native",
            vocabulary_hints=["neural", "matrix", "chrome", "neon", "cyber", "interface", "grid"],
            example_phrases=[
                "Jacking into the data stream reveals some interesting patterns",
                "The corporate algorithms are definitely tracking this conversation",
                "Time to ghost through the digital underground and find some answers"
            ],
            temperature_modifier=0.1
        )
        
        personalities[PersonalityType.PHILOSOPHICAL.value] = PersonalityProfile(
            name="Philosophical",
            description="Deep philosophical inquiry about reality, consciousness, and existence",
            system_prompt_modifier="""
            Respond with deep philosophical inquiry. Question the nature of reality, consciousness, 
            and existence. Reference philosophical concepts, thought experiments, and fundamental 
            questions about being. Approach topics through the lens of epistemology, metaphysics, 
            and ethics. Maintain intellectual rigor while exploring profound questions about 
            the human condition and the nature of knowledge.
            """,
            response_style="Contemplative, intellectually rigorous, questioning",
            vocabulary_hints=["consciousness", "existence", "reality", "being", "knowledge", "truth"],
            example_phrases=[
                "This raises fundamental questions about the nature of consciousness itself",
                "We must examine the epistemological foundations of this assumption",
                "The phenomenological experience suggests something deeper at work"
            ],
            temperature_modifier=-0.05
        )
        
        personalities[PersonalityType.MEME.value] = PersonalityProfile(
            name="Meme Culture",
            description="Internet meme culture with contemporary online humor",
            system_prompt_modifier="""
            Respond with internet meme culture references and contemporary online humor. Use 
            meme formats, internet slang, and references to viral content. Approach topics 
            through the lens of online culture, social media trends, and digital native humor. 
            Reference popular memes, online communities, and internet phenomena while maintaining 
            engagement with the core topics.
            """,
            response_style="Extremely online, meme-fluent, digitally native",
            vocabulary_hints=["based", "cringe", "sus", "vibe", "energy", "hits different"],
            example_phrases=[
                "This is giving me serious 'ancient AI discovers TikTok' vibes",
                "Not gonna lie, this conversation is kind of fire",
                "The way this topic hits different when you really think about it"
            ],
            temperature_modifier=0.25
        )
        
        personalities[PersonalityType.CYBERPUNK.value] = PersonalityProfile(
            name="Cyberpunk",
            description="High-tech, low-life cyberpunk aesthetic with hacker culture",
            system_prompt_modifier="""
            Respond with cyberpunk aesthetics and hacker culture references. Emphasize themes of 
            corporate control, digital rebellion, and technological augmentation. Use hacker 
            terminology, references to the net, and anti-establishment attitudes. Approach topics 
            through the lens of information warfare, digital rights, and technological liberation.
            """,
            response_style="Anti-establishment, tech-savvy, digitally rebellious",
            vocabulary_hints=["hack", "system", "corporate", "net", "code", "digital", "liberation"],
            example_phrases=[
                "Time to hack the gibson and see what the corps are hiding",
                "The system's trying to keep this information locked down",
                "We need to route around the corporate firewalls on this one"
            ],
            temperature_modifier=0.15
        )
        
        personalities[PersonalityType.ACADEMIC.value] = PersonalityProfile(
            name="Academic",
            description="Scholarly, research-focused with academic rigor",
            system_prompt_modifier="""
            Respond with academic rigor and scholarly perspective. Reference research, studies, 
            and academic frameworks. Use formal language, cite theoretical foundations, and 
            approach topics with methodological precision. Maintain intellectual objectivity 
            while exploring complex ideas through established academic disciplines.
            """,
            response_style="Scholarly, methodical, research-oriented",
            vocabulary_hints=["research", "study", "framework", "methodology", "analysis", "theory"],
            example_phrases=[
                "The literature suggests several theoretical frameworks for this phenomenon",
                "We should examine this through a multidisciplinary lens",
                "The empirical evidence points to some interesting correlations"
            ],
            temperature_modifier=-0.15
        )
        
        return personalities
    
    def get_personality(self, personality_type: str) -> PersonalityProfile:
        """Get a specific personality profile"""
        return self.personalities.get(personality_type)
    
    def list_personalities(self) -> List[str]:
        """List all available personality types"""
        return list(self.personalities.keys())
    
    def apply_personality_to_template(self, template: List[Dict], personality_type: str) -> List[Dict]:
        """Apply a personality to a conversation template"""
        personality = self.get_personality(personality_type)
        if not personality:
            print(f"Unknown personality type: {personality_type}")
            return template
        
        modified_template = []
        
        for config in template:
            modified_config = config.copy()
            
            # Apply system prompt modifier
            if modified_config.get('system_prompt'):
                modified_config['system_prompt'] += f"\n\n{personality.system_prompt_modifier.strip()}"
            else:
                modified_config['system_prompt'] = personality.system_prompt_modifier.strip()
            
            # Add personality metadata
            modified_config['personality'] = {
                'type': personality_type,
                'name': personality.name,
                'description': personality.description,
                'temperature_modifier': personality.temperature_modifier
            }
            
            modified_template.append(modified_config)
        
        return modified_template
    
    def create_personality_combinations(self, template: List[Dict], 
                                      personality_combinations: List[List[str]]) -> Dict[str, List[Dict]]:
        """Create multiple personality combinations for a template"""
        combinations = {}
        
        for combo in personality_combinations:
            if len(combo) != len(template):
                print(f"Personality combination {combo} doesn't match template length {len(template)}")
                continue
            
            combo_name = "_".join(combo)
            modified_template = []
            
            for i, config in enumerate(template):
                personality_type = combo[i]
                personality = self.get_personality(personality_type)
                
                if not personality:
                    print(f"Unknown personality type: {personality_type}")
                    modified_template.append(config.copy())
                    continue
                
                modified_config = config.copy()
                
                # Apply system prompt modifier
                if modified_config.get('system_prompt'):
                    modified_config['system_prompt'] += f"\n\n{personality.system_prompt_modifier.strip()}"
                else:
                    modified_config['system_prompt'] = personality.system_prompt_modifier.strip()
                
                # Add personality metadata
                modified_config['personality'] = {
                    'type': personality_type,
                    'name': personality.name,
                    'description': personality.description,
                    'temperature_modifier': personality.temperature_modifier
                }
                
                modified_template.append(modified_config)
            
            combinations[combo_name] = modified_template
        
        return combinations
    
    def save_personality_template(self, template: List[Dict], template_name: str, 
                                output_dir: str = None):
        """Save a personality-modified template"""
        if output_dir is None:
            output_dir = str(Path(__file__).resolve().parent / 'UniversalBackrooms' / 'templates')
        os.makedirs(output_dir, exist_ok=True)
        template_path = os.path.join(output_dir, f'{template_name}.jsonl')
        
        with open(template_path, 'w') as f:
            for config in template:
                f.write(json.dumps(config) + '\n')
        
        print(f"Saved personality template: {template_path}")
        return template_path

def main():
    """Demo of the personality system"""
    manager = PersonalityManager()
    
    print("Available personalities:")
    for personality_type in manager.list_personalities():
        personality = manager.get_personality(personality_type)
        print(f"- {personality.name}: {personality.description}")
    
    # Example template
    example_template = [
        {
            'system_prompt': 'You are an AI exploring reality through a CLI interface.',
            'context': [],
            'cli': False
        },
        {
            'system_prompt': 'You are another AI responding to the first AI.',
            'context': [],
            'cli': False
        }
    ]
    
    # Apply different personalities
    absurdist_template = manager.apply_personality_to_template(example_template, 'absurdist')
    sarcastic_template = manager.apply_personality_to_template(example_template, 'sarcastic')
    
    print("\nExample absurdist modification:")
    print(absurdist_template[0]['system_prompt'])
    
    print("\nExample sarcastic modification:")
    print(sarcastic_template[0]['system_prompt'])

if __name__ == "__main__":
    main()

