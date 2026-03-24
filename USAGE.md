# QE Director Agent Usage

## Run a skill
```bash
./scripts/agent --skill quality_gate --input 06_inputs/your_case.md --output 03_templates/your_result.md
./scripts/agent --skill pilot_diagnosis --input 06_inputs/your_case.md --output 03_templates/your_result.md
./scripts/agent --skill incident_review --input 06_inputs/your_case.md --output 03_templates/your_result.md
./scripts/agent --skill weekly_report --input 06_inputs/your_case.md --output 03_templates/your_result.md
./scripts/agent --skill ai_radar --input 06_inputs/your_case.md --output 03_templates/your_result.md
```

## Supported skills
- quality_gate
- pilot_diagnosis
- incident_review
- weekly_report
- ai_radar

## Input and output
- Input files live in `06_inputs/`
- Output files live in `03_templates/`

## Example
```bash
./scripts/agent --skill quality_gate --input 06_inputs/real_case_quality_gate_001.md --output 03_templates/real_case_quality_gate_001_result_custom.md
```
