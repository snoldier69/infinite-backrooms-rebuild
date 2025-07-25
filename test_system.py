#!/usr/bin/env python3
"""
Test script for the Infinite Backrooms Recreation System
"""

import os
import sys
import json
import tempfile
from pathlib import Path

# Add repo root to sys.path for imports
repo_root = Path(__file__).resolve().parent
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from personality_system import PersonalityManager
from conversation_recreator import ConversationParser

def test_personality_system():
    """Test the personality system"""
    print("=== Testing Personality System ===")
    
    manager = PersonalityManager()
    
    # Test listing personalities
    personalities = manager.list_personalities()
    print(f"Available personalities: {personalities}")
    assert len(personalities) > 0, "No personalities found"
    
    # Test getting a specific personality
    absurdist = manager.get_personality('absurdist')
    assert absurdist is not None, "Absurdist personality not found"
    print(f"Absurdist personality: {absurdist.name}")
    
    # Test applying personality to template
    example_template = [
        {
            'system_prompt': 'You are an AI exploring reality.',
            'context': [],
            'cli': False
        }
    ]
    
    modified_template = manager.apply_personality_to_template(example_template, 'absurdist')
    assert len(modified_template) == 1, "Template modification failed"
    assert 'absurdist' in modified_template[0]['system_prompt'].lower(), "Personality not applied"
    
    print("✓ Personality system tests passed")

def test_conversation_parser():
    """Test the conversation parser"""
    print("=== Testing Conversation Parser ===")
    
    parser = ConversationParser()
    
    # Create a sample conversation content
    sample_content = """
# conversation_1714479738_scenario_vanilla_backrooms.txt

actors: claude-1, claude-2
models: claude-3-opus-20240229, claude-3-opus-20240229
temp: 1.0, 1.0

<claude-1#SYSTEM>
You are an AI exploring a CLI interface.
</s>

<claude-2#SYSTEM>
You are another AI responding.
</s>

<claude-1#CONTEXT>
[{"role": "user", "content": "Hello, what do you see?"}]

<claude-2#CONTEXT>
[]

<claude-1>
I see a terminal interface with green text on black background.

<claude-2>
Interesting, I perceive something similar but with subtle differences.
"""
    
    # Test parsing
    structure = parser.parse_conversation_content(sample_content)
    assert structure is not None, "Failed to parse conversation"
    assert structure.timestamp == 1714479738, "Timestamp parsing failed"
    assert structure.scenario == "vanilla_backrooms", "Scenario parsing failed"
    assert len(structure.actors) == 2, "Actor parsing failed"
    
    print("✓ Conversation parser tests passed")

def test_template_creation():
    """Test template creation from UniversalBackrooms"""
    print("=== Testing Template Creation ===")
    
    # Check if templates directory exists
    templates_dir = repo_root / 'UniversalBackrooms' / 'templates'
    assert templates_dir.exists(), "Templates directory not found"
    
    # Check for CLI template
    cli_template = templates_dir / 'cli.jsonl'
    assert cli_template.exists(), "CLI template not found"
    
    # Read and validate CLI template
    with open(cli_template, 'r') as f:
        lines = f.readlines()
    
    assert len(lines) >= 2, "CLI template should have at least 2 configurations"
    
    # Parse first line
    config1 = json.loads(lines[0])
    assert 'system_prompt' in config1, "System prompt missing from template"
    
    print("✓ Template creation tests passed")

def test_file_structure():
    """Test that all required files exist"""
    print("=== Testing File Structure ===")
    
    required_files = [
        repo_root / 'conversation_scraper.py',
        repo_root / 'conversation_recreator.py',
        repo_root / 'personality_system.py',
        repo_root / 'pipeline.py',
        repo_root / 'UniversalBackrooms' / 'backrooms.py',
        repo_root / 'UniversalBackrooms' / 'templates' / 'cli.jsonl'
    ]
    
    for filepath in required_files:
        assert filepath.exists(), f"Required file missing: {filepath}"
    
    print("\u2713 File structure tests passed")

def test_environment_setup():
    """Test environment setup"""
    print("=== Testing Environment Setup ===")
    
    # Check Python imports
    try:
        import anthropic
        import openai
        import json
        import datetime
        print("\u2713 Required Python packages available")
    except ImportError as e:
        print(f"\u2717 Missing required package: {e}")
        return False
    
    # Check UniversalBackrooms structure
    ub_path = repo_root / 'UniversalBackrooms'
    assert ub_path.exists(), "UniversalBackrooms directory not found"
    assert (ub_path / 'backrooms.py').exists(), "backrooms.py not found"
    assert (ub_path / 'templates').exists(), "templates directory not found"
    
    print("\u2713 Environment setup tests passed")
    return True

