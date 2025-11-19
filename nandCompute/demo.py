#!/usr/bin/env python3
"""
NAND Compute Demo

Demonstrates the complete computer built from NAND gates.
"""

import sys
import os

# Add paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'logic'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'arithmetic'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'assembly'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'vm'))

from logic import NAND, AND, OR, NOT
from arithmetic import ALU
from assembler import Assembler
from emulator import VM


def demo_banner(title):
    """Print a nice banner."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")


def demo_nand_gates():
    """Demonstrate building gates from NAND."""
    demo_banner("Level 1: NAND Gates - The Foundation")
    
    print("NAND is the ONLY primitive gate. Everything is built from it!\n")
    
    print("NAND Truth Table:")
    print("  A | B | NAND(A,B)")
    print("  --|---|----------")
    for a in [0, 1]:
        for b in [0, 1]:
            result = NAND(bool(a), bool(b))
            print(f"  {a} | {b} |     {int(result)}")
    
    print("\nBuilding NOT from NAND:")
    print("  NOT(a) = NAND(a, a)")
    print(f"  NOT(0) = {int(NOT(False))}")
    print(f"  NOT(1) = {int(NOT(True))}")
    
    print("\nBuilding AND from NAND:")
    print("  AND(a, b) = NOT(NAND(a, b))")
    print(f"  AND(1, 1) = {int(AND(True, True))}")
    
    print("\nBuilding OR from NAND:")
    print("  OR(a, b) = NAND(NOT(a), NOT(b))")
    print(f"  OR(1, 0) = {int(OR(True, False))}")
    
    input("\nPress Enter to continue...")


def demo_alu():
    """Demonstrate the ALU."""
    demo_banner("Level 2: Arithmetic Logic Unit (ALU)")
    
    print("The ALU performs arithmetic and logical operations.\n")
    
    def int_to_bits(val, n=8):
        return [bool((val >> i) & 1) for i in range(n)]
    
    def bits_to_int(bits):
        return sum(b << i for i, b in enumerate(bits))
    
    alu = ALU(n_bits=8)
    
    # Addition
    a, b = 42, 18
    result = alu.compute(int_to_bits(a), int_to_bits(b), 0)
    print(f"Addition:   {a} + {b} = {bits_to_int(result)}")
    
    # Subtraction
    a, b = 100, 25
    result = alu.compute(int_to_bits(a), int_to_bits(b), 1)
    print(f"Subtraction: {a} - {b} = {bits_to_int(result)}")
    
    # Bitwise AND
    a, b = 0b11110000, 0b10101010
    result = alu.compute(int_to_bits(a), int_to_bits(b), 2)
    print(f"Bitwise AND: 0b{a:08b} & 0b{b:08b} = 0b{bits_to_int(result):08b}")
    
    # Bitwise OR
    result = alu.compute(int_to_bits(a), int_to_bits(b), 3)
    print(f"Bitwise OR:  0b{a:08b} | 0b{b:08b} = 0b{bits_to_int(result):08b}")
    
    print("\nThe ALU is the computational heart of the CPU!")
    
    input("\nPress Enter to continue...")


def demo_assembly():
    """Demonstrate assembly language."""
    demo_banner("Level 3: Assembly Language & Assembler")
    
    print("Our custom assembly language:\n")
    
    sample = """
    ; Simple program
    LOADI R0, 72    ; Load 'H' (ASCII 72)
    OUT R0          ; Output the character
    HALT            ; Stop execution
    """
    
    print(sample)
    
    print("This assembler translates to 16-bit machine code:")
    
    assembler = Assembler()
    machine_code = assembler.assemble(sample)
    
    for addr, instruction in enumerate(machine_code):
        if instruction != 0:
            print(f"  Address {addr}: 0x{instruction:04X} (0b{instruction:016b})")
    
    input("\nPress Enter to continue...")


def demo_hello_world():
    """Run the Hello World program."""
    demo_banner("Level 4: Hello, World! - The Complete System")
    
    print("Running Hello, World! program...\n")
    print("Source code: assembly/examples/hello_world.asm\n")
    
    # Show a snippet of the source
    with open('assembly/examples/hello_world.asm', 'r') as f:
        lines = f.readlines()[:15]
        for line in lines:
            print(f"  {line}", end='')
    
    print("\n  ...\n")
    
    print("Output:")
    print("-" * 40)
    
    # Assemble and run
    assembler = Assembler()
    machine_code = assembler.assemble_file('assembly/examples/hello_world.asm')
    
    vm = VM()
    vm.load_program(machine_code)
    vm.run()
    
    print("-" * 40)
    print(f"\nExecuted {vm.instruction_count} instructions")
    
    input("\nPress Enter to continue...")


def demo_all_programs():
    """Run all example programs."""
    demo_banner("Level 5: More Example Programs")
    
    programs = [
        ('counter.asm', 'Counter (0-9)'),
        ('fibonacci.asm', 'Fibonacci Sequence'),
        ('bitops.asm', 'Bitwise Operations'),
    ]
    
    for filename, description in programs:
        print(f"\n{description}:")
        print("-" * 40)
        
        filepath = os.path.join('assembly', 'examples', filename)
        
        assembler = Assembler()
        machine_code = assembler.assemble_file(filepath)
        
        vm = VM()
        vm.load_program(machine_code)
        vm.run()
        
        print("-" * 40)
        print(f"Instructions: {vm.instruction_count}\n")
    
    input("\nPress Enter to continue...")


def demo_architecture():
    """Show the complete architecture."""
    demo_banner("Complete Architecture: From NAND to Hello World")
    
    architecture = """
    Layer 1: Logic Gates (from NAND)
    ================================
    NAND → NOT, AND, OR, XOR
         → MUX, DMUX (selectors)
         → Multi-bit operations
    
    Layer 2: Arithmetic
    ===================
    Half Adder, Full Adder
         → N-bit Adder
         → Subtraction (two's complement)
         → ALU (8 operations)
    
    Layer 3: Memory (conceptual)
    =============================
    Flip-Flops → Registers → RAM
    Program Counter
    
    Layer 4: CPU Architecture
    =========================
    - 8 general-purpose registers (R0-R7)
    - 256 bytes RAM (0x00-0xFF)
    - 16-bit instruction set
    - 16 instructions (LOAD, ADD, JMP, OUT, etc.)
    
    Layer 5: Software
    =================
    Assembly Language
         → Assembler (ASM → Machine Code)
         → Virtual Machine/Emulator
         → Programs!
    
    All built from NAND gates! 🎉
    """
    
    print(architecture)
    
    input("\nPress Enter to finish...")


def main():
    """Run the complete demonstration."""
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    print("\n")
    print("╔════════════════════════════════════════════════════════════════════╗")
    print("║                                                                    ║")
    print("║                    NAND COMPUTE DEMONSTRATION                      ║")
    print("║                                                                    ║")
    print("║         Building a Computer from NAND Gates to Hello World        ║")
    print("║                                                                    ║")
    print("╚════════════════════════════════════════════════════════════════════╝")
    
    print("\nThis demonstration shows how we build a complete computer")
    print("starting with only NAND gates and ending with programs that")
    print("can output 'Hello, World!'")
    
    input("\nPress Enter to begin...")
    
    try:
        demo_nand_gates()
        demo_alu()
        demo_assembly()
        demo_hello_world()
        demo_all_programs()
        demo_architecture()
        
        demo_banner("Demonstration Complete!")
        
        print("You've seen how we build a complete computing system from")
        print("the ground up, starting with just NAND gates!")
        print("\nExplore the code:")
        print("  - logic/      : Logic gates from NAND")
        print("  - arithmetic/ : ALU and arithmetic circuits")
        print("  - assembly/   : Assembly language and assembler")
        print("  - vm/         : Virtual machine/emulator")
        print("  - tests/      : Test suite")
        print("\nTry writing your own assembly programs!")
        print("\n🎉 Happy computing! 🎉\n")
        
    except KeyboardInterrupt:
        print("\n\nDemo interrupted. Goodbye!")
    except Exception as e:
        print(f"\n\nError: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
