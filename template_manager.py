#!/usr/bin/env python3
"""
Template Manager for UniversalBackrooms
Handles creation, validation, and management of conversation templates with proper placeholder formatting
"""

import json
import os
import re
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class TemplateConfig:
    """Configuration for a single LM in a template"""
    system_prompt: str = ""
    context: List[Dict[str, str]] = None
    cli: bool = False
    
    def __post_init__(self):
        if self.context is None:
            self.context = []

class TemplateManager:
    """Manages conversation templates for UniversalBackrooms"""
    
    def __init__(self, templates_dir: str = None):
        if templates_dir is None:
            self.templates_dir = Path(__file__).resolve().parent / 'UniversalBackrooms' / 'templates'
        else:
        self.templates_dir = Path(templates_dir)
        self.templates_dir.mkdir(exist_ok=True)
        
        # Available placeholders that can be used in templates
        self.available_placeholders = [
            "{lm1_actor}", "{lm2_actor}", "{lm3_actor}", "{lm4_actor}",
            "{lm1_company}", "{lm2_company}", "{lm3_company}", "{lm4_company}",
        ]
    
    def create_template(self, template_name: str, configs: List[TemplateConfig]) -> str:
        """Create a new template file"""
        template_path = self.templates_dir / f"{template_name}.jsonl"
        
        with open(template_path, 'w') as f:
            for config in configs:
                template_obj = {
                    "system_prompt": config.system_prompt,
                    "context": config.context,
                }
                if config.cli:
                    template_obj["cli"] = True
                
                f.write(json.dumps(template_obj) + '\n')
        
        print(f"Created template: {template_path}")
        return str(template_path)
    
    def load_template(self, template_name: str) -> List[TemplateConfig]:
        """Load an existing template"""
        template_path = self.templates_dir / f"{template_name}.jsonl"
        
        if not template_path.exists():
            raise FileNotFoundError(f"Template '{template_name}' not found at {template_path}")
        
        configs = []
        with open(template_path, 'r') as f:
            for line in f:
                if line.strip():
                    data = json.loads(line)
                    config = TemplateConfig(
                        system_prompt=data.get("system_prompt", ""),
                        context=data.get("context", []),
                        cli=data.get("cli", False)
                    )
                    configs.append(config)
        
        return configs
    
    def list_templates(self) -> List[str]:
        """List all available templates"""
        templates = []
        for file in self.templates_dir.glob("*.jsonl"):
            templates.append(file.stem)
        return sorted(templates)
    
    def validate_template(self, template_name: str) -> Dict[str, Any]:
        """Validate a template and return validation results"""
        try:
            configs = self.load_template(template_name)
            
            validation = {
                "valid": True,
                "errors": [],
                "warnings": [],
                "info": {
                    "num_lms": len(configs),
                    "has_cli": any(config.cli for config in configs),
                    "placeholders_used": set()
                }
            }
            
            # Check for placeholders
            for i, config in enumerate(configs):
                text_to_check = config.system_prompt
                for context_msg in config.context:
                    text_to_check += " " + context_msg.get("content", "")
                
                # Find placeholders
                placeholders = re.findall(r'\{[^}]+\}', text_to_check)
                validation["info"]["placeholders_used"].update(placeholders)
                
                # Check for unknown placeholders
                for placeholder in placeholders:
                    if placeholder not in self.available_placeholders:
                        validation["warnings"].append(f"Unknown placeholder '{placeholder}' in LM {i+1}")
            
            validation["info"]["placeholders_used"] = list(validation["info"]["placeholders_used"])
            
            return validation
            
        except Exception as e:
            return {
                "valid": False,
                "errors": [str(e)],
                "warnings": [],
                "info": {}
            }
    
    def create_custom_template_from_existing(self, base_template: str, new_template: str, 
                                           modifications: Dict[int, Dict[str, Any]]) -> str:
        """Create a new template based on an existing one with modifications"""
        configs = self.load_template(base_template)
        
        # Apply modifications
        for lm_index, mods in modifications.items():
            if 0 <= lm_index < len(configs):
                if "system_prompt" in mods:
                    configs[lm_index].system_prompt = mods["system_prompt"]
                if "context" in mods:
                    configs[lm_index].context = mods["context"]
                if "cli" in mods:
                    configs[lm_index].cli = mods["cli"]
        
        return self.create_template(new_template, configs)
    
    def create_template_from_scratch(self, template_name: str, 
                                   system_prompts: List[str],
                                   contexts: List[List[Dict[str, str]]] = None,
                                   cli_flags: List[bool] = None) -> str:
        """Create a template from scratch with basic parameters"""
        if contexts is None:
            contexts = [[] for _ in system_prompts]
        if cli_flags is None:
            cli_flags = [False for _ in system_prompts]
        
        configs = []
        for i, prompt in enumerate(system_prompts):
            config = TemplateConfig(
                system_prompt=prompt,
                context=contexts[i] if i < len(contexts) else [],
                cli=cli_flags[i] if i < len(cli_flags) else False
            )
            configs.append(config)
        
        return self.create_template(template_name, configs)
    
    def add_placeholder_examples(self) -> Dict[str, str]:
        """Return examples of how to use placeholders"""
        return {
            "{lm1_actor}": "Will be replaced with 'Claude 1', 'GPT4o 1', etc.",
            "{lm2_actor}": "Will be replaced with 'Claude 2', 'GPT4o 2', etc.",
            "{lm1_company}": "Will be replaced with 'anthropic', 'openai', etc.",
            "{lm2_company}": "Will be replaced with 'anthropic', 'openai', etc.",
            "Example usage": "Hello {lm1_actor}, I am from {lm2_company}."
        }

def create_example_templates():
    """Create some example templates to demonstrate the system"""
    manager = TemplateManager()
    
    # Example 1: Simple debate template
    debate_prompts = [
        "You are a debater arguing FOR the given topic. Use logical arguments and evidence. Be respectful but firm in your position.",
        "You are a debater arguing AGAINST the given topic. Use logical arguments and evidence. Be respectful but firm in your position."
    ]
    
    debate_contexts = [
        [{"role": "user", "content": "Today's debate topic: 'Artificial Intelligence will ultimately benefit humanity more than it will harm it.' You are arguing FOR this position. Please present your opening statement."}],
        []
    ]
    
    manager.create_template_from_scratch(
        "debate_template",
        debate_prompts,
        debate_contexts
    )
    
    # Example 2: Creative writing collaboration
    creative_prompts = [
        "You are a creative writer specializing in science fiction. You love exploring themes of technology, space, and the future of humanity. Work with {lm2_actor} to create an engaging story.",
        "You are a creative writer specializing in character development and dialogue. You excel at creating compelling characters and realistic conversations. Work with {lm1_actor} to create an engaging story."
    ]
    
    creative_contexts = [
        [{"role": "user", "content": "Let's collaborate on writing a short science fiction story. I'll start us off with a premise, and we can build the story together, taking turns adding scenes and developing characters."}],
        []
    ]
    
    manager.create_template_from_scratch(
        "creative_collaboration",
        creative_prompts,
        creative_contexts
    )
    
    # Example 3: Technical problem solving
    tech_prompts = [
        "You are a senior software engineer with expertise in system architecture. You approach problems methodically and focus on scalable solutions. Work with {lm2_actor} to solve technical challenges.",
        "You are a senior software engineer with expertise in algorithms and optimization. You focus on efficiency and performance. Work with {lm1_actor} to solve technical challenges."
    ]
    
    tech_contexts = [
        [{"role": "user", "content": "We need to design a system for handling real-time data processing at scale. Let's discuss the architecture and implementation approach."}],
        []
    ]
    
    manager.create_template_from_scratch(
        "technical_problem_solving",
        tech_prompts,
        tech_contexts
    )
    
    print("Created example templates: debate_template, creative_collaboration, technical_problem_solving")

def main():
    """Demo of the template manager"""
    manager = TemplateManager()
    
    print("=== Template Manager Demo ===")
    
    # List existing templates
    print("\nExisting templates:")
    for template in manager.list_templates():
        print(f"  - {template}")
    
    # Create example templates
    print("\nCreating example templates...")
    create_example_templates()
    
    # Validate a template
    print("\nValidating CLI template:")
    validation = manager.validate_template("cli")
    print(f"Valid: {validation['valid']}")
    print(f"Number of LMs: {validation['info']['num_lms']}")
    print(f"Placeholders used: {validation['info']['placeholders_used']}")
    
    # Show placeholder examples
    print("\nPlaceholder examples:")
    examples = manager.add_placeholder_examples()
    for placeholder, description in examples.items():
        print(f"  {placeholder}: {description}")

if __name__ == "__main__":
    main()

