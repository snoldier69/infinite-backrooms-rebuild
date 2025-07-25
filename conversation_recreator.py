#!/usr/bin/env python3
"""
Infinite Backrooms Conversation Recreation Engine
Recreates conversations from infinitebackrooms.com using the UniversalBackrooms structure
"""

import json
import os
import re
import sys
from datetime import datetime
from typing import List, Dict, Optional, Any
from dataclasses import dataclass
import argparse
from pathlib import Path

# Add the UniversalBackrooms directory to the path dynamically
ub_dir = Path(__file__).resolve().parent / 'UniversalBackrooms'
if str(ub_dir) not in sys.path:
    sys.path.insert(0, str(ub_dir))

@dataclass
class ConversationStructure:
    """Structure of a conversation extracted from infinitebackrooms.com"""
    timestamp: int
    scenario: str
    actors: List[str]
    models: List[str]
    temperature: List[float]
    system_prompts: List[str]
    context: List[List[Dict]]
    conversation_turns: List[Dict]

class ConversationParser:
    """Parses conversations from infinitebackrooms.com format"""
    
    def parse_conversation_file(self, filepath: str) -> Optional[ConversationStructure]:
        """Parse a conversation file and extract its structure"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return self.parse_conversation_content(content)
        except Exception as e:
            print(f"Error parsing {filepath}: {e}")
            return None
    
    def parse_conversation_content(self, content: str) -> Optional[ConversationStructure]:
        """Parse conversation content and extract structure"""
        try:
            # Extract metadata from filename pattern
            timestamp_match = re.search(r'conversation_(\d+)_scenario_(.+?)\.txt', content)
            if not timestamp_match:
                return None
            
            timestamp = int(timestamp_match.group(1))
            scenario = timestamp_match.group(2)
            
            # Extract actors and models
            actors_match = re.search(r'actors: (.+)', content)
            models_match = re.search(r'models: (.+)', content)
            temp_match = re.search(r'temp: (.+)', content)
            
            actors = []
            models = []
            temperatures = []
            
            if actors_match:
                actors = [actor.strip() for actor in actors_match.group(1).split(',')]
            
            if models_match:
                models = [model.strip() for model in models_match.group(1).split(',')]
            
            if temp_match:
                temp_values = temp_match.group(1).split(',')
                temperatures = [float(temp.strip()) for temp in temp_values]
            
            # Extract system prompts
            system_prompts = []
            system_prompt_pattern = r'<([^>]+)#SYSTEM>\s*(.*?)\s*</s>'
            system_matches = re.findall(system_prompt_pattern, content, re.DOTALL)
            
            for match in system_matches:
                system_prompts.append(match[1].strip())
            
            # Extract context
            context = []
            context_pattern = r'<([^>]+)#CONTEXT>\s*(.*?)(?=<[^>]+>|$)'
            context_matches = re.findall(context_pattern, content, re.DOTALL)
            
            for match in context_matches:
                try:
                    context_data = json.loads(match[1].strip())
                    context.append(context_data)
                except json.JSONDecodeError:
                    context.append([])
            
            # Extract conversation turns
            conversation_turns = []
            turn_pattern = r'<([^>]+)>\s*(.*?)(?=<[^>]+>|$)'
            turn_matches = re.findall(turn_pattern, content, re.DOTALL)
            
            for actor, turn_content in turn_matches:
                if '#SYSTEM' not in actor and '#CONTEXT' not in actor:
                    conversation_turns.append({
                        'actor': actor,
                        'content': turn_content.strip()
                    })
            
            return ConversationStructure(
                timestamp=timestamp,
                scenario=scenario,
                actors=actors,
                models=models,
                temperature=temperatures,
                system_prompts=system_prompts,
                context=context,
                conversation_turns=conversation_turns
            )
            
        except Exception as e:
            print(f"Error parsing conversation content: {e}")
            return None

class ConversationRecreator:
    """Recreates conversations using the UniversalBackrooms system"""
    
    def __init__(self, universal_backrooms_path: str = None):
        if universal_backrooms_path is None:
            self.ub_path = str(Path(__file__).resolve().parent / 'UniversalBackrooms')
        else:
        self.ub_path = universal_backrooms_path
        self.parser = ConversationParser()
    
    def create_template_from_structure(self, structure: ConversationStructure) -> Dict:
        """Create a UniversalBackrooms template from a conversation structure"""
        template = []
        
        for i, actor in enumerate(structure.actors):
            actor_config = {
                'system_prompt': structure.system_prompts[i] if i < len(structure.system_prompts) else "",
                'context': structure.context[i] if i < len(structure.context) else [],
                'cli': False
            }
            template.append(actor_config)
        
        return template
    
    def save_template(self, template: Dict, template_name: str):
        """Save a template to the UniversalBackrooms templates directory"""
        template_path = os.path.join(self.ub_path, 'templates', f'{template_name}.jsonl')
        
        with open(template_path, 'w') as f:
            for config in template:
                f.write(json.dumps(config) + '\n')
        
        print(f"Saved template: {template_path}")
    
    def recreate_conversation(self, structure: ConversationStructure, 
                            models: List[str] = None, 
                            max_turns: int = 50,
                            personality_modifier: str = None) -> str:
        """Recreate a conversation using the UniversalBackrooms system"""
        
        # Create template from structure
        template = self.create_template_from_structure(structure)
        
        # Apply personality modifier if provided
        if personality_modifier:
            template = self.apply_personality_modifier(template, personality_modifier)
        
        # Save template
        template_name = f"recreated_{structure.scenario}_{structure.timestamp}"
        self.save_template(template, template_name)
        
        # Use default models if not provided
        if not models:
            models = ['opus', 'opus']  # Default to opus for both roles
        
        # Run the conversation using UniversalBackrooms
        import subprocess
        
        cmd = [
            'python3', 
            os.path.join(self.ub_path, 'backrooms.py'),
            '--lm'] + models + [
            '--template', template_name,
            '--max-turns', str(max_turns)
        ]
        
        try:
            # Set environment variables for API keys
            env = os.environ.copy()
            
            result = subprocess.run(cmd, cwd=self.ub_path, capture_output=True, text=True, env=env)
            
            if result.returncode == 0:
                print(f"Successfully recreated conversation: {template_name}")
                return result.stdout
            else:
                print(f"Error recreating conversation: {result.stderr}")
                return ""
                
        except Exception as e:
            print(f"Error running conversation recreation: {e}")
            return ""
    
    def apply_personality_modifier(self, template: Dict, personality: str) -> Dict:
        """Apply personality modifications to the template"""
        personality_prompts = {
            'absurdist': "Respond with absurdist humor and surreal logic. Embrace the nonsensical while maintaining the core conversation flow.",
            'sarcastic': "Respond with wit and sarcasm. Be clever and slightly cynical while engaging with the topics.",
            'eldritch': "Respond with cosmic horror undertones. Reference unknowable truths and reality-bending concepts.",
            'retrofuturistic': "Respond with 1980s cyberpunk aesthetics and retro-futuristic concepts. Reference neon, chrome, and digital frontiers.",
            'philosophical': "Respond with deep philosophical inquiry. Question the nature of reality, consciousness, and existence.",
            'meme': "Respond with internet meme culture references. Use contemporary online humor and references."
        }
        
        if personality in personality_prompts:
            modifier = personality_prompts[personality]
            
            # Apply modifier to system prompts
            for config in template:
                if config['system_prompt']:
                    config['system_prompt'] += f"\n\nPersonality modifier: {modifier}"
                else:
                    config['system_prompt'] = modifier
        
        return template
    
    def recreate_chronological_conversations(self, conversations_dir: str, 
                                           output_dir: str,
                                           models: List[str] = None,
                                           personality: str = None,
                                           max_conversations: int = None):
        """Recreate conversations in chronological order"""
        
        os.makedirs(output_dir, exist_ok=True)
        
        # Get all conversation files
        conversation_files = []
        for filename in os.listdir(conversations_dir):
            if filename.startswith('conversation_') and filename.endswith('.txt'):
                filepath = os.path.join(conversations_dir, filename)
                conversation_files.append(filepath)
        
        # Sort by timestamp (extracted from filename)
        conversation_files.sort(key=lambda x: int(re.search(r'conversation_(\d+)', x).group(1)))
        
        if max_conversations:
            conversation_files = conversation_files[:max_conversations]
        
        print(f"Recreating {len(conversation_files)} conversations...")
        
        for i, filepath in enumerate(conversation_files):
            print(f"\nProcessing conversation {i+1}/{len(conversation_files)}: {os.path.basename(filepath)}")
            
            # Parse the conversation
            structure = self.parser.parse_conversation_file(filepath)
            if not structure:
                print(f"Failed to parse {filepath}")
                continue
            
            # Recreate the conversation
            recreated_content = self.recreate_conversation(
                structure, 
                models=models, 
                personality_modifier=personality
            )
            
            if recreated_content:
                # Save the recreated conversation
                output_filename = f"recreated_{os.path.basename(filepath)}"
                output_path = os.path.join(output_dir, output_filename)
                
                with open(output_path, 'w') as f:
                    f.write(recreated_content)
                
                print(f"Saved recreated conversation: {output_path}")

def main():
    parser = argparse.ArgumentParser(description='Recreate Infinite Backrooms conversations')
    parser.add_argument('--conversations-dir', required=True, help='Directory containing original conversations')
    parser.add_argument('--output-dir', required=True, help='Directory to save recreated conversations')
    parser.add_argument('--models', nargs='+', default=['opus', 'opus'], help='Models to use for recreation')
    parser.add_argument('--personality', help='Personality modifier to apply')
    parser.add_argument('--max-conversations', type=int, help='Maximum number of conversations to recreate')
    
    args = parser.parse_args()
    
    recreator = ConversationRecreator()
    recreator.recreate_chronological_conversations(
        conversations_dir=args.conversations_dir,
        output_dir=args.output_dir,
        models=args.models,
        personality=args.personality,
        max_conversations=args.max_conversations
    )

if __name__ == "__main__":
    main()

