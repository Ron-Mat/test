import unittest
from helloworld import VehicleController
from subsystem import TransmissionController


class TestIntegrationVehicleTransmission(unittest.TestCase):
    """Integration tests verifying VehicleController with TransmissionController."""

    def setUp(self):
        self.vehicle = VehicleController("INT_TEST_001", max_speed=200)
        self.trans = TransmissionController()

    def test_throttle_no_transmission(self):
        """Throttle should not increase speed when transmission is not engaged."""
        speed = self.trans.apply_throttle(self.vehicle, 10)
        self.assertEqual(speed, 0)

    def test_throttle_with_transmission(self):
        """Throttle increases speed when transmission is engaged."""
        self.vehicle.start_engine()
        self.trans.engage(2)
        speed = self.trans.apply_throttle(self.vehicle, 10)
        self.assertGreater(speed, 0)
        self.assertLessEqual(self.vehicle.current_speed, self.vehicle.max_speed)

    def test_transmission_disengage(self):
        self.vehicle.start_engine()
        self.trans.engage(3)
        self.trans.apply_throttle(self.vehicle, 20)
        self.trans.disengage()
        prev_speed = self.vehicle.current_speed
        speed = self.trans.apply_throttle(self.vehicle, 10)
        self.assertEqual(speed, prev_speed)


if __name__ == "__main__":
    unittest.main()