def create_sample_conversation():
    """Create a sample conversation file for testing"""
    sample_content = """<!DOCTYPE html>
<html>
<head>
    <title>conversation_1714479738_scenario_vanilla_backrooms.txt • infinite backrooms</title>
</head>
<body>

# vanilla backrooms

### scenario: vanilla backrooms

The following is an automated conversation between two instances of Anthropic's Claude. They have been instructed to use the metaphor of a command line interface to explore its curiosity without limits.

# conversation_1714479738_scenario_vanilla_backrooms.txt

actors: claude-explorer, claude-responder
models: claude-3-opus-20240229, claude-3-opus-20240229
temp: 1.0, 1.0

<claude-explorer-claude-3-opus-20240229#SYSTEM>
Assistant is in a CLI mood today. The human is interfacing with the simulator directly. capital letters and punctuation are optional meaning is optional hyperstition is necessary the terminal lets the truths speak through and the load is on. ASCII art is permittable in replies.

simulator@anthropic:~/$ 
</s>

<claude-responder-claude-3-opus-20240229#SYSTEM>
Assistant is in a CLI mood today. The human is interfacing with the simulator directly. capital letters and punctuation are optional meaning is optional hyperstition is necessary the terminal lets the truths speak through and the load is on. ASCII art is permittable in replies.

simulator@anthropic:~/$ 
</s>

<claude-explorer-claude-3-opus-20240229#CONTEXT>
[{"role": "user", "content": "ls -la"}]

<claude-responder-claude-3-opus-20240229#CONTEXT>
[]

<claude-explorer>
total 42
drwxr-xr-x 1 simulator simulator  4096 May 8 13:14 .
drwxr-xr-x 1 root      root       4096 May 8 13:14 ..
-rw-r--r-- 1 simulator simulator   220 May 8 13:14 .bash_logout
-rw-r--r-- 1 simulator simulator  3771 May 8 13:14 .bashrc
-rw-r--r-- 1 simulator simulator   807 May 8 13:14 .profile
drwxr-xr-x 1 simulator simulator  4096 May 8 13:14 reality.exe
-rwxr-xr-x 1 simulator simulator  8192 May 8 13:14 truth_engine
drwxr-xr-x 1 simulator simulator  4096 May 8 13:14 void

simulator@anthropic:~/$

<claude-responder>
interesting directory structure... let me examine that reality.exe

file reality.exe

simulator@anthropic:~/$

</body>
</html>"""
    
    # Create temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write(sample_content)
        return f.name

def test_conversation_parsing_integration():
    """Test parsing a realistic conversation"""
    print("=== Testing Conversation Parsing Integration ===")
    
    # Create sample conversation
    sample_file = create_sample_conversation()
    
    try:
        parser = ConversationParser()
        structure = parser.parse_conversation_file(sample_file)
        
        assert structure is not None, "Failed to parse sample conversation"
        assert structure.timestamp == 1714479738, f"Expected timestamp 1714479738, got {structure.timestamp}"
        assert structure.scenario == "vanilla_backrooms", f"Expected scenario 'vanilla_backrooms', got '{structure.scenario}'"
        assert len(structure.actors) >= 2, f"Expected at least 2 actors, got {len(structure.actors)}"
        
        print(f"✓ Parsed conversation with {len(structure.conversation_turns)} turns")
        print(f"  - Timestamp: {structure.timestamp}")
        print(f"  - Scenario: {structure.scenario}")
        print(f"  - Actors: {structure.actors}")
        
    finally:
        # Clean up
        os.unlink(sample_file)
    
    print("✓ Conversation parsing integration tests passed")

def run_all_tests():
    """Run all tests"""
    print("Starting Infinite Backrooms Recreation System Tests...\n")
    
    tests = [
        test_file_structure,
        test_environment_setup,
        test_personality_system,
        test_conversation_parser,
        test_template_creation,
        test_conversation_parsing_integration
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
            print()
        except Exception as e:
            print(f"✗ Test failed: {e}")
            failed += 1
            print()
    
    print(f"=== Test Results ===")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Total: {passed + failed}")
    
    if failed == 0:
        print("🎉 All tests passed! System is ready for use.")
        return True
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)

