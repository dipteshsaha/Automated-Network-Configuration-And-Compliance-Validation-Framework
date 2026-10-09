# Automated Network Configuration and Compliance Validation Framework

A Python-based read-only Cisco IOS network compliance auditing toolkit. Connects through SSH using Netmiko or audits offline configuration snapshots, checks YAML-defined security policies, and exports JSON/CSV reports.

## Features
- SSH-based `show running-config` collection (read-only)
- YAML-defined policy rules using regular expressions
- SSH v2, AAA, NTP, remote syslog, insecure HTTP checks
- Offline audit mode for demos and CI
- CSV and JSON compliance reports
- Unit tests and GitHub Actions
- Non-zero exit status on failed checks or connection errors

## Setup
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Offline demo (no router required)
```bash
python -m network_compliance.cli --config-dir examples --output reports
```

## Audit your lab devices
Edit `examples/inventory.yml` with your lab IPs. Use environment variables to avoid hardcoding credentials:
```bash
export NET_USERNAME='your-username'
export NET_PASSWORD='your-password'
python -m network_compliance.cli --inventory examples/inventory.yml --policies examples/policies.yml
```
If variables are omitted, the program prompts for credentials. Do not commit passwords, private configs, or sensitive reports.

## Tests
```bash
python -m unittest discover -s tests -v
```

## Scope and limitations
This starter is **read-only**: it does not deploy or change configurations. Checks are regex-based, not a complete parser, and may need adaptation to your IOS version and enterprise baselines. Only connect to devices you are authorized to administer. Review output before publishing because running configurations can contain secrets.

## Next enhancements
- Jinja2 configuration templates and explicit approval-based remediation
- Device-type-specific compliance baselines
- Secure configuration backup and diff reports
- More robust structured parsing using Cisco Genie/pyATS
- HTML dashboard and scheduled audits
