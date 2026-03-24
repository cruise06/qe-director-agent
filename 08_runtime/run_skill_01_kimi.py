import os
from pathlib import Path
from openai import OpenAI

ROOT = Path(__file__).resolve().parents[1]
PROMPT_FILE = ROOT / "07_prompt_shortcuts" / "skill_01_quality_gate_prompt.md"
INPUT_FILE = ROOT / "06_inputs" / "real_case_quality_gate_001.md"
OUTPUT_FILE = ROOT / "03_templates" / "real_case_quality_gate_001_result_kimi.md"

MODEL = os.getenv("KIMI_MODEL", "kimi-k2.5")

def main():
    api_key = os.getenv("KIMI_API_KEY")
    if not api_key:
        raise SystemExit("Missing KIMI_API_KEY")

    prompt_text = PROMPT_FILE.read_text(encoding="utf-8")
    input_text = INPUT_FILE.read_text(encoding="utf-8")

    full_prompt = f"""{prompt_text}

Use the following real case as the review input:

{input_text}
"""

    client = OpenAI(
        api_key=api_key,
        base_url="https://api.moonshot.ai/v1",
    )

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "user", "content": full_prompt}
        ],
        temperature=1,
    )

    result_text = response.choices[0].message.content.strip()
    OUTPUT_FILE.write_text(result_text + "\n", encoding="utf-8")

    print("DONE")
    print(f"model={MODEL}")
    print(f"output_file={OUTPUT_FILE}")

if __name__ == "__main__":
    main()
