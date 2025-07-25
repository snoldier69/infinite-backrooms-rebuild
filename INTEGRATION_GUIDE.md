# Integration Guide: How the Recreation System Works with backrooms.py

This guide explains how the Infinite Backrooms Recreation System integrates with and utilizes the original `backrooms.py` from the UniversalBackrooms repository.

## System Architecture Overview

The recreation system is designed as a **wrapper and orchestrator** around the existing `backrooms.py`, not a replacement. Here's how the components work together:

```
┌─────────────────────────────────────────────────────────────────┐
│                    Recreation System                            │
├─────────────────────────────────────────────────────────────────┤
│  conversation_scraper.py  │  Scrapes infinitebackrooms.com     │
│  conversation_parser.py   │  Extracts conversation structure   │
│  personality_system.py    │  Applies personality modifications │
│  pipeline.py             │  Orchestrates the entire workflow  │
└─────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                 UniversalBackrooms                              │
├─────────────────────────────────────────────────────────────────┤
│  backrooms.py            │  Core conversation engine           │
│  templates/*.jsonl       │  Conversation templates             │
└─────────────────────────────────────────────────────────────────┘
```

## How Integration Works

### 1. Template Generation

The recreation system analyzes original conversations and creates **new templates** for `backrooms.py`:

```python
# conversation_recreator.py creates templates like this:
def create_template_from_structure(self, structure: ConversationStructure) -> Dict:
    template = []
    
    for i, actor in enumerate(structure.actors):
        actor_config = {
            'system_prompt': structure.system_prompts[i] if i < len(structure.system_prompts) else "",
            'context': structure.context[i] if i < len(structure.context) else [],
            'cli': False
        }
        template.append(actor_config)
    
    return template
```

### 2. Template Saving

Templates are saved in the format expected by `backrooms.py`:

```python
def save_template(self, template: Dict, template_name: str):
    template_path = os.path.join(self.ub_path, 'templates', f'{template_name}.jsonl')
    
    with open(template_path, 'w') as f:
        for config in template:
            f.write(json.dumps(config) + '\n')  # JSONL format
```

### 3. Calling backrooms.py

The recreation system then calls `backrooms.py` with the generated template:

```python
def recreate_conversation(self, structure: ConversationStructure, 
                        models: List[str] = None, 
                        max_turns: int = 50,
                        personality_modifier: str = None) -> str:
    
    # Create and save template
    template = self.create_template_from_structure(structure)
    if personality_modifier:
        template = self.apply_personality_modifier(template, personality_modifier)
    
    template_name = f"recreated_{structure.scenario}_{structure.timestamp}"
    self.save_template(template, template_name)
    
    # Call backrooms.py
    cmd = [
        'python3', 
        os.path.join(self.ub_path, 'backrooms.py'),
        '--lm'] + models + [
        '--template', template_name,
        '--max-turns', str(max_turns)
    ]
    
    result = subprocess.run(cmd, cwd=self.ub_path, capture_output=True, text=True, env=env)
    return result.stdout
```

## Understanding backrooms.py Integration Points

### 1. Command Line Interface

`backrooms.py` accepts these arguments that our system uses:

- `--lm`: Model selection (opus, sonnet, gpt4o, o1-preview, o1-mini, cli)
- `--template`: Template name (our system generates these)
- `--max-turns`: Maximum conversation turns

### 2. Template Format

`backrooms.py` expects templates in JSONL format where each line is a JSON object:

```json
{"system_prompt": "You are an AI...", "context": [{"role": "user", "content": "Hello"}], "cli": false}
{"system_prompt": "You are another AI...", "context": [], "cli": false}
```

### 3. Model Handling

`backrooms.py` handles different model types:

```python
# From backrooms.py
MODEL_INFO = {
    "sonnet": {"api_name": "claude-3-5-sonnet-20240620", "company": "anthropic"},
    "opus": {"api_name": "claude-3-opus-20240229", "company": "anthropic"},
    "gpt4o": {"api_name": "gpt-4o-2024-08-06", "company": "openai"},
    "o1-preview": {"api_name": "o1-preview", "company": "openai"},
    "o1-mini": {"api_name": "o1-mini", "company": "openai"},
}
```

## Step-by-Step Integration Process

### Step 1: Parse Original Conversation

```python
# Extract structure from infinitebackrooms.com conversation
structure = parser.parse_conversation_file('conversation_1714479738_scenario_vanilla_backrooms.txt')

# Results in:
# structure.actors = ['claude-explorer', 'claude-responder']
# structure.models = ['claude-3-opus-20240229', 'claude-3-opus-20240229']
# structure.system_prompts = ['You are in CLI mode...', 'You are in CLI mode...']
# structure.context = [[{"role": "user", "content": "ls -la"}], []]
```

### Step 2: Create Template

```python
# Convert to backrooms.py template format
template = [
    {
        "system_prompt": "You are in CLI mode...",
        "context": [{"role": "user", "content": "ls -la"}],
        "cli": False
    },
    {
        "system_prompt": "You are in CLI mode...",
        "context": [],
        "cli": False
    }
]
```

### Step 3: Apply Personality (Optional)

```python
# Add personality modifier to system prompts
if personality == 'absurdist':
    for config in template:
        config['system_prompt'] += "\n\nPersonality modifier: Respond with absurdist humor..."
```

### Step 4: Save Template

```python
# Save as JSONL file in UniversalBackrooms/templates/
with open('templates/recreated_vanilla_backrooms_1714479738.jsonl', 'w') as f:
    for config in template:
        f.write(json.dumps(config) + '\n')
```

### Step 5: Execute backrooms.py

```bash
# Our system runs this command:
python3 backrooms.py \
  --lm opus opus \
  --template recreated_vanilla_backrooms_1714479738 \
  --max-turns 50
```

### Step 6: Capture Output

`backrooms.py` generates conversation output and saves it to `BackroomsLogs/`. Our system captures this output and processes it further.

## Key Integration Benefits

### 1. Preserves Original Functionality

- Uses `backrooms.py` exactly as designed
- No modifications to core conversation engine
- Maintains all model compatibility

### 2. Extends Capabilities

- Adds conversation scraping
- Provides structure analysis
- Enables personality modifications
- Offers multiple output formats

### 3. Maintains Compatibility

- Works with all supported models
- Respects API key configuration
- Uses standard template format

## Environment Setup for Integration

### 1. Directory Structure

```
project/
├── UniversalBackrooms/           # Original repository
│   ├── backrooms.py             # Core engine
│   ├── templates/               # Template directory
│   └── BackroomsLogs/          # Output logs
├── conversation_scraper.py      # Our scraper
├── conversation_recreator.py    # Our recreator
├── personality_system.py        # Our personality system
└── pipeline.py                 # Our orchestrator
```

### 2. Environment Variables

Both systems share the same environment variables:

```bash
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
```

### 3. Dependencies

Our system uses the same dependencies as `backrooms.py`:

```bash
pip install -r UniversalBackrooms/requirements.txt
```

## Practical Usage Examples

### Example 1: Basic Integration

```bash
# Our system does this automatically:
python3 pipeline.py --step 3 --models opus sonnet --max-conversations 5

# Which internally:
# 1. Parses original conversations
# 2. Creates templates in UniversalBackrooms/templates/
# 3. Calls: python3 backrooms.py --lm opus sonnet --template recreated_scenario_timestamp
# 4. Captures and processes output
```

### Example 2: Personality Integration

```bash
# With personality modification:
python3 pipeline.py --step 3 --personality absurdist --models opus opus

# Which:
# 1. Applies absurdist personality to system prompts
# 2. Saves modified template
# 3. Calls backrooms.py with modified template
```

### Example 3: Manual Integration

You can also use the components separately:

```python
# Create template manually
from conversation_recreator import ConversationRecreator
recreator = ConversationRecreator()

# Parse a conversation
structure = recreator.parser.parse_conversation_file('original_conversation.txt')

# Create template
template = recreator.create_template_from_structure(structure)
recreator.save_template(template, 'my_custom_template')

# Run backrooms.py manually
import subprocess
result = subprocess.run([
    'python3', 'UniversalBackrooms/backrooms.py',
    '--lm', 'opus', 'sonnet',
    '--template', 'my_custom_template',
    '--max-turns', '20'
], capture_output=True, text=True)
```

## Troubleshooting Integration Issues

### Issue 1: Template Not Found

```
Error: Template 'recreated_scenario_123456' not found.
```

**Solution:** Ensure the template was saved correctly:

```python
# Check if template exists
import os
template_path = 'UniversalBackrooms/templates/recreated_scenario_123456.jsonl'
if not os.path.exists(template_path):
    print("Template not created properly")
```

### Issue 2: Model Mismatch

```
Error: Model 'custom_model' not found in MODEL_INFO.
```

**Solution:** Use only supported models:

```python
supported_models = ['opus', 'sonnet', 'gpt4o', 'o1-preview', 'o1-mini', 'cli']
```

### Issue 3: API Key Issues

```
Error: ANTHROPIC_API_KEY must be set in the environment
```

**Solution:** Ensure environment variables are set:

```bash
# Check if keys are set
echo $ANTHROPIC_API_KEY
echo $OPENAI_API_KEY

# Set if missing
export ANTHROPIC_API_KEY=sk-ant-...
export OPENAI_API_KEY=sk-...
```

## Summary

The recreation system is designed to **enhance and extend** `backrooms.py` rather than replace it. It:

1. **Analyzes** original conversations from infinitebackrooms.com
2. **Extracts** their structure and metadata
3. **Creates** new templates in the format expected by `backrooms.py`
4. **Applies** personality modifications to system prompts
5. **Calls** `backrooms.py` with the generated templates
6. **Processes** the output into multiple formats

This approach ensures compatibility with the original system while adding powerful new capabilities for conversation recreation and personality modification.

