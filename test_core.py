import unittest
from network_compliance.core import audit_config, load_yaml


class ComplianceTests(unittest.TestCase):
    def test_compliant_sample(self):
        policies = load_yaml("examples/policies.yml")["policies"]
        with open("examples/router.cfg", encoding="utf-8") as handle:
            results = audit_config(handle.read(), policies)
        self.assertTrue(all(item["passed"] for item in results))

    def test_detect_insecure_http(self):
        policies = load_yaml("examples/policies.yml")["policies"]
        results = audit_config("ip http server\n", policies)
        self.assertFalse(next(x for x in results if x["id"] == "NO_HTTP_SERVER")["passed"])


if __name__ == "__main__":
    unittest.main()
