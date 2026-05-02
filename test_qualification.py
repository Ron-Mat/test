import unittest
import time
from helloworld import VehicleController
from subsystem import TransmissionController
from test_helpers import TestHelper, analyze_test_results


class QualificationTests(unittest.TestCase):
    """Qualification-level tests (SWE6) - end-to-end scenarios and acceptance criteria."""

    def setUp(self):
        self.helper = TestHelper()

    def test_end_to_end_scenario(self):
        """Simulate a full scenario: start, accelerate, run diagnostics, and measure readiness."""
        vehicle = VehicleController("QUAL_TEST_001", max_speed=180)
        trans = TransmissionController()

        # Start and engage
        vehicle.start_engine()
        trans.engage(3)

        # Simulate a sustained drive
        for throttle in [10, 20, 30, 40]:
            trans.apply_throttle(vehicle, throttle)
            time.sleep(0.01)

        diag = vehicle.run_diagnostics()
        self.assertTrue(diag["system_ready"])  # acceptance: system ready

    def test_performance_threshold(self):
        """Qualification performance: scenario should complete within threshold."""
        self.helper.start_test_timer()
        vehicle = VehicleController("QUAL_PERF_001")
        vehicle.start_engine()
        trans = TransmissionController()
        trans.engage(2)
        for _ in range(5):
            trans.apply_throttle(vehicle, 20)
        elapsed = self.helper.end_test_timer()
        # qualification threshold: complete within 2 seconds in CI
        self.assertLess(elapsed, 2.0)


if __name__ == '__main__':
    unittest.main()
