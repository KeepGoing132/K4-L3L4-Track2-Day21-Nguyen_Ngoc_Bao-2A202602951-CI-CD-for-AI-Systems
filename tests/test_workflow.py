from pathlib import Path

import pytest
import yaml


WORKFLOW_PATH = Path(__file__).resolve().parents[1] / ".github/workflows/cicd.yml"


@pytest.mark.parametrize("value,passes", [
    ("0", False), ("0.6499", False), ("0.65", True), ("0.7156", True),
    ("1", True), ("1.01", False), ("nan", False), ("inf", False),
])
def test_actual_workflow_quality_gate(value, passes):
    workflow = yaml.safe_load(WORKFLOW_PATH.read_text(encoding="utf-8"))
    command = workflow["jobs"]["quality-gate"]["steps"][0]["run"]
    script = command.split("python - <<'PYEOF'\n", 1)[1].rsplit("PYEOF", 1)[0]
    script = script.replace("${{ needs.train.outputs.f1 }}", value)
    if passes:
        exec(compile(script, str(WORKFLOW_PATH), "exec"), {})
    else:
        with pytest.raises(SystemExit):
            exec(compile(script, str(WORKFLOW_PATH), "exec"), {})


def test_only_gated_release_publishes_model():
    jobs = yaml.safe_load(WORKFLOW_PATH.read_text(encoding="utf-8"))["jobs"]
    assert jobs["train"]["needs"] == "unit-test"
    assert jobs["quality-gate"]["needs"] == "train"
    assert jobs["release"]["needs"] == "quality-gate"
    publishers = [name for name, job in jobs.items() if any(
        "client.upload_file" in step.get("run", "") for step in job["steps"]
    )]
    assert publishers == ["release"]
    saved_candidates = [step["with"]["name"] for step in jobs["train"]["steps"]
                        if step.get("uses", "").startswith("actions/upload-artifact@")]
    assert "candidate-model" in saved_candidates
    downloads = [step["with"]["name"] for step in jobs["release"]["steps"]
                 if step.get("uses", "").startswith("actions/download-artifact@")]
    assert "candidate-model" in downloads
