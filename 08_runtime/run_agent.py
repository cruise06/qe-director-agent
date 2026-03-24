import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SKILL_MAP = {
    "quality_gate": ROOT / "08_runtime" / "run_skill_01_kimi.py",
    "weekly_report": ROOT / "08_runtime" / "run_skill_06_kimi.py",
    "ai_radar": ROOT / "08_runtime" / "run_skill_07_kimi.py",
}

def main():
    parser = argparse.ArgumentParser(description="QE Director Agent unified runner")
    parser.add_argument("--skill", required=True, choices=SKILL_MAP.keys())
    args = parser.parse_args()

    script = SKILL_MAP[args.skill]
    result = subprocess.run([sys.executable, str(script)])
    raise SystemExit(result.returncode)

if __name__ == "__main__":
    main()
