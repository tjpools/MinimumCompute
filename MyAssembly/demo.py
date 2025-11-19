#!/usr/bin/env python3
"""
Complete Computer System Demo

Demonstrates the full system:
- Clock (Dell computer, Arduino, or 555 timer emulation)
- CPU with microcode
- Memory and registers
- Program execution

This is a working computer built from NAND gates up!
"""

import sys
import time
from emulator.clock import Clock, ClockMode, create_clock
from emulator.cpu import CPU, load_microcode


def main():
    print("=" * 70)
    print("MYASSEMBLY COMPUTER - Ben Eater Style")
    print("=" * 70)
    
    # Load microcode ROM
    print("\n1. Loading microcode ROM...")
    microcode = load_microcode('microcode/microcode.bin')
    print(f"   ✓ Loaded {len(microcode)} bytes")
    
    # Create CPU
    print("\n2. Initializing CPU...")
    cpu = CPU(microcode, debug=False)
    print("   ✓ CPU ready with 16 bytes RAM")
    
    # Create clock
    print("\n3. Setting up clock...")
    clock_mode = 'emulator'  # Change to 'arduino' or '555' for hardware
    clock = create_clock(clock_mode, preset='slow')  # 1 Hz - visible
    print(f"   ✓ Clock configured: {clock}")
    
    # Load program
    print("\n4. Loading program...")
    program = bytes([
        0x02, 0x07,  # LDI_A 7
        0x03, 0x02,  # LDI_B 2
        0x08,        # ADD (A = A + B = 9)
        0x06, 0x0E,  # STA_A 0xE  (store result at address 14)
        0x0F,        # OUT_A (output result)
        0x01,        # HALT
    ])
    cpu.load_program(program)
    print(f"   ✓ Program loaded: {len(program)} bytes")
    print("\n   Program: 7 + 2 = ?")
    
    # Show initial RAM
    print("\n5. Initial RAM state:")
    cpu.dump_ram()
    
    # Connect clock to CPU
    print("\n6. Connecting clock to CPU...")
    clock.on_rising_edge(cpu.clock_cycle)
    clock.start()
    print("   ✓ Clock started")
    
    # Run until halted
    print("\n7. Running program...")
    print("-" * 70)
    
    cycle = 0
    start_time = time.time()
    
    while not cpu.halted and cycle < 100:
        # Tick the clock
        if clock.tick():
            # Clock edge occurred - CPU already executed via callback
            if cycle % 5 == 0:  # Print every 5 cycles to avoid spam
                print(f"   Cycle {cycle:3d}: PC={cpu.pc:X} IR=0x{cpu.ir:02X} "
                      f"A=0x{cpu.a:02X} B=0x{cpu.b:02X}")
            cycle += 1
        
        # Small sleep to allow clock timing
        time.sleep(0.01)
    
    elapsed = time.time() - start_time
    clock.stop()
    
    print("-" * 70)
    print(f"\n8. Execution complete!")
    print(f"   Time elapsed: {elapsed:.2f}s")
    print(f"   Instructions executed: {cpu.instruction_count}")
    print(f"   Clock cycles: {cpu.cycle_count}")
    print(f"   Average speed: {cpu.cycle_count/elapsed:.1f} Hz")
    
    # Show results
    print(f"\n9. Result:")
    print(f"   Register A: {cpu.a} (0x{cpu.a:02X})")
    print(f"   Expected: 9 (0x09)")
    print(f"   ✓ CORRECT!" if cpu.a == 9 else f"   ✗ ERROR")
    
    # Show final RAM
    print("\n10. Final RAM state:")
    cpu.dump_ram()
    print(f"\n   Value at address 0xE: {cpu.ram[0xE]} (should be 9)")
    
    print("\n" + "=" * 70)
    print("COMPUTER DEMONSTRATION COMPLETE")
    print("=" * 70)
    
    print("\n✓ This computer was built from:")
    print("  - NAND gates (fundamental logic)")
    print("  - Microcode ROM (instruction sequences)")
    print("  - Clock signal (Dell/Arduino/555 timer)")
    print("  - 8-bit ALU and registers")
    print("  - Von Neumann architecture")
    print("\n✓ Ready to deploy to:")
    print("  - Arduino hardware (with EEPROM)")
    print("  - Breadboard (with 74LS series ICs)")
    print("  - FPGA (for educational purposes)")
    
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(1)
