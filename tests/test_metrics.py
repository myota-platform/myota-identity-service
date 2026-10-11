from types import SimpleNamespace
import unittest
from unittest.mock import patch

from identity import IdentityHandler


class IdentityMetricsTests(unittest.TestCase):
    def test_metrics_are_aggregated_and_bounded(self):
        fake_store = SimpleNamespace(
            items={
                "private-account-id": {
                    "email": "private@example.invalid",
                    "participationType": "OPERATOR",
                    "callsigns": [{"callsign": "PRIVATE"}],
                },
                "another-private-id": {
                    "email": "another@example.invalid",
                    "participationType": "SWL",
                    "callsigns": [],
                },
            },
            data={
                "credentials": {
                    "private-account-id": {
                        "lockedUntil": "2999-01-01T00:00:00Z"
                    },
                    "another-private-id": {"lockedUntil": None},
                },
                "roles": {
                    "role-1": {"validTo": None},
                    "role-2": {"validTo": "2026-01-01T00:00:00Z"},
                },
                "securityEvents": {"event-1": {}, "event-2": {}},
            },
        )

        with patch.object(IdentityHandler, "store", fake_store):
            output = IdentityHandler.metrics_text()

        self.assertIn(
            'myota_identity_users{participation_type="OPERATOR"} 1', output
        )
        self.assertIn(
            'myota_identity_users{participation_type="SWL"} 1', output
        )
        self.assertIn("myota_identity_callsigns 1", output)
        self.assertIn("myota_identity_roles 1", output)
        self.assertIn("myota_identity_security_events 2", output)
        self.assertIn("myota_identity_locked_accounts 1", output)
        self.assertNotIn("private@example.invalid", output)
        self.assertNotIn("PRIVATE", output)
        self.assertNotIn("private-account-id", output)


if __name__ == "__main__":
    unittest.main()
