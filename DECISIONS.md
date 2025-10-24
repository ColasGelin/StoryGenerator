# StoryGenerator

## 1. Input phase

**Decision**: Simple command-line interface with argparse

**Justification**:
- **Fast MVP development**: Minimal and simple code
- **Evaluator-friendly**: Quick to test multiple scenarios without editing files
- **Auto-documentation**: `--help or -h` flag provides built-in usage guide
- **Scriptable**: Easy to automate testing with different parameters

**Parameters chosen**:
- `--theme`:(required) Core story concept 
- `--age-range`: (required) Guides AI generation style
- `--tone`: (required) Guides AI generation style
- `--characters`: Optional flexibility for unique and personalized experiences (accepts multiple names)

## 2. Generation phase

**Decision**: OpenAI agent, prompt it with the input parameters and the validation requirements directly

**Justification**: OpenAI is just the API key I had already, althought it's cheap and efficient. Less iterations and less tokens consumed by sending all requirements since the beginning

**Note**: Added a --test-mode flag to avoid including those validation requirements directly for validation testing purposes

## 3. Validation phase

**Decision**: An agent verifies the character count and that the 3 phases are respected and the program counts the number of words. Every time there is a missing requirements, the story is regenerated specifying the missing requirement in the prompt. The logging is made with the logging sdk.

**Justification**: The program checks for word count which is more efficient and accurate than making the agent do it, so the agent is focused on harder tasks (phases and character count).
This simple validation loop is easily scalable, making it possible to add other validation criteria.
The logging sdk is a common standard, allowing us to have time stamps, HTTP requests and each steps of the program.

## 4. PDF exportation

**Decisions & Justification**: Created a pdf with the story in it, specifying the agent to add a title to the story so that it looks better in the pdf. Applied wrapping and character encoding, I had a bug where the pdf generation was failing because of character encoding.

**Developement**: Wanted to make the story title as the title of the pdf but it requires json response from the first generation which would be the next step (with the image generation) if we would have further development of the MVP.



