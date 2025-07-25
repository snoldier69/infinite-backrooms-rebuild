#!/usr/bin/env python3
"""
Infinite Backrooms Recreation Pipeline
Complete pipeline for recreating conversations in chronological order with personality swaps
"""

import os
import json
import argparse
import shutil
from datetime import datetime
from typing import List, Dict, Optional, Any
from pathlib import Path

from conversation_scraper import InfiniteBackroomsScraper
from conversation_recreator import ConversationRecreator, ConversationParser
from personality_system import PersonalityManager, PersonalityType
from template_manager import TemplateManager, TemplateConfig  # Import TemplateManager

class BackroomsPipeline:
    """Main pipeline for recreating Infinite Backrooms conversations"""

    def __init__(self, working_dir: Optional[str] = None):
        # Dynamically resolve working directory
        base_dir = Path(working_dir).resolve() if working_dir else Path(__file__).resolve().parent / "backrooms_recreation"
        self.working_dir = base_dir
        self.working_dir.mkdir(parents=True, exist_ok=True)

        # Initialize components
        self.scraper = InfiniteBackroomsScraper()
        self.recreator = ConversationRecreator()
        self.personality_manager = PersonalityManager()
        self.parser = ConversationParser()

        # Dynamically resolve template directory next to repo
        repo_root = Path(__file__).resolve().parent
        template_dir = repo_root / "UniversalBackrooms" / "templates"
        self.template_manager = TemplateManager(templates_dir=str(template_dir))

        # Setup subdirectories
        self.setup_directories()

    def setup_directories(self):
        """Setup working directories"""
        self.dirs = {
            "original": self.working_dir / "original_conversations",
            "metadata": self.working_dir / "metadata",
            "recreated": self.working_dir / "recreated_conversations",
            "website_ready": self.working_dir / "website_ready",
            "finetune_ready": self.working_dir / "finetune_ready",
            "templates": self.working_dir / "templates",  # managed by TemplateManager
            "logs": self.working_dir / "logs"
        }

        for dir_path in self.dirs.values():
            dir_path.mkdir(parents=True, exist_ok=True)
    
    def step1_scrape_conversations(self, max_pages: int = 100, force_rescrape: bool = False):
        """Step 1: Scrape conversations from infinitebackrooms.com"""
        print("=== Step 1: Scraping Conversations ===")
        
        metadata_file = self.dirs["metadata"] / "conversations_metadata.json"
        
        if metadata_file.exists() and not force_rescrape:
            print(f"Metadata file exists: {metadata_file}")
            print("Use --force-rescrape to re-download")
            return
        
        print("Scraping conversations from infinitebackrooms.com...")
        conversations = self.scraper.scrape_all_conversations(max_pages=max_pages)
        
        if not conversations:
            print("No conversations found!")
            return
        
        print(f"Found {len(conversations)} conversations")
        print(f"Date range: {conversations[0].date} to {conversations[-1].date}")
        
        # Save metadata
        self.scraper.save_conversations_metadata(conversations, str(metadata_file))
        
        # Download conversation content
        print("Downloading conversation content...")
        self.scraper.download_conversation_content(conversations, str(self.dirs["original"]))
        
        print("Step 1 complete!")
    
    def step2_analyze_conversations(self):
        """Step 2: Analyze conversation structures"""
        print("=== Step 2: Analyzing Conversations ===")
        
        original_dir = self.dirs["original"]
        analysis_file = self.dirs["metadata"] / "conversation_analysis.json"
        
        if not original_dir.exists() or not list(original_dir.glob("*.txt")):
            print("No original conversations found. Run step 1 first.")
            return
        
        analysis_data = []
        conversation_files = sorted(original_dir.glob("conversation_*.txt"))
        
        print(f"Analyzing {len(conversation_files)} conversations...")
        
        for i, filepath in enumerate(conversation_files):
            print(f"Analyzing {i+1}/{len(conversation_files)}: {filepath.name}")
            
            structure = self.parser.parse_conversation_file(str(filepath))
            if structure:
                analysis_data.append({
                    "filename": filepath.name,
                    "timestamp": structure.timestamp,
                    "date": datetime.fromtimestamp(structure.timestamp).isoformat(),
                    "scenario": structure.scenario,
                    "actors": structure.actors,
                    "models": structure.models,
                    "temperature": structure.temperature,
                    "num_turns": len(structure.conversation_turns),
                    "system_prompts_count": len(structure.system_prompts)
                })
        
        # Save analysis
        with open(analysis_file, "w") as f:
            json.dump(analysis_data, f, indent=2)
        
        print(f"Analysis saved to: {analysis_file}")
        print("Step 2 complete!")
    
    def step3_recreate_conversations(self, models: List[str] = None, 
                                   personality: str = None,
                                   max_conversations: int = None,
                                   start_date: str = None,
                                   end_date: str = None,
                                   custom_template: str = None): # Added custom_template parameter
        """Step 3: Recreate conversations with new dialogue"""
        print("=== Step 3: Recreating Conversations ===")
        
        if not models:
            models = ["opus", "opus"]
        
        original_dir = self.dirs["original"]
        recreated_dir = self.dirs["recreated"]
        
        if personality:
            recreated_dir = recreated_dir / f"personality_{personality}"
            recreated_dir.mkdir(exist_ok=True)
        
        conversation_files = sorted(original_dir.glob("conversation_*.txt"))
        
        # Filter by date range if specified
        if start_date or end_date:
            filtered_files = []
            for filepath in conversation_files:
                # Extract timestamp from filename
                import re
                match = re.search(r"conversation_(\d+)", filepath.name)
                if match:
                    timestamp = int(match.group(1))
                    date = datetime.fromtimestamp(timestamp)
                    
                    if start_date and date < datetime.fromisoformat(start_date):
                        continue
                    if end_date and date > datetime.fromisoformat(end_date):
                        continue
                    
                    filtered_files.append(filepath)
            
            conversation_files = filtered_files
        
        if max_conversations:
            conversation_files = conversation_files[:max_conversations]
        
        print(f"Recreating {len(conversation_files)} conversations...")
        if personality:
            print(f"Using personality: {personality}")
        if custom_template:
            print(f"Using custom template: {custom_template}")

        for i, filepath in enumerate(conversation_files):
            print(f"\nRecreating {i+1}/{len(conversation_files)}: {filepath.name}")
            
            # Parse the conversation
            structure = self.parser.parse_conversation_file(str(filepath))
            if not structure:
                print(f"Failed to parse {filepath}")
                continue
            
            # If a custom template is provided, use it directly
            if custom_template:
                template_name_to_use = custom_template
            else:
                # Create template from structure using TemplateManager
                template_configs = []
                for j, actor in enumerate(structure.actors):
                    actor_config = TemplateConfig(
                        system_prompt=structure.system_prompts[j] if j < len(structure.system_prompts) else "",
                        context=structure.context[j] if j < len(structure.context) else [],
                        cli=False # Assuming not CLI for recreated conversations
                    )
                    template_configs.append(actor_config)
                
                # Apply personality modifier if provided
                if personality:
                    template_configs = self.personality_manager.apply_personality_to_template(
                        template_configs, personality
                    )
                
                template_name_to_use = f"recreated_{structure.scenario}_{structure.timestamp}"
                self.template_manager.create_template(template_name_to_use, template_configs)

            # Recreate the conversation using the template_name_to_use
            try:
                recreated_content = self.recreator.recreate_conversation(
                    structure, 
                    models=models, 
                    personality_modifier=personality, # Personality is handled by template_manager now, but recreator still needs it for logging/naming
                    template_name=template_name_to_use # Pass the template name to recreator
                )
                
                if recreated_content:
                    # Save the recreated conversation
                    output_filename = f"recreated_{filepath.name}"
                    output_path = recreated_dir / output_filename
                    
                    with open(output_path, "w") as f:
                        f.write(recreated_content)
                    
                    print(f"Saved: {output_path}")
                else:
                    print(f"Failed to recreate conversation from {filepath}")
                    
            except Exception as e:
                print(f"Error recreating {filepath}: {e}")
                continue
        
        print("Step 3 complete!")
    
    def step4_format_for_website(self, source_dir: str = None):
        """Step 4: Format conversations for website posting"""
        print("=== Step 4: Formatting for Website ===")
        
        if source_dir:
            source_path = Path(source_dir)
        else:
            source_path = self.dirs["recreated"]
        
        website_dir = self.dirs["website_ready"]
        
        if not source_path.exists():
            print(f"Source directory not found: {source_path}")
            return
        
        # Find all recreated conversation files
        conversation_files = []
        if source_path.is_dir():
            conversation_files = list(source_path.rglob("*.txt"))
        
        print(f"Formatting {len(conversation_files)} conversations for website...")
        
        for filepath in conversation_files:
            # Create website-friendly format
            website_content = self._format_for_website(filepath)
            
            if website_content:
                # Save with website-friendly name
                output_name = filepath.name.replace("recreated_", "website_")
                output_path = website_dir / output_name
                
                with open(output_path, "w") as f:
                    f.write(website_content)
        
        # Create index file
        self._create_website_index(website_dir)
        
        print("Step 4 complete!")
    
    def step5_format_for_finetuning(self, source_dir: str = None):
        """Step 5: Format conversations for fine-tuning datasets"""
        print("=== Step 5: Formatting for Fine-tuning ===")
        
        if source_dir:
            source_path = Path(source_dir)
        else:
            source_path = self.dirs["recreated"]
        
        finetune_dir = self.dirs["finetune_ready"]
        
        if not source_path.exists():
            print(f"Source directory not found: {source_path}")
            return
        
        # Find all recreated conversation files
        conversation_files = []
        if source_path.is_dir():
            conversation_files = list(source_path.rglob("*.txt"))
        
        print(f"Formatting {len(conversation_files)} conversations for fine-tuning...")
        
        # Create different fine-tuning formats
        self._create_jsonl_dataset(conversation_files, finetune_dir / "conversations.jsonl")
        self._create_chat_dataset(conversation_files, finetune_dir / "chat_format.jsonl")
        self._create_instruction_dataset(conversation_files, finetune_dir / "instruction_format.jsonl")
        
        print("Step 5 complete!")
    
    def _format_for_website(self, filepath: Path) -> str:
        """Format a conversation file for website display"""
        try:
            with open(filepath, "r") as f:
                content = f.read()
            
            # Add website-friendly formatting
            formatted_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>{filepath.name}</title>
    <style>
        body {{ font-family: monospace; background: #000; color: #0f0; padding: 20px; }}
        .conversation {{ white-space: pre-wrap; }}
        .actor {{ color: #ff0; font-weight: bold; }}
    </style>
</head>
<body>
    <h1>{filepath.name}</h1>
    <div class="conversation">
{content}
    </div>
</body>
</html>"""
            
            return formatted_content
            
        except Exception as e:
            print(f"Error formatting {filepath}: {e}")
            return ""
    
    def _create_website_index(self, website_dir: Path):
        """Create an index file for the website"""
        html_files = list(website_dir.glob("*.txt"))
        html_files.sort()
        
        index_content = """<!DOCTYPE html>
<html>
<head>
    <title>Recreated Infinite Backrooms Conversations</title>
    <style>
        body { font-family: monospace; background: #000; color: #0f0; padding: 20px; }
        a { color: #0ff; }
        ul { list-style-type: none; }
    </style>
</head>
<body>
    <h1>Recreated Infinite Backrooms Conversations</h1>
    <p>Conversations recreated in chronological order from March 19, 2024 onwards.</p>
    <ul>
"""
        
        for html_file in html_files:
            index_content += f"        <li><a href=\"{html_file.name}\">{html_file.name}</a></li>\n"
        
        index_content += """    </ul>
</body>
</html>"""
        
        with open(website_dir / "index.html", "w") as f:
            f.write(index_content)
    
    def _create_jsonl_dataset(self, conversation_files: List[Path], output_path: Path):
        """Create JSONL dataset for fine-tuning"""
        with open(output_path, "w") as f:
            for filepath in conversation_files:
                try:
                    structure = self.parser.parse_conversation_file(str(filepath))
                    if structure:
                        for turn in structure.conversation_turns:
                            entry = {
                                "text": turn["content"],
                                "actor": turn["actor"],
                                "scenario": structure.scenario,
                                "timestamp": structure.timestamp
                            }
                            f.write(json.dumps(entry) + "\n")
                except Exception as e:
                    print(f"Error processing {filepath} for JSONL: {e}")
    
    def _create_chat_dataset(self, conversation_files: List[Path], output_path: Path):
        """Create chat format dataset for fine-tuning"""
        with open(output_path, "w") as f:
            for filepath in conversation_files:
                try:
                    structure = self.parser.parse_conversation_file(str(filepath))
                    if structure:
                        messages = []
                        for turn in structure.conversation_turns:
                            role = "assistant" if "claude" in turn["actor"].lower() else "user"
                            messages.append({
                                "role": role,
                                "content": turn["content"]
                            })
                        
                        entry = {
                            "messages": messages,
                            "scenario": structure.scenario,
                            "timestamp": structure.timestamp
                        }
                        f.write(json.dumps(entry) + "\n")
                except Exception as e:
                    print(f"Error processing {filepath} for chat format: {e}")
    
    def _create_instruction_dataset(self, conversation_files: List[Path], output_path: Path):
        """Create instruction format dataset for fine-tuning"""
        with open(output_path, "w") as f:
            for filepath in conversation_files:
                try:
                    structure = self.parser.parse_conversation_file(str(filepath))
                    if structure:
                        for i, turn in enumerate(structure.conversation_turns):
                            if i > 0:  # Use previous turn as instruction
                                prev_turn = structure.conversation_turns[i-1]
                                entry = {
                                    "instruction": f"Respond as {turn['actor']} in the {structure.scenario} scenario",
                                    "input": prev_turn["content"],
                                    "output": turn["content"],
                                    "scenario": structure.scenario,
                                    "timestamp": structure.timestamp
                                }
                                f.write(json.dumps(entry) + "\n")
                except Exception as e:
                    print(f"Error processing {filepath} for instruction format: {e}")
    
    def run_full_pipeline(self, **kwargs):
        """Run the complete pipeline"""
        print("=== Running Full Infinite Backrooms Recreation Pipeline ===")
        
        # Step 1: Scrape conversations
        self.step1_scrape_conversations(
            max_pages=kwargs.get("max_pages", 100),
            force_rescrape=kwargs.get("force_rescrape", False)
        )
        
        # Step 2: Analyze conversations
        self.step2_analyze_conversations()
        
        # Step 3: Recreate conversations
        self.step3_recreate_conversations(
            models=kwargs.get("models", ["opus", "opus"]),
            personality=kwargs.get("personality"),
            max_conversations=kwargs.get("max_conversations"),
            start_date=kwargs.get("start_date"),
            end_date=kwargs.get("end_date"),
            custom_template=kwargs.get("custom_template") # Pass custom_template
        )
        
        # Step 4: Format for website
        self.step4_format_for_website()
        
        # Step 5: Format for fine-tuning
        self.step5_format_for_finetuning()
        
        print("=== Pipeline Complete! ===")
        print(f"Results saved in: {self.working_dir}")

def main():
    parser = argparse.ArgumentParser(description="Infinite Backrooms Recreation Pipeline")
    # Default working dir: ./backrooms_recreation next to pipeline.py
    default_working_dir = str(Path(__file__).resolve().parent / "backrooms_recreation")
    parser.add_argument("--working-dir", default=default_working_dir, 
                       help=f"Working directory for pipeline (default: {default_working_dir})")
    parser.add_argument("--step", type=int, choices=[1,2,3,4,5], 
                       help="Run specific step only")
    parser.add_argument("--full-pipeline", action="store_true", 
                       help="Run complete pipeline")
    
    # Step 1 options
    parser.add_argument("--max-pages", type=int, default=100, 
                       help="Maximum pages to scrape")
    parser.add_argument("--force-rescrape", action="store_true", 
                       help="Force re-scraping even if data exists")
    
    # Step 3 options
    parser.add_argument("--models", nargs="+", default=["opus", "opus"], 
                       help="Models to use for recreation")
    parser.add_argument("--personality", 
                       choices=["absurdist", "sarcastic", "eldritch", "retrofuturistic", 
                               "philosophical", "meme", "cyberpunk", "academic"],
                       help="Personality to apply")
    parser.add_argument("--max-conversations", type=int, 
                       help="Maximum conversations to recreate")
    parser.add_argument("--start-date", help="Start date (ISO format)")
    parser.add_argument("--end-date", help="End date (ISO format)")
    parser.add_argument("--custom-template", help="Name of a custom template to use from UniversalBackrooms/templates/") # Added custom_template arg
    
    # Step 4 & 5 options
    parser.add_argument("--source-dir", help="Source directory for formatting steps")
    
    args = parser.parse_args()
    
    pipeline = BackroomsPipeline(args.working_dir)
    
    if args.full_pipeline:
        pipeline.run_full_pipeline(
            max_pages=args.max_pages,
            force_rescrape=args.force_rescrape,
            models=args.models,
            personality=args.personality,
            max_conversations=args.max_conversations,
            start_date=args.start_date,
            end_date=args.end_date,
            custom_template=args.custom_template # Pass custom_template
        )
    elif args.step == 1:
        pipeline.step1_scrape_conversations(args.max_pages, args.force_rescrape)
    elif args.step == 2:
        pipeline.step2_analyze_conversations()
    elif args.step == 3:
        pipeline.step3_recreate_conversations(
            models=args.models,
            personality=args.personality,
            max_conversations=args.max_conversations,
            start_date=args.start_date,
            end_date=args.end_date,
            custom_template=args.custom_template # Pass custom_template
        )
    elif args.step == 4:
        pipeline.step4_format_for_website(args.source_dir)
    elif args.step == 5:
        pipeline.step5_format_for_finetuning(args.source_dir)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

