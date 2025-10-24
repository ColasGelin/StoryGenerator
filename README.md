# Story Generator

A simple Python script that generates a short story based on user-defined parameters.

## Requirements

- Python 3
- Virtual environment

## Setup

1. Clone the repository and navigate to the project directory.
2. Create a virtual environment:
   ```bash
   python3 -m venv .venv
   ```
3. Activate the virtual environment:
   ```bash
   source .venv/bin/activate
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Usage

Run the script with the following command:
```bash
python3 story_generator.py --theme <theme> --age-range <age_range> --tone <tone> --characters <character1> <character2> <character3> [--test-mode]
```

Example:
```bash
python3 story_generator.py --theme forest --age-range 3-5 --tone Educational --characters Alice Bob Charlie --test-mode
```

### Test Mode

Use the `--test-mode` flag to run the script in validation test mode. In this mode, the story will be generated without applying the validation requirements, allowing you to test the validation logic separately.