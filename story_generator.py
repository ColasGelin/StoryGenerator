import argparse
import openai
import os
import dotenv

dotenv.load_dotenv()

def generate_story(theme, age_range, tone, characters):
    # Generating story with Theme, Age Range, Tone, and Character Names
    # Specify also the Length, Structure, and Character Requirements
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("OPENAI_API_KEY not set in environment")
    client = openai.OpenAI(api_key=api_key)
    
    prompt = f"""Create a short story with these specifications:
    - Theme: {theme}
    - Age Range: {age_range}
    - Tone: {tone}
    """
    
    if characters:
        prompt += f"\n- Characters names that you HAVE TO use: {', '.join(characters)}"

    prompt += """
    
    The story must follow these requirements:
    - Length: Between 450 and 550 words.
    - Structure: Clearly divided into 3 phases (introduction, conflict/development, resolution).
    - Characters: Feature at least 3 distinct characters.

    Write an engaging story that matches these requirements."""
    
    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[{"role": "user", "content": prompt}],
        max_completion_tokens=2000,
    )

    return response.choices[0].message.content

def main():
    parser = argparse.ArgumentParser(description='Generate story parameters')
    
    parser.add_argument('--theme', required=True, help='Story theme or topic')
    parser.add_argument('--age-range', required=True, choices=['3-5', '6-8', '9-12'], help='Target age range')
    parser.add_argument('--tone', required=True, help='Story tone (e.g., funny, adventurous, educational)')
    parser.add_argument('--characters', nargs='+', help='Character names (space-separated)')
    
    args = parser.parse_args()
    
    print("\nGenerating story...\n")
    story = generate_story(args.theme, args.age_range, args.tone, args.characters)
    print(story)
    
if __name__ == "__main__":
    main()