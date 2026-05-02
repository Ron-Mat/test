"""
Automotive Software Module - CI/CD Practice Project
This module simulates core automotive control functions that would be tested
in a real production environment. The functions demonstrate:
- Vehicle speed control
- Engine diagnostics
- Safety system checks
Key Responsibilities (from Job Description):
- Develop reliable, testable functions that can be verified by test scripts
- Implement helper functions for modular testing approach
- Follow software development lifecycle best practices
"""



class VehicleController:
    """
    Simulates core automotive control system.
    This class demonstrates the types of functions that would be tested
    in automotive quality assurance environments (HIL, SIL testing).
    """
    def __init__(self, vehicle_id: str, max_speed: int = 200):
        """Initialize vehicle controller with safety parameters."""
        self.vehicle_id = vehicle_id
        self.max_speed = max_speed
        self.current_speed = 0
        self.engine_on = False
        self.fault_codes = []

    def start_engine(self) -> bool:
        """
        Start the vehicle engine with safety checks.
        Returns:
            bool: True if engine started successfully, False otherwise
        """
        if len(self.fault_codes) > 0:
            return False  # Cannot start with active fault codes
        self.engine_on = True
        return self.engine_on

    def accelerate(self, speed_increase: int) -> int:
        """
        Safely increase vehicle speed with boundary checks.
        Args:
            speed_increase: Amount to increase speed
        Returns:
            int: Current speed after acceleration (clamped to max_speed)
        """
        if not self.engine_on:
            return 0
        self.current_speed = min(self.current_speed + speed_increase, self.max_speed)
        return self.current_speed

    def run_diagnostics(self) -> dict:
        """
        Run diagnostic checks on vehicle systems.
        This simulates the kind of diagnostic testing mentioned in the job description
        (Diagnostics, HWIO, Power Management checks).
        Returns:
            dict: Status of various system checks
        """
        diagnostics = {
            "engine_status": "OK" if self.engine_on else "OFF",
            "speed_valid": self.current_speed >= 0 and self.current_speed <= self.max_speed,
            "fault_count": len(self.fault_codes),
            "system_ready": len(self.fault_codes) == 0

        }
        return diagnostics

    def add_fault_code(self, fault_code: str) -> None:
        """Add a fault code for diagnostic purposes."""
        self.fault_codes.append(fault_code)

    def clear_faults(self) -> None:
        """Clear all active fault codes."""
        self.fault_codes.clear()



# Example usage demonstrating the module
if __name__ == "__main__":
    vehicle = VehicleController("VEHICLE_001")
    print(f"Created vehicle: {vehicle.vehicle_id}")
    print(f"Initial diagnostics: {vehicle.run_diagnostics()}")
