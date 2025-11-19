"""
CPU Emulator - Microcode-based Processor

Implements a clock-driven CPU that executes microcode instructions.
Based on Ben Eater's breadboard computer design.
"""

import time
from typing import Optional, List
from dataclasses import dataclass


@dataclass
class ControlSignals:
    """Control signals decoded from microcode ROM."""
    PC_OUT: bool = False
    PC_INC: bool = False
    MAR_IN: bool = False
    RAM_OUT: bool = False
    RAM_IN: bool = False
    IR_IN: bool = False
    IR_OUT: bool = False
    A_IN: bool = False
    A_OUT: bool = False
    B_IN: bool = False
    B_OUT: bool = False
    ALU_OUT: bool = False
    ALU_SUB: bool = False
    HALT: bool = False
    FLAGS_IN: bool = False
    
    @classmethod
    def from_word(cls, word: int):
        """Decode 16-bit control word into signals."""
        return cls(
            PC_OUT=(word & 0x0001) != 0,
            PC_INC=(word & 0x0002) != 0,
            MAR_IN=(word & 0x0004) != 0,
            RAM_OUT=(word & 0x0008) != 0,
            RAM_IN=(word & 0x0010) != 0,
            IR_IN=(word & 0x0020) != 0,
            IR_OUT=(word & 0x0040) != 0,
            A_IN=(word & 0x0080) != 0,
            A_OUT=(word & 0x0100) != 0,
            B_IN=(word & 0x0200) != 0,
            B_OUT=(word & 0x0400) != 0,
            ALU_OUT=(word & 0x0800) != 0,
            ALU_SUB=(word & 0x1000) != 0,
            HALT=(word & 0x2000) != 0,
            FLAGS_IN=(word & 0x4000) != 0,
        )
    
    def __repr__(self):
        active = []
        if self.PC_OUT: active.append("PC_OUT")
        if self.PC_INC: active.append("PC_INC")
        if self.MAR_IN: active.append("MAR_IN")
        if self.RAM_OUT: active.append("RAM_OUT")
        if self.RAM_IN: active.append("RAM_IN")
        if self.IR_IN: active.append("IR_IN")
        if self.IR_OUT: active.append("IR_OUT")
        if self.A_IN: active.append("A_IN")
        if self.A_OUT: active.append("A_OUT")
        if self.B_IN: active.append("B_IN")
        if self.B_OUT: active.append("B_OUT")
        if self.ALU_OUT: active.append("ALU_OUT")
        if self.ALU_SUB: active.append("ALU_SUB")
        if self.HALT: active.append("HALT")
        if self.FLAGS_IN: active.append("FLAGS_IN")
        return " | ".join(active) if active else "NOP"


class CPU:
    """
    Microcode-based 8-bit CPU.
    
    Registers:
    - PC: Program Counter (4 bits, 0-15)
    - MAR: Memory Address Register (4 bits)
    - IR: Instruction Register (8 bits)
    - A: General purpose register A (8 bits)
    - B: General purpose register B (8 bits)
    - FLAGS: Carry, Zero flags
    
    Memory:
    - 16 bytes RAM (4-bit addressing)
    
    Bus:
    - 8-bit data bus connecting all components
    """
    
    def __init__(self, microcode_rom: bytes, debug: bool = False):
        # Registers
        self.pc = 0          # Program counter (4 bits)
        self.mar = 0         # Memory address register (4 bits)
        self.ir = 0          # Instruction register (8 bits)
        self.a = 0           # Register A (8 bits)
        self.b = 0           # Register B (8 bits)
        self.flags = 0       # Flags: bit 0 = Carry, bit 1 = Zero
        
        # Memory
        self.ram = bytearray(16)  # 16 bytes RAM
        
        # Bus
        self.bus = 0         # 8-bit data bus
        
        # Control
        self.microcode = microcode_rom
        self.micro_step = 0  # Current micro-step in instruction
        self.fetching = True # True = fetch phase, False = execute phase
        self.fetch_step = 0  # Step within fetch cycle (0 or 1)
        self.halted = False
        self.debug = debug
        
        # Statistics
        self.instruction_count = 0
        self.cycle_count = 0
        
        if debug:
            print("CPU initialized:")
            print(f"  Microcode ROM: {len(microcode_rom)} bytes")
            print(f"  RAM: {len(self.ram)} bytes")
    
    def reset(self):
        """Reset CPU to initial state."""
        self.pc = 0
        self.mar = 0
        self.ir = 0
        self.a = 0
        self.b = 0
        self.flags = 0
        self.bus = 0
        self.micro_step = 0
        self.fetching = True
        self.fetch_step = 0
        self.halted = False
        self.instruction_count = 0
        self.cycle_count = 0
        
        if self.debug:
            print("CPU reset")
    
    def load_program(self, program: bytes, offset: int = 0):
        """Load program into RAM."""
        for i, byte in enumerate(program):
            if offset + i < len(self.ram):
                self.ram[offset + i] = byte
        
        if self.debug:
            print(f"Loaded {len(program)} bytes at address {offset}")
    
    def clock_cycle(self):
        """
        Execute one clock cycle (one microcode step).
        This is called on each clock edge.
        """
        if self.halted:
            return
        
        # Handle fetch cycle first (2 steps)
        if self.fetching:
            if self.debug:
                print(f"\nCycle {self.cycle_count}: FETCH T{self.fetch_step}")
            
            if self.fetch_step == 0:
                # T0: PC -> MAR
                self.bus = self.pc
                self.mar = self.bus & 0x0F
                if self.debug:
                    print(f"  PC -> MAR: {self.mar}")
            
            elif self.fetch_step == 1:
                # T1: RAM -> IR, PC++
                self.bus = self.ram[self.mar]
                self.ir = self.bus
                self.pc = (self.pc + 1) & 0x0F
                if self.debug:
                    print(f"  RAM[{self.mar}] -> IR: 0x{self.ir:02X}, PC++: {self.pc}")
                
                # Fetch complete, move to execute
                self.fetching = False
                self.fetch_step = 0
            
            self.fetch_step += 1
            self.cycle_count += 1
            
            if self.debug:
                self._print_state()
            return
        
        # Execute phase - use microcode ROM
        # Address = (instruction << 3) | micro_step
        rom_addr = (self.ir << 3) | self.micro_step
        
        # Read 16-bit control word (little-endian)
        if rom_addr * 2 + 1 < len(self.microcode):
            low_byte = self.microcode[rom_addr * 2]
            high_byte = self.microcode[rom_addr * 2 + 1]
            control_word = (high_byte << 8) | low_byte
        else:
            control_word = 0
        
        # Decode control signals
        signals = ControlSignals.from_word(control_word)
        
        if self.debug:
            print(f"\nCycle {self.cycle_count}: IR=0x{self.ir:02X} T{self.micro_step}")
            print(f"  Signals: {signals}")
        
        # Execute control signals
        self._execute_signals(signals)
        
        # Advance micro-step
        self.micro_step = (self.micro_step + 1) % 3
        
        # If back to T0, instruction complete - start new fetch
        if self.micro_step == 0:
            self.instruction_count += 1
            self.fetching = True
            self.fetch_step = 0
        
        self.cycle_count += 1
        
        if self.debug:
            self._print_state()
    
    def _execute_signals(self, signals: ControlSignals):
        """Execute the active control signals."""
        
        # HALT signal
        if signals.HALT:
            self.halted = True
            if self.debug:
                print("  ** HALTED **")
            return
        
        # Bus writes (multiple sources can write to bus)
        if signals.PC_OUT:
            self.bus = self.pc & 0xFF
            if self.debug:
                print(f"  PC -> Bus: 0x{self.bus:02X}")
        
        if signals.RAM_OUT:
            self.bus = self.ram[self.mar]
            if self.debug:
                print(f"  RAM[{self.mar}] -> Bus: 0x{self.bus:02X}")
        
        if signals.IR_OUT:
            self.bus = self.ir
            if self.debug:
                print(f"  IR -> Bus: 0x{self.bus:02X}")
        
        if signals.A_OUT:
            self.bus = self.a
            if self.debug:
                print(f"  A -> Bus: 0x{self.bus:02X}")
        
        if signals.B_OUT:
            self.bus = self.b
            if self.debug:
                print(f"  B -> Bus: 0x{self.bus:02X}")
        
        if signals.ALU_OUT:
            # ALU computes A +/- B
            if signals.ALU_SUB:
                result = (self.a - self.b) & 0xFF
                carry = self.a < self.b
            else:
                result = (self.a + self.b) & 0xFF
                carry = (self.a + self.b) > 0xFF
            
            self.bus = result
            
            # Update flags if FLAGS_IN is also active
            if signals.FLAGS_IN:
                self.flags = (carry << 0) | ((result == 0) << 1)
            
            if self.debug:
                op = "-" if signals.ALU_SUB else "+"
                print(f"  ALU: A {op} B = 0x{result:02X} (C={carry}, Z={result==0})")
        
        # Bus reads (registers/memory read from bus)
        if signals.MAR_IN:
            self.mar = self.bus & 0x0F  # 4-bit address
            if self.debug:
                print(f"  Bus -> MAR: {self.mar}")
        
        if signals.RAM_IN:
            self.ram[self.mar] = self.bus
            if self.debug:
                print(f"  Bus -> RAM[{self.mar}]: 0x{self.bus:02X}")
        
        if signals.IR_IN:
            self.ir = self.bus
            if self.debug:
                print(f"  Bus -> IR: 0x{self.ir:02X}")
        
        if signals.A_IN:
            self.a = self.bus
            if self.debug:
                print(f"  Bus -> A: 0x{self.a:02X}")
        
        if signals.B_IN:
            self.b = self.bus
            if self.debug:
                print(f"  Bus -> B: 0x{self.b:02X}")
        
        # PC increment
        if signals.PC_INC:
            self.pc = (self.pc + 1) & 0x0F  # 4-bit counter
            if self.debug:
                print(f"  PC++: {self.pc}")
    
    def _print_state(self):
        """Print current CPU state."""
        print(f"  State: PC={self.pc:X} MAR={self.mar:X} IR=0x{self.ir:02X} "
              f"A=0x{self.a:02X} B=0x{self.b:02X} Flags={self.flags:02b}")
    
    def run(self, max_cycles: int = 1000):
        """Run CPU until halted or max cycles reached."""
        print(f"Running CPU (max {max_cycles} cycles)...")
        print("=" * 60)
        
        while not self.halted and self.cycle_count < max_cycles:
            self.clock_cycle()
        
        print("=" * 60)
        if self.halted:
            print(f"CPU halted after {self.instruction_count} instructions, "
                  f"{self.cycle_count} cycles")
        else:
            print(f"Max cycles reached: {max_cycles}")
        
        return self.halted
    
    def get_output(self) -> int:
        """Get value from register A (output register)."""
        return self.a
    
    def dump_ram(self):
        """Print RAM contents."""
        print("\nRAM contents:")
        for i in range(0, len(self.ram), 8):
            hex_values = " ".join(f"{b:02X}" for b in self.ram[i:i+8])
            ascii_values = "".join(chr(b) if 32 <= b < 127 else "." for b in self.ram[i:i+8])
            print(f"  {i:X}: {hex_values}  {ascii_values}")


def load_microcode(filepath: str) -> bytes:
    """Load microcode ROM from binary file."""
    with open(filepath, 'rb') as f:
        return f.read()


if __name__ == '__main__':
    print("=" * 70)
    print("CPU Emulator Test")
    print("=" * 70)
    
    # Load microcode
    print("\n1. Loading microcode ROM...")
    microcode = load_microcode('microcode/microcode.bin')
    print(f"   Loaded {len(microcode)} bytes")
    
    # Create CPU
    cpu = CPU(microcode, debug=True)
    
    # Test program: Load immediate values and add
    print("\n2. Test Program: LDI_A 5, LDI_B 3, ADD, OUT_A, HALT")
    program = bytes([
        0x02, 0x05,  # LDI_A 5
        0x03, 0x03,  # LDI_B 3
        0x08,        # ADD
        0x0F,        # OUT_A
        0x01,        # HALT
    ])
    
    cpu.load_program(program)
    cpu.dump_ram()
    
    # Run program
    print("\n3. Running program...")
    cpu.run(max_cycles=50)
    
    print(f"\n4. Result in A: {cpu.get_output()} (expected: 8)")
    
    print("\n" + "=" * 70)
    print("CPU emulator ready!")
    print("=" * 70)
