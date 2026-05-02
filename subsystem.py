"""Simple subsystem to simulate integration (Transmission) interacting with VehicleController."""
from typing import Optional

class TransmissionController:
    """Simulates a transmission that must be engaged for acceleration to apply."""

    def __init__(self):
        self.gear: Optional[int] = None
        self.engaged: bool = False

    def engage(self, gear: int) -> None:
        if gear < 0 or gear > 6:
            raise ValueError("Invalid gear")
        self.gear = gear
        self.engaged = True

    def disengage(self) -> None:
        self.gear = None
        self.engaged = False

    def apply_throttle(self, vehicle, throttle: int) -> int:
        """
        Apply throttle to the given vehicle. If transmission not engaged,
        throttle has no effect.
        """
        if not self.engaged:
            return vehicle.current_speed
        # simple model: throttle increases speed by throttle * gear factor
        factor = max(1, self.gear)
        return vehicle.accelerate(throttle * factor)
