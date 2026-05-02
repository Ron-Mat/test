"""

Unit Tests for Automotive Software Module

This test suite demonstrates JUnit-style unit testing in Python using the unittest framework.

Key Responsibilities (from Job Description):

- "Strong knowledge of Unit test frameworks like JUnit, Unit, etc."

- "Lead in how test scripts are designed to verify key functional behaviors"

- "Identify structural challenges with scripts, helpers, benches, etc."

- "Establish Key Test Behaviors and drive efficiency in the work product"

Test Categories:

1. Unit Tests: Individual function testing

2. Integration Tests: Multiple components working together

3. Behavioral Tests: System behavior under various conditions

"""

import unittest
from helloworld import VehicleController
from test_helpers import TestHelper, analyze_test_results, setup_automotive_test_scenario


class TestVehicleEngineControl(unittest.TestCase):
    """
    Test Suite: Engine Control Functions
    Verifies that the engine start/stop functionality works correctly
    under various conditions (normal, fault states, etc.)
    """
    def setUp(self):

        """
        Test fixture: Setup before each test.
        This demonstrates proper test isolation and setup patterns,
        ensuring each test starts with a clean vehicle instance.
        """
        self.vehicle = VehicleController("TEST_ENGINE_001")
        self.helper = TestHelper()

    def test_engine_starts_successfully(self):
        """
        Test: Engine should start when no fault codes present.
        Expected Behavior: start_engine() returns True
        """
        result = self.vehicle.start_engine()
        self.assertTrue(result, "Engine should start successfully with no faults")

    def test_engine_cannot_start_with_faults(self):
        """
        Test: Engine should NOT start if fault codes are present.
        Safety Feature: Prevents vehicle operation when diagnostics fail.
        This demonstrates automotive safety principles.
        """
        self.vehicle.add_fault_code("P0100")  # Generic engine fault
        result = self.vehicle.start_engine()
        self.assertFalse(result, "Engine should not start with active fault codes")

    def test_fault_code_management(self):
        """
        Test: Fault codes can be added and cleared properly.
        This is critical for diagnostic functionality mentioned in job description:
        "Knowledge and familiarity with ... Diagnostics"
        """
        self.vehicle.add_fault_code("P0100")
        self.vehicle.add_fault_code("P0200")
        self.assertEqual(len(self.vehicle.fault_codes), 2)
        self.vehicle.clear_faults()
        self.assertEqual(len(self.vehicle.fault_codes), 0)


class TestVehicleSpeedControl(unittest.TestCase):
    """
    Test Suite: Speed Control Functions
    Verifies speed acceleration, limits, and safety boundaries.
    In real automotive testing (HIL/SIL), this would test:
    - Physical speed limits
    - Acceleration ramp rates
    - Emergency stop scenarios
    """
    def setUp(self):
        """Setup vehicle for speed testing."""
        self.vehicle = VehicleController("TEST_SPEED_001", max_speed=200)
        self.helper = TestHelper()

    def test_acceleration_when_engine_off(self):
        """
        Test: Vehicle should not accelerate when engine is off.
        Safety Feature: Prevents unintended movement.
        """
        speed = self.vehicle.accelerate(50)
        self.assertEqual(speed, 0, "Speed should remain 0 when engine is off")

    def test_acceleration_when_engine_on(self):
        """
        Test: Vehicle should accelerate when engine is running.
        """
        self.vehicle.start_engine()
        speed = self.vehicle.accelerate(50)
        self.assertEqual(speed, 50, "Speed should increase by 50 km/h")

    def test_speed_limit_enforcement(self):
        """
        Test: Vehicle should not exceed maximum speed.
        Requirement: Speed must stay within safe operating bounds
        (typical automotive requirement: max_speed = 200 km/h)
        """
        self.vehicle.start_engine()
        self.vehicle.accelerate(150)  # Current speed: 150
        self.vehicle.accelerate(100)  # Try to go 250, but max is 200
        self.assertLessEqual(
            self.vehicle.current_speed, 
            self.vehicle.max_speed, 
            "Speed should never exceed max_speed limit"
        )
        self.assertEqual(self.vehicle.current_speed, 200, "Speed should be clamped to max_speed (200)")

    def test_incremental_acceleration_sequence(self):
        """
        Test: Multiple acceleration steps in sequence.
        This simulates real driving scenarios with gradual speed changes.
        Demonstrates test behavior efficiency.
        """
        self.vehicle.start_engine()
        # Simulate gradual acceleration
        speeds = []
        for accel in [20, 30, 40, 50]:
            current_speed = self.vehicle.accelerate(accel)
            speeds.append(current_speed)
            # Speed should increase monotonically
            self.assertGreater(current_speed, speeds[-2] if len(speeds) > 1 else -1)
        self.helper.assert_true(
            len(speeds) == 4,
            "Should have recorded 4 speed changes"
        )


