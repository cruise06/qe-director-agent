import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SKILL_MAP = {
    "quality_gate": ROOT / "08_runtime" / "run_skill_01_kimi.py",
    "pilot_diagnosis": ROOT / "08_runtime" / "run_skill_02_kimi.py",
    "incident_review": ROOT / "08_runtime" / "run_skill_05_kimi.py",
    "weekly_report": ROOT / "08_runtime" / "run_skill_06_kimi.py",
    "ai_radar": ROOT / "08_runtime" / "run_skill_07_kimi.py",
}

def main():
    parser = argparse.ArgumentParser(description="QE Director Agent unified runner")
    parser.add_argument("--skill", required=True, choices=SKILL_MAP.keys())
    parser.add_argument("--input", required=False, help="Path to input markdown file")
    parser.add_argument("--output", required=False, help="Path to output markdown file")
    args = parser.parse_args()

    script = SKILL_MAP[args.skill]
    cmd = [sys.executable, str(script)]

    if args.input:
        cmd.extend(["--input", args.input])
    if args.output:
        cmd.extend(["--output", args.output])

    result = subprocess.run(cmd)
    raise SystemExit(result.returncode)

if __name__ == "__main__":
    main()
