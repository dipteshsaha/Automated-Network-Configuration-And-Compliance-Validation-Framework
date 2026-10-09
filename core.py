import csv
import json
import re
from pathlib import Path

import yaml


def load_yaml(path):
    with open(path, encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def audit_config(config, policies):
    results = []
    for policy in policies:
        matched = bool(re.search(policy["pattern"], config, flags=re.MULTILINE | re.IGNORECASE))
        passed = matched if policy.get("expect", "present") == "present" else not matched
        results.append({"id": policy["id"], "description": policy["description"], "passed": passed})
    return results


def write_reports(results, output_dir):
    path = Path(output_dir)
    path.mkdir(parents=True, exist_ok=True)
    (path / "compliance.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
    with (path / "compliance.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["device", "id", "description", "passed"])
        writer.writeheader()
        for device, checks in results.items():
            for check in checks:
                writer.writerow({"device": device, **check})
