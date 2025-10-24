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

**Justification**: Less iterations and less tokens consumed by sending all requirements since the beginning


