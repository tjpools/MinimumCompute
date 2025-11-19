"""
Clock Module - Flexible Timing for Multiple Platforms

Provides clock signals for:
- Emulator mode: Software-controlled, variable speed
- Arduino mode: Hardware timer interrupts
- 555 Timer mode: External hardware clock input

The clock drives the microcode sequencer through each instruction cycle.
"""

import time
from enum import Enum
from typing import Callable, Optional


class ClockMode(Enum):
    """Clock source modes."""
    EMULATOR = "emulator"      # Software clock (Dell computer)
    ARDUINO = "arduino"        # Hardware timer simulation
    TIMER_555 = "555_timer"    # External hardware clock
    MANUAL = "manual"          # Single-step for debugging


class Clock:
    """
    Flexible clock system supporting multiple platforms.
    
    The clock generates rising/falling edge signals that drive
    the CPU's microcode sequencer.
    """
    
    def __init__(self, mode: ClockMode = ClockMode.EMULATOR, frequency_hz: float = 1.0):
        self.mode = mode
        self.frequency_hz = frequency_hz
        self.period = 1.0 / frequency_hz if frequency_hz > 0 else 1.0
        
        self.running = False
        self.cycle_count = 0
        self.state = False  # False = low, True = high
        
        # Callbacks for edge detection
        self.rising_edge_callbacks = []
        self.falling_edge_callbacks = []
        
        # Timing
        self.last_edge_time = 0
        
        print(f"Clock initialized: {mode.value} mode at {frequency_hz} Hz")
    
    def set_frequency(self, hz: float):
        """Change clock frequency (for emulator/manual modes)."""
        self.frequency_hz = hz
        self.period = 1.0 / hz if hz > 0 else 1.0
        print(f"Clock frequency set to {hz} Hz (period: {self.period*1000:.2f}ms)")
    
    def start(self):
        """Start the clock."""
        self.running = True
        self.last_edge_time = time.time()
        print(f"Clock started at {self.frequency_hz} Hz")
    
    def stop(self):
        """Stop the clock."""
        self.running = False
        print(f"Clock stopped after {self.cycle_count} cycles")
    
    def reset(self):
        """Reset clock to initial state."""
        self.cycle_count = 0
        self.state = False
        self.last_edge_time = 0
        print("Clock reset")
    
    def on_rising_edge(self, callback: Callable):
        """Register callback for rising edge (0→1 transition)."""
        self.rising_edge_callbacks.append(callback)
    
    def on_falling_edge(self, callback: Callable):
        """Register callback for falling edge (1→0 transition)."""
        self.falling_edge_callbacks.append(callback)
    
    def tick(self) -> bool:
        """
        Advance clock by one half-cycle.
        Returns True if edge occurred, False otherwise.
        """
        if not self.running:
            return False
        
        current_time = time.time()
        
        if self.mode == ClockMode.EMULATOR:
            # Software-controlled timing (Dell computer clock)
            elapsed = current_time - self.last_edge_time
            
            if elapsed >= self.period / 2:
                self._toggle_state()
                self.last_edge_time = current_time
                return True
        
        elif self.mode == ClockMode.ARDUINO:
            # Simulate hardware timer (would be interrupt-driven on real Arduino)
            elapsed = current_time - self.last_edge_time
            
            if elapsed >= self.period / 2:
                self._toggle_state()
                self.last_edge_time = current_time
                return True
        
        elif self.mode == ClockMode.TIMER_555:
            # External hardware clock - would read from GPIO pin
            # For emulation, we simulate the 555 timer behavior
            elapsed = current_time - self.last_edge_time
            
            if elapsed >= self.period / 2:
                self._toggle_state()
                self.last_edge_time = current_time
                return True
        
        elif self.mode == ClockMode.MANUAL:
            # Manual stepping - only advances when explicitly called
            pass
        
        return False
    
    def step(self):
        """
        Manual single-step (for debugging).
        Forces one complete clock cycle regardless of mode.
        """
        # Rising edge
        self.state = True
        self._fire_callbacks(self.rising_edge_callbacks)
        
        # Small delay to visualize
        if self.mode == ClockMode.MANUAL:
            time.sleep(0.1)
        
        # Falling edge
        self.state = False
        self._fire_callbacks(self.falling_edge_callbacks)
        
        self.cycle_count += 1
    
    def _toggle_state(self):
        """Toggle clock state and fire appropriate callbacks."""
        self.state = not self.state
        
        if self.state:  # Rising edge
            self._fire_callbacks(self.rising_edge_callbacks)
        else:  # Falling edge
            self._fire_callbacks(self.falling_edge_callbacks)
            self.cycle_count += 1
    
    def _fire_callbacks(self, callbacks):
        """Execute all registered callbacks."""
        for callback in callbacks:
            try:
                callback()
            except Exception as e:
                print(f"Clock callback error: {e}")
    
    def get_status(self) -> dict:
        """Get current clock status."""
        return {
            'mode': self.mode.value,
            'frequency_hz': self.frequency_hz,
            'period_ms': self.period * 1000,
            'running': self.running,
            'state': 'HIGH' if self.state else 'LOW',
            'cycles': self.cycle_count
        }
    
    def __repr__(self):
        status = self.get_status()
        return (f"Clock({status['mode']}, {status['frequency_hz']}Hz, "
                f"{'RUNNING' if status['running'] else 'STOPPED'}, "
                f"cycles={status['cycles']})")


class Timer555Emulator:
    """
    Emulates a 555 timer circuit for clock generation.
    
    Real 555 timer formula: f = 1.44 / ((R1 + 2*R2) * C)
    Where:
    - R1, R2 are resistors in ohms
    - C is capacitor in farads
    """
    
    def __init__(self, r1_ohms: float, r2_ohms: float, c_farads: float):
        self.r1 = r1_ohms
        self.r2 = r2_ohms
        self.c = c_farads
        
        # Calculate frequency
        self.frequency = 1.44 / ((r1_ohms + 2 * r2_ohms) * c_farads)
        
        print(f"555 Timer configured:")
        print(f"  R1 = {r1_ohms/1000:.1f}kΩ")
        print(f"  R2 = {r2_ohms/1000:.1f}kΩ")
        print(f"  C  = {c_farads*1e6:.1f}µF")
        print(f"  Frequency = {self.frequency:.2f} Hz")
    
    def get_frequency(self) -> float:
        """Get calculated frequency."""
        return self.frequency
    
    @staticmethod
    def design_for_frequency(target_hz: float, c_farads: float = 10e-6) -> tuple:
        """
        Design 555 timer circuit for target frequency.
        Returns (R1, R2) in ohms.
        
        For simplicity, we use R1 = R2 for 50% duty cycle.
        """
        # Using R1 = R2 = R: f = 1.44 / (3RC)
        # Solving for R: R = 1.44 / (3 * f * C)
        r = 1.44 / (3 * target_hz * c_farads)
        
        return (r, r)


# Preset clock configurations
CLOCK_PRESETS = {
    'slow': 1.0,           # 1 Hz - visible stepping
    'normal': 10.0,        # 10 Hz - comfortable speed
    'fast': 100.0,         # 100 Hz - quick execution
    'turbo': 1000.0,       # 1 kHz - maximum emulator speed
    'breadboard': 0.5,     # 0.5 Hz - very slow for hardware debug
    'arduino': 16e6,       # 16 MHz - Arduino crystal frequency
}


def create_clock(mode: str = 'emulator', preset: str = 'normal') -> Clock:
    """
    Convenient clock factory.
    
    Args:
        mode: 'emulator', 'arduino', '555', or 'manual'
        preset: 'slow', 'normal', 'fast', 'turbo', 'breadboard', 'arduino'
    
    Returns:
        Configured Clock instance
    """
    clock_mode = ClockMode[mode.upper()]
    frequency = CLOCK_PRESETS.get(preset, 1.0)
    
    return Clock(clock_mode, frequency)


if __name__ == '__main__':
    print("=" * 70)
    print("Clock Module Test")
    print("=" * 70)
    
    # Test emulator clock
    print("\n1. Emulator Clock (1 Hz):")
    clock = create_clock('emulator', 'slow')
    
    tick_count = [0]  # Use list for mutability in nested function
    def on_tick():
        tick_count[0] += 1
        print(f"  Tick {tick_count[0]}")
    
    clock.on_rising_edge(on_tick)
    clock.start()
    
    # Run for a few cycles
    start = time.time()
    while time.time() - start < 3.5:
        clock.tick()
        time.sleep(0.01)
    
    clock.stop()
    print(f"  Ran {clock.cycle_count} complete cycles")
    
    # Test manual stepping
    print("\n2. Manual Clock (single-step debugging):")
    manual_clock = create_clock('manual', 'slow')
    
    step_count = [0]  # Use list for mutability in nested function
    def on_step():
        step_count[0] += 1
        print(f"  Step {step_count[0]}")
    
    manual_clock.on_rising_edge(on_step)
    
    print("  Executing 3 manual steps...")
    for i in range(3):
        manual_clock.step()
    
    # Test 555 timer design
    print("\n3. 555 Timer Design:")
    print("\nDesigning for 1 Hz clock:")
    r1, r2 = Timer555Emulator.design_for_frequency(1.0, 10e-6)
    timer = Timer555Emulator(r1, r2, 10e-6)
    
    print("\nDesigning for breadboard (0.5 Hz):")
    r1, r2 = Timer555Emulator.design_for_frequency(0.5, 47e-6)
    timer = Timer555Emulator(r1, r2, 47e-6)
    
    print("\n" + "=" * 70)
    print("Clock module ready for CPU integration!")
    print("=" * 70)