class TestVehicleDiagnostics(unittest.TestCase):
    """
    Test Suite: Diagnostic Functions
    Tests the diagnostic checking system that monitors vehicle health.
    Key Responsibility: "Knowledge and familiarity with ... Diagnostics"
    """
    def setUp(self):
        """Setup vehicle for diagnostic testing."""
        self.vehicle = VehicleController("TEST_DIAG_001")
        self.helper = TestHelper()
    def test_diagnostics_show_engine_off(self):
        """Test: Diagnostics correctly report engine status (off)."""
        diag = self.vehicle.run_diagnostics()
        self.assertEqual(diag["engine_status"], "OFF")
    def test_diagnostics_show_engine_on(self):
        """Test: Diagnostics correctly report engine status (on)."""
        self.vehicle.start_engine()
        diag = self.vehicle.run_diagnostics()
        self.assertEqual(diag["engine_status"], "OK")
    def test_diagnostics_speed_validity(self):
        """
        Test: Diagnostics verify that speed is within valid range.
        This is critical for safety verification in automotive systems.
        Speed must always be between 0 and max_speed.
        """
        self.vehicle.start_engine()
        self.vehicle.accelerate(100)
        result = self.vehicle.run_diagnostics()
        self.assertTrue(
            result["speed_valid"], 
            "Speed should be valid (within 0 to max_speed bounds)"
        )

    def test_diagnostics_with_faults(self):
        """
        Test: Diagnostics report fault codes correctly.
        Demonstrates diagnostic monitoring capability required in job:
        "Monitor QA testing needs/Objectives from various upstream and downstream stakeholders
        """
        self.vehicle.add_fault_code("P0100")
        self.assertEqual(self.vehicle.run_diagnostics()["fault_count"], 1)
        self.assertFalse(
            self.vehicle.run_diagnostics()["system_ready"], 
            "System should not be ready with active faults"
        )



class TestIntegrationScenarios(unittest.TestCase):
    """
    Integration Test Suite: Complete Vehicle Operation Scenarios
    Tests multiple components working together in realistic scenarios.
    Key Responsibility: "Develop Test Plans ... to ensure coverage in terms of
    integration of software and virtualized hardware components."
    """
    def setUp(self):
        """Setup for integration testing."""
        self.helper = TestHelper()
        self.helper.start_test_timer()
    def tearDown(self):
        """Report on test timing."""
        elapsed = self.helper.end_test_timer()
        print(f"\nTest execution time: {elapsed:.3f}s")

    def test_normal_driving_scenario(self):
        """
        Test: Normal driving scenario from startup to highway speed.
        Scenario:
        1. Start engine
        2. Accelerate gradually
        3. Verify system remains healthy
        4. Check diagnostics
        """
        scenario = setup_automotive_test_scenario("normal")
        vehicle = self.helper.setup_vehicle(
            scenario["vehicle_id"],
            scenario["max_speed"]
        )

        # Start engine
        self.assertTrue(vehicle.start_engine())

        # Gradual acceleration to highway speed
        for accel in scenario["test_acceleration"]:
            vehicle.accelerate(accel)

        # Verify diagnostics
        self.assertTrue(vehicle.run_diagnostics()["system_ready"])
        self.helper.assert_true(
            vehicle.run_diagnostics()["system_ready"],
            "System should be ready in normal scenario"
        )

    def test_fault_detection_scenario(self):
        """
        Test: System properly handles fault conditions.
        Scenario:
        1. Add fault code to system
        2. Attempt to start engine (should fail)
        3. Verify diagnostics show fault
        4. Clear fault and retry
        """
        scenario = setup_automotive_test_scenario("fault")
        vehicle = self.helper.setup_vehicle(scenario["vehicle_id"])
        # Inject fault
        vehicle.add_fault_code("P0100")
        # Try to start (should fail)
        start_result = vehicle.start_engine()
        self.assertFalse(start_result, "Engine should not start with fault")
        # Clear fault and retry
        vehicle.clear_faults()
        start_result = vehicle.start_engine()
        self.assertTrue(start_result, "Engine should start after fault cleared")



class TestPerformanceAndMetrics(unittest.TestCase):
    """
    Test Suite: Performance Metrics and Quality Measures
    Key Responsibility: "Define metrics for simulation quality and identify
    enablers for improved quality."
    These tests verify that the system meets performance requirements.
    """
    def setUp(self):
        """Setup for performance testing."""
        self.helper = TestHelper()

    def test_test_execution_efficiency(self):
        """
        Test: Verify test suite executes in reasonable time.
        Requirement: All unit tests should complete within acceptable timeframe
        for CI/CD pipeline integration.
        """
        self.helper.start_test_timer()
        # Create and run basic operations
        vehicle = self.helper.setup_vehicle("TEST_PERF_001")
        vehicle.start_engine()
        vehicle.accelerate(100)
        elapsed = self.helper.end_test_timer()
        # Performance metric: Tests should run quickly (< 1 second)
        self.assertLess(
            elapsed, 1.0,
            f"Test execution too slow: {elapsed:.3f}s (should be < 1.0s)"
        )

    def test_result_analysis(self):
        """
        Test: Verify test result analysis works correctly.
        Key Responsibility: "Develop, Lead, Enforce the use of solutions to
        increase operational efficiency, e.g. analyzing script results"
        """
        # Setup some test results
        self.helper.assert_equals(50, 50, "test_1")
        self.helper.assert_equals(75, 75, "test_2")
        summary = self.helper.get_test_summary()
        self.assertEqual(summary["total_tests"], 2)
        self.assertEqual(summary["passed"], 2)
        self.assertEqual(summary["failed"], 0)
        # Analyze results
        analysis = analyze_test_results(summary)
        self.assertIn("PASSED", analysis)



# Script to run tests with reporting
if __name__ == "__main__":
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestVehicleEngineControl))
    suite.addTests(loader.loadTestsFromTestCase(TestVehicleSpeedControl))
    suite.addTests(loader.loadTestsFromTestCase(TestVehicleDiagnostics))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegrationScenarios))
    suite.addTests(loader.loadTestsFromTestCase(TestPerformanceAndMetrics))
    # Run with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    # Exit with appropriate code for CI/CD
    exit(0 if result.wasSuccessful() else 1)
    