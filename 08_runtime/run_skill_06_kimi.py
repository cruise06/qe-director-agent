import os
import argparse
from pathlib import Path
from openai import OpenAI

ROOT = Path(__file__).resolve().parents[1]
PROMPT_FILE = ROOT / "07_prompt_shortcuts" / "skill_06_management_reporting_prompt.md"
DEFAULT_INPUT_FILE = ROOT / "06_inputs" / "real_case_report_001.md"
DEFAULT_OUTPUT_FILE = ROOT / "03_templates" / "real_case_report_001_result_kimi.md"

MODEL = os.getenv("KIMI_MODEL", "kimi-k2.5")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default=str(DEFAULT_INPUT_FILE))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT_FILE))
    args = parser.parse_args()

    api_key = os.getenv("KIMI_API_KEY")
    if not api_key:
        raise SystemExit("Missing KIMI_API_KEY")

    input_file = Path(args.input)
    output_file = Path(args.output)

    prompt_text = PROMPT_FILE.read_text(encoding="utf-8")
    input_text = input_file.read_text(encoding="utf-8")

    full_prompt = f"""{prompt_text}

Use the following real case as the reporting input:

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
    output_file.write_text(result_text + "\n", encoding="utf-8")

    print("DONE")
    print(f"model={MODEL}")
    print(f"input_file={input_file}")
    print(f"output_file={output_file}")

if __name__ == "__main__":
    main()
