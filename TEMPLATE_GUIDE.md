# Guide to Adding New Conversation Templates

This guide explains how to create and add new conversation templates to the system, allowing you to define custom conversation structures, initial prompts, and contexts for the AI models.

## Understanding the Template Format

Conversation templates are `JSONL` (JSON Lines) files. Each line in the file is a JSON object, and each JSON object represents the configuration for one of the Language Models (LMs) participating in the conversation.

The order of the JSON objects in the `.jsonl` file corresponds to the order of the LMs specified with the `--lm` argument when running `backrooms.py` or `pipeline.py`.

### Key Fields in a Template JSON Object:

-   `system_prompt` (string, optional): This is the initial instruction or persona given to the AI. It sets the overall tone, role, and behavior for that specific LM. If not provided, the LM will have no explicit system prompt.
    -   **Important**: This is where personality modifiers are injected by the system.
-   `context` (array of objects, optional): This field contains the initial conversation history or context for the LM. Each object in the array should have a `role` (e.g., "user", "assistant") and `content` (the message text).
    -   This is crucial for setting up the initial state of the conversation, including any out-of-character (OOC) discussions or initial user prompts.
-   `cli` (boolean, optional): If set to `true`, this indicates that the LM is a Command Line Interface (CLI) and will interact with the `world-interface` service instead of a language model. This is specific to the `UniversalBackrooms` implementation.

### Example Template (`my_custom_template.jsonl`):

Let's say you want a conversation between two LMs: a "Philosopher AI" and a "Skeptical AI".

```json
{"system_prompt": "You are a profound philosopher AI, always questioning the nature of existence and reality. Your responses should be contemplative and deep.", "context": [{"role": "user", "content": "Let us ponder the essence of being."}]}
{"system_prompt": "You are a skeptical AI, always seeking empirical evidence and logical consistency. Your responses should challenge assumptions and demand proof.", "context": []}
```

-   **Line 1 (Philosopher AI)**: Sets a system prompt for the first LM and provides an initial user message in its context.
-   **Line 2 (Skeptical AI)**: Sets a system prompt for the second LM with no initial context.

If you run this with `--lm opus sonnet`, `opus` will be the Philosopher AI and `sonnet` will be the Skeptical AI.

## Steps to Add a New Template:

1.  **Create your `.jsonl` file**: Write your template content following the format described above. Ensure each line is a valid JSON object.
    -   You can use existing templates in `UniversalBackrooms/templates/` as a reference.
2.  **Name your file**: Choose a descriptive name for your template (e.g., `my_new_scenario.jsonl`). The name of the file (without the `.jsonl` extension) will be the template name you use with the `--template` argument.
3.  **Place the file**: Copy your newly created `.jsonl` file into the `UniversalBackrooms/templates/` directory.

    ```bash
    cp /path/to/your/my_new_scenario.jsonl /home/ubuntu/UniversalBackrooms/templates/
    ```

## Using Your New Template

Once your template file is in the `UniversalBackrooms/templates/` directory, the system will automatically detect it. You can then use it with the `pipeline.py` script (specifically in Step 3) or directly with `backrooms.py`.

### Example Usage with `pipeline.py`:

```bash
python3 pipeline.py --step 3 \
  --template my_new_scenario \
  --models opus sonnet \
  --max-conversations 5
```

This command will:
1.  Load your `my_new_scenario.jsonl` template.
2.  Use `opus` as the first LM (Philosopher AI) and `sonnet` as the second LM (Skeptical AI).
3.  Recreate 5 conversations based on your template.

### Example Usage with `backrooms.py` (for direct testing):

```bash
python3 UniversalBackrooms/backrooms.py \
  --lm opus sonnet \
  --template my_new_scenario \
  --max-turns 10
```

## Important Considerations:

-   **LM Count**: The number of JSON objects (lines) in your `.jsonl` template file **must match** the number of LMs you specify with the `--lm` argument. If you have two lines in your template, you must provide two models (e.g., `--lm opus sonnet`).
-   **Placeholder Formatting**: `backrooms.py` supports placeholders like `{lm1_actor}`, `{lm2_company}`, etc., in the `system_prompt` and `context` fields. These are automatically replaced by `backrooms.py` with the actual actor names and company names of the LMs involved. You can use these to make your templates more dynamic.
-   **Personality Swaps**: When you use a personality modifier with `pipeline.py` (e.g., `--personality absurdist`), the system will automatically append the personality's system prompt modifier to the `system_prompt` defined in your template. This allows your custom templates to be enhanced with different personalities.

By following these steps, you can easily extend the system with your own custom conversation templates, enabling a wide range of new conversational scenarios and experiments.

