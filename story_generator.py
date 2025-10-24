import argparse
import openai
import os
import json
import re
import dotenv
import logging
from fpdf import FPDF

dotenv.load_dotenv()

logging.basicConfig(filename='story_generator.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def generate_story(theme, age_range, tone, characters, missing_requirements=None, validation_test_mode=False):
    logging.info(f"Generating story with parameters: theme={theme}, age_range={age_range}, tone={tone}, characters={characters}")
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = f"""Create a engaging short story with these specifications for children:
    - Theme: {theme}
    - Age Range: {age_range}
    - Tone: {tone}
    Don't forget to put a Title at the top of the story"""

    if characters:
        prompt += f"\n- Characters names that you HAVE TO use: {', '.join(characters)}"
        
    if not validation_test_mode:
        print("Generating story with validation requirements in first generation, enable --test-mode to skip.")
        prompt += """
        The story MUST follow these requirements:
        - Length: Between 450 and 550 words.
        - Structure: Clearly divided into 3 phases (introduction, conflict/development, resolution).
        - Characters: Feature at least 3 distinct characters.
        Write an engaging story that matches these requirements."""
        
    if missing_requirements:
        prompt += "\nThe story MUST follow these requirements:\n- " + "\n- ".join(missing_requirements) + "\n(don't write the titles of the phases)"
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=2000,
    )
    
    return response.choices[0].message.content

def validate_length(story, min_words=450, max_words=550):
    words = re.findall(r"\S+", story)
    count = len(words)
    return count, (min_words <= count <= max_words)

def validate_with_agent(story):
    
    logging.info("Validating story with agent.")
    
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    system_msg = "You are a strict validator. Only output a single JSON object with the exact fields specified and valid JSON."
    user_msg = (
        "Validate the following story for two requirements:\n\n"
        "1) The story is clearly divided into three phases: introduction, conflict/development, resolution.\n"
        "2) The story features at least 3 distinct characters and list their names.\n\n"
        "Return only JSON with this exact structure:\n"
        '{"phases": {"introduction": boolean, "conflict": boolean, "resolution": boolean, "all_phases": boolean},'
        ' "characters": {"distinct_count": integer, "names": [string,...], "enough": boolean}} \n\n'
        "Do not add any extra fields or commentary. Here is the story:\n\n" + story
    )
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": system_msg}, {"role": "user", "content": user_msg}],
        max_tokens=500,
        temperature=0
    )
    
    content = response.choices[0].message.content.strip()
    try:
        data = json.loads(content)
        return data
    except Exception:
        return {}

def validate_story(story):
    logging.info("Starting story validation.")
    
    word_count, length_ok = validate_length(story)
    
    logging.info(f"Word count: {word_count} (required: 450-550) - {'Valid' if length_ok else 'Invalid'}")
    
    agent_result = validate_with_agent(story)
    phases = agent_result.get("phases", {}).get("all_phases", False)
    chars = agent_result.get("characters", {}).get("enough", False)

    if phases:
        logging.info("Story has all three phases (introduction, conflict, resolution).")
    else:
        logging.warning("Story is missing phases.")

    distinct_count = agent_result.get("characters", {}).get("distinct_count", 0)
    names = agent_result.get("characters", {}).get("names", [])

    if chars:
        logging.info(f"At least 3 characters found: {distinct_count} - names: {names}.")
    else:
        logging.warning("Not enough distinct characters found.")

    return length_ok, phases, chars

def save_story_to_pdf(story, filename='story.pdf'):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    pdf.set_left_margin(10)
    pdf.set_right_margin(10)

    # Replace unsupported characters with a placeholder
    story = story.encode('latin-1', 'replace').decode('latin-1')

    for line in story.split('\n'):
        pdf.multi_cell(0, 10, txt=line)
    pdf.output(filename)
    logging.info(f"Story saved to {filename}")

def main():
    parser = argparse.ArgumentParser(description='Generate story parameters')
    parser.add_argument('--theme', required=True, help='Story theme or topic')
    parser.add_argument('--age-range', required=True, choices=['3-5', '6-8', '9-12'], help='Target age range')
    parser.add_argument('--tone', required=True, help='Story tone (e.g., funny, adventurous, educational)')
    parser.add_argument('--characters', nargs='+', help='Character names (space-separated)')
    parser.add_argument('--test-mode', action='store_true', help='Enable validation test mode')
    args = parser.parse_args()
    
    logging.info(f"Received parameters: theme={args.theme}, age_range={args.age_range}, tone={args.tone}, characters={args.characters}")
    
    missing = []
    while True:
        story = generate_story(args.theme, args.age_range, args.tone, args.characters, missing, args.test_mode)
        logging.info("Generated story.")
        length_ok, all_phases, enough_chars = validate_story(story)

        if all_phases and enough_chars and length_ok:
            logging.info("Story validated successfully.")
            break
        else:
            if not all_phases:
                missing.append("Three phases: introduction, conflict/development, resolution.")
            if not enough_chars:
                missing.append("At least 3 distinct characters.")
            logging.warning(f"Story validation failed. Missing: {', '.join(missing)}")
            
    print("Final Story:\n", story)
    save_story_to_pdf(story)

if __name__ == "__main__":
    main()