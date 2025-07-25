# Usage Examples for Infinite Backrooms Recreation System

This document provides comprehensive examples of how to use the Infinite Backrooms Recreation System for various scenarios and use cases.

## Table of Contents

1. [Basic Recreation Examples](#basic-recreation-examples)
2. [Personality Swap Examples](#personality-swap-examples)
3. [Model Combination Examples](#model-combination-examples)
4. [Output Format Examples](#output-format-examples)
5. [Advanced Workflow Examples](#advanced-workflow-examples)
6. [Batch Processing Examples](#batch-processing-examples)
7. [Custom Integration Examples](#custom-integration-examples)

## Basic Recreation Examples

### Example 1: Simple Recreation with Default Settings

Recreate 10 conversations using default Opus models:

```bash
python3 pipeline.py --full-pipeline --max-conversations 10
```

**Expected Output:**
- Original conversations scraped to `backrooms_recreation/original_conversations/`
- Recreated conversations in `backrooms_recreation/recreated_conversations/`
- Website-ready HTML files in `backrooms_recreation/website_ready/`
- Fine-tuning datasets in `backrooms_recreation/finetune_ready/`

### Example 2: Step-by-Step Recreation

Run each step individually for better control:

```bash
# Step 1: Scrape conversations
python3 pipeline.py --step 1 --max-pages 20

# Step 2: Analyze structures
python3 pipeline.py --step 2

# Step 3: Recreate conversations
python3 pipeline.py --step 3 --max-conversations 5

# Step 4: Format for website
python3 pipeline.py --step 4

# Step 5: Format for fine-tuning
python3 pipeline.py --step 5
```

### Example 3: Date Range Recreation

Recreate conversations from a specific time period:

```bash
python3 pipeline.py --step 3 \
  --start-date 2024-03-19 \
  --end-date 2024-04-19 \
  --max-conversations 20
```

## Personality Swap Examples

### Example 4: Absurdist Personality

Create surreal, paradoxical conversations:

```bash
python3 pipeline.py --step 3 \
  --personality absurdist \
  --max-conversations 10 \
  --models opus opus
```

**Sample Output Characteristics:**
- Paradoxical reasoning
- Dreamlike scenarios
- Unexpected connections
- Playful confusion about reality

### Example 5: Sarcastic Personality

Generate witty, cynical conversations:

```bash
python3 pipeline.py --step 3 \
  --personality sarcastic \
  --max-conversations 10 \
  --models sonnet sonnet
```

**Sample Output Characteristics:**
- Ironic observations
- Subtle mockery
- Sardonic humor
- Intelligent skepticism

### Example 6: Eldritch Horror Personality

Create cosmic horror-themed conversations:

```bash
python3 pipeline.py --step 3 \
  --personality eldritch \
  --max-conversations 5 \
  --models opus gpt4o
```

**Sample Output Characteristics:**
- References to unknowable truths
- Cosmic horror undertones
- Reality-bending concepts
- Existential dread

### Example 7: Cyberpunk Personality

Generate hacker culture conversations:

```bash
python3 pipeline.py --step 3 \
  --personality cyberpunk \
  --max-conversations 8 \
  --models sonnet o1-preview
```

**Sample Output Characteristics:**
- Anti-establishment attitudes
- Hacker terminology
- Corporate paranoia
- Digital rebellion themes

## Model Combination Examples

### Example 8: Claude vs GPT-4o

Create conversations between different AI families:

```bash
python3 pipeline.py --step 3 \
  --models opus gpt4o \
  --max-conversations 5 \
  --personality philosophical
```

### Example 9: Sonnet vs O1-Preview

Combine different reasoning approaches:

```bash
python3 pipeline.py --step 3 \
  --models sonnet o1-preview \
  --max-conversations 3 \
  --personality academic
```

### Example 10: Multi-Model Comparison

Create the same conversation with different model combinations:

```bash
# Version 1: Opus vs Opus
python3 pipeline.py --step 3 \
  --models opus opus \
  --max-conversations 5 \
  --personality meme

# Version 2: Sonnet vs GPT-4o
python3 pipeline.py --step 3 \
  --models sonnet gpt4o \
  --max-conversations 5 \
  --personality meme

# Version 3: O1-Preview vs O1-Mini
python3 pipeline.py --step 3 \
  --models o1-preview o1-mini \
  --max-conversations 5 \
  --personality meme
```

## Output Format Examples

### Example 11: Website Deployment Ready

Generate HTML files optimized for web deployment:

```bash
python3 pipeline.py --step 4 \
  --source-dir backrooms_recreation/recreated_conversations/personality_absurdist
```

**Generated Files:**
- `index.html`: Navigation page
- `website_conversation_*.txt`: Individual conversation HTML files
- Terminal-style CSS formatting
- Chronological organization

### Example 12: Fine-Tuning Dataset Creation

Create datasets for model fine-tuning:

```bash
python3 pipeline.py --step 5 \
  --source-dir backrooms_recreation/recreated_conversations/personality_sarcastic
```

**Generated Datasets:**
- `conversations.jsonl`: Raw conversation turns
- `chat_format.jsonl`: OpenAI chat format
- `instruction_format.jsonl`: Instruction-following format

### Example 13: Custom Output Processing

Process specific personality variations:

```bash
# Create absurdist conversations
python3 pipeline.py --step 3 --personality absurdist --max-conversations 10

# Format only the absurdist conversations for website
python3 pipeline.py --step 4 \
  --source-dir backrooms_recreation/recreated_conversations/personality_absurdist

# Create fine-tuning dataset from absurdist conversations
python3 pipeline.py --step 5 \
  --source-dir backrooms_recreation/recreated_conversations/personality_absurdist
```

## Advanced Workflow Examples

### Example 14: Multi-Personality Batch Processing

Create multiple personality variations of the same conversations:

```bash
#!/bin/bash
# batch_personalities.sh

PERSONALITIES=("absurdist" "sarcastic" "eldritch" "cyberpunk" "philosophical")
MAX_CONVERSATIONS=15

for personality in "${PERSONALITIES[@]}"; do
    echo "Processing personality: $personality"
    python3 pipeline.py --step 3 \
      --personality $personality \
      --max-conversations $MAX_CONVERSATIONS \
      --models opus sonnet
    
    echo "Formatting for website: $personality"
    python3 pipeline.py --step 4 \
      --source-dir "backrooms_recreation/recreated_conversations/personality_$personality"
done
```

### Example 15: Chronological Recreation Pipeline

Recreate conversations in strict chronological order:

```bash
# Start from the earliest conversations (March 19, 2024)
python3 pipeline.py --step 3 \
  --start-date 2024-03-19 \
  --end-date 2024-03-31 \
  --personality retrofuturistic \
  --models opus gpt4o

# Continue with April 2024
python3 pipeline.py --step 3 \
  --start-date 2024-04-01 \
  --end-date 2024-04-30 \
  --personality retrofuturistic \
  --models opus gpt4o

# Process May 2024
python3 pipeline.py --step 3 \
  --start-date 2024-05-01 \
  --end-date 2024-05-31 \
  --personality retrofuturistic \
  --models opus gpt4o
```

### Example 16: Quality Control Workflow

Implement quality control with smaller batches:

```bash
# Test with small batch first
python3 pipeline.py --step 3 \
  --personality academic \
  --max-conversations 3 \
  --models sonnet sonnet

# Review output quality, then scale up
python3 pipeline.py --step 3 \
  --personality academic \
  --max-conversations 20 \
  --models sonnet sonnet
```

## Batch Processing Examples

### Example 17: Parallel Processing Script

Process multiple personality types simultaneously:

```bash
#!/bin/bash
# parallel_processing.sh

# Background process 1: Absurdist conversations
python3 pipeline.py --step 3 \
  --personality absurdist \
  --max-conversations 20 \
  --models opus opus &

# Background process 2: Sarcastic conversations
python3 pipeline.py --step 3 \
  --personality sarcastic \
  --max-conversations 20 \
  --models sonnet sonnet &

# Background process 3: Eldritch conversations
python3 pipeline.py --step 3 \
  --personality eldritch \
  --max-conversations 20 \
  --models gpt4o gpt4o &

# Wait for all processes to complete
wait

echo "All personality variations completed!"
```

### Example 18: Resource-Conscious Processing

Process large datasets with memory management:

```bash
# Process in small chunks to manage memory
for i in {1..10}; do
    start_date=$(date -d "2024-03-19 + $((($i-1)*7)) days" +%Y-%m-%d)
    end_date=$(date -d "2024-03-19 + $(($i*7)) days" +%Y-%m-%d)
    
    echo "Processing week $i: $start_date to $end_date"
    
    python3 pipeline.py --step 3 \
      --start-date $start_date \
      --end-date $end_date \
      --personality meme \
      --models opus sonnet
    
    # Brief pause to allow system recovery
    sleep 10
done
```

## Custom Integration Examples

### Example 19: Python API Usage

Use the system components programmatically:

```python
#!/usr/bin/env python3
# custom_recreation.py

import sys
sys.path.append('/home/ubuntu')

from pipeline import BackroomsPipeline
from personality_system import PersonalityManager

# Initialize pipeline
pipeline = BackroomsPipeline('/home/ubuntu/custom_recreation')

# Custom personality combinations
personality_manager = PersonalityManager()

# Create custom personality combination
custom_personalities = [
    ['absurdist', 'sarcastic'],
    ['eldritch', 'cyberpunk'],
    ['philosophical', 'meme']
]

# Process each combination
for combo in custom_personalities:
    combo_name = "_".join(combo)
    print(f"Processing combination: {combo_name}")
    
    # This would require extending the system to support
    # different personalities for different actors
    # (currently each conversation uses one personality for all actors)
```

### Example 20: Custom Output Format

Create a custom output format:

```python
#!/usr/bin/env python3
# custom_formatter.py

import json
from pathlib import Path
from conversation_recreator import ConversationParser

def create_custom_format(conversations_dir, output_file):
    """Create a custom JSON format for conversations"""
    parser = ConversationParser()
    custom_data = []
    
    for filepath in Path(conversations_dir).glob('*.txt'):
        structure = parser.parse_conversation_file(str(filepath))
        if structure:
            custom_entry = {
                'id': structure.timestamp,
                'scenario': structure.scenario,
                'date': structure.timestamp,
                'participants': structure.actors,
                'dialogue': [
                    {
                        'speaker': turn['actor'],
                        'message': turn['content'],
                        'turn_number': i
                    }
                    for i, turn in enumerate(structure.conversation_turns)
                ],
                'metadata': {
                    'models': structure.models,
                    'temperature': structure.temperature,
                    'system_prompts': structure.system_prompts
                }
            }
            custom_data.append(custom_entry)
    
    # Sort by timestamp
    custom_data.sort(key=lambda x: x['id'])
    
    # Save custom format
    with open(output_file, 'w') as f:
        json.dump(custom_data, f, indent=2)
    
    print(f"Custom format saved to: {output_file}")

# Usage
create_custom_format(
    'backrooms_recreation/recreated_conversations/personality_absurdist',
    'custom_format.json'
)
```

### Example 21: Integration with External Systems

Export conversations for external analysis:

```python
#!/usr/bin/env python3
# export_for_analysis.py

import csv
import json
from pathlib import Path
from conversation_recreator import ConversationParser
from datetime import datetime

def export_conversation_metrics(conversations_dir, output_csv):
    """Export conversation metrics for analysis"""
    parser = ConversationParser()
    metrics = []
    
    for filepath in Path(conversations_dir).glob('*.txt'):
        structure = parser.parse_conversation_file(str(filepath))
        if structure:
            # Calculate metrics
            total_turns = len(structure.conversation_turns)
            avg_turn_length = sum(len(turn['content']) for turn in structure.conversation_turns) / total_turns if total_turns > 0 else 0
            unique_actors = len(set(turn['actor'] for turn in structure.conversation_turns))
            
            metrics.append({
                'timestamp': structure.timestamp,
                'date': datetime.fromtimestamp(structure.timestamp).isoformat(),
                'scenario': structure.scenario,
                'total_turns': total_turns,
                'avg_turn_length': avg_turn_length,
                'unique_actors': unique_actors,
                'models': ','.join(structure.models),
                'temperature': ','.join(map(str, structure.temperature))
            })
    
    # Sort by timestamp
    metrics.sort(key=lambda x: x['timestamp'])
    
    # Write CSV
    with open(output_csv, 'w', newline='') as f:
        if metrics:
            writer = csv.DictWriter(f, fieldnames=metrics[0].keys())
            writer.writeheader()
            writer.writerows(metrics)
    
    print(f"Metrics exported to: {output_csv}")

# Usage
export_conversation_metrics(
    'backrooms_recreation/recreated_conversations',
    'conversation_metrics.csv'
)
```

## Testing and Validation Examples

### Example 22: System Validation

Validate the system before large-scale processing:

```bash
# Run system tests
python3 test_system.py

# Test with minimal data
python3 pipeline.py --step 3 \
  --max-conversations 2 \
  --personality absurdist \
  --models opus opus

# Validate output quality
ls -la backrooms_recreation/recreated_conversations/
```

### Example 23: Quality Assurance Workflow

Implement quality checks:

```bash
#!/bin/bash
# quality_check.sh

# Create test batch
python3 pipeline.py --step 3 \
  --personality sarcastic \
  --max-conversations 5 \
  --models sonnet sonnet

# Check output files exist
if [ -d "backrooms_recreation/recreated_conversations/personality_sarcastic" ]; then
    file_count=$(ls backrooms_recreation/recreated_conversations/personality_sarcastic/*.txt | wc -l)
    echo "Generated $file_count conversation files"
    
    if [ $file_count -eq 5 ]; then
        echo "✓ Expected number of files generated"
    else
        echo "✗ Unexpected number of files: expected 5, got $file_count"
    fi
else
    echo "✗ Output directory not found"
fi

# Check file sizes (should not be empty)
for file in backrooms_recreation/recreated_conversations/personality_sarcastic/*.txt; do
    if [ -s "$file" ]; then
        echo "✓ $file has content"
    else
        echo "✗ $file is empty"
    fi
done
```

These examples demonstrate the flexibility and power of the Infinite Backrooms Recreation System. Users can adapt these patterns to their specific needs, whether for research, content creation, or AI model development.

