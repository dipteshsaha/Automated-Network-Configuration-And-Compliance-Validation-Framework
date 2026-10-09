import argparse
import os
import sys
from pathlib import Path

from .core import audit_config, load_yaml, write_reports


def main():
    parser = argparse.ArgumentParser(description="Audit Cisco IOS configurations")
    parser.add_argument("--inventory", default="examples/inventory.yml")
    parser.add_argument("--policies", default="examples/policies.yml")
    parser.add_argument("--config-dir", help="Audit saved .cfg files without connecting to devices")
    parser.add_argument("--output", default="reports")
    args = parser.parse_args()

    policies = load_yaml(args.policies)["policies"]
    results = {}
    errors = []

    if args.config_dir:
        for path in sorted(Path(args.config_dir).glob("*.cfg")):
            results[path.stem] = audit_config(path.read_text(encoding="utf-8"), policies)
        if not results:
            parser.error("No .cfg files found in --config-dir")
    else:
        from getpass import getpass
        from netmiko import ConnectHandler

        devices = load_yaml(args.inventory)["devices"]
        username = os.environ.get("NET_USERNAME") or input("SSH username: ")
        password = os.environ.get("NET_PASSWORD") or getpass("SSH password: ")
        for device in devices:
            name = device["name"]
            try:
                with ConnectHandler(device_type=device.get("device_type", "cisco_ios"), host=device["host"], username=username, password=password) as conn:
                    config = conn.send_command("show running-config", read_timeout=90)
                results[name] = audit_config(config, policies)
            except Exception as exc:
                errors.append(f"{name}: {type(exc).__name__}: {exc}")

    write_reports(results, args.output)
    for name, checks in results.items():
        print(f"{name}: {sum(c['passed'] for c in checks)}/{len(checks)} passed")
    for error in errors:
        print(f"ERROR {error}", file=sys.stderr)
    if errors or any(not check["passed"] for checks in results.values() for check in checks):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
