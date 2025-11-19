"""
Test Suite for NAND Compute

Tests logic gates, arithmetic, and the complete system.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from logic import NAND, AND, OR, XOR, NOT, MUX, DMUX
from arithmetic import half_adder, full_adder, add_n, ALU


def test_nand():
    """Test NAND gate (the primitive)."""
    assert NAND(False, False) == True
    assert NAND(False, True) == True
    assert NAND(True, False) == True
    assert NAND(True, True) == False
    print("✓ NAND gate tests passed")


def test_basic_gates():
    """Test basic logic gates."""
    # NOT
    assert NOT(False) == True
    assert NOT(True) == False
    
    # AND
    assert AND(False, False) == False
    assert AND(False, True) == False
    assert AND(True, False) == False
    assert AND(True, True) == True
    
    # OR
    assert OR(False, False) == False
    assert OR(False, True) == True
    assert OR(True, False) == True
    assert OR(True, True) == True
    
    # XOR
    assert XOR(False, False) == False
    assert XOR(False, True) == True
    assert XOR(True, False) == True
    assert XOR(True, True) == False
    
    print("✓ Basic gate tests passed")


def test_composite_gates():
    """Test MUX and DMUX."""
    # MUX
    assert MUX(True, False, False) == True   # sel=0, output=a
    assert MUX(True, False, True) == False   # sel=1, output=b
    assert MUX(False, True, False) == False
    assert MUX(False, True, True) == True
    
    # DMUX
    assert DMUX(True, False) == (True, False)   # sel=0, a=input
    assert DMUX(True, True) == (False, True)    # sel=1, b=input
    assert DMUX(False, False) == (False, False)
    assert DMUX(False, True) == (False, False)
    
    print("✓ Composite gate tests passed")


def test_adders():
    """Test half and full adders."""
    # Half adder
    assert half_adder(False, False) == (False, False)
    assert half_adder(False, True) == (True, False)
    assert half_adder(True, False) == (True, False)
    assert half_adder(True, True) == (False, True)
    
    # Full adder
    assert full_adder(False, False, False) == (False, False)
    assert full_adder(True, True, False) == (False, True)
    assert full_adder(True, True, True) == (True, True)
    
    print("✓ Adder tests passed")


def test_alu():
    """Test ALU operations."""
    def int_to_bits(val, n=8):
        return [bool((val >> i) & 1) for i in range(n)]
    
    def bits_to_int(bits):
        return sum(b << i for i, b in enumerate(bits))
    
    alu = ALU(n_bits=8)
    
    # Test ADD
    result = alu.compute(int_to_bits(42), int_to_bits(18), 0)  # ADD
    assert bits_to_int(result) == 60
    
    # Test SUB
    result = alu.compute(int_to_bits(100), int_to_bits(25), 1)  # SUB
    assert bits_to_int(result) == 75
    
    # Test AND
    result = alu.compute(int_to_bits(0b11110000), int_to_bits(0b10101010), 2)
    assert bits_to_int(result) == 0b10100000
    
    # Test OR
    result = alu.compute(int_to_bits(0b11110000), int_to_bits(0b10101010), 3)
    assert bits_to_int(result) == 0b11111010
    
    print("✓ ALU tests passed")


def test_hello_world():
    """Test Hello World program execution."""
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'assembly'))
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'vm'))
    
    from assembler import Assembler
    from emulator import VM
    
    # Assemble hello world
    assembler = Assembler()
    asm_file = os.path.join(os.path.dirname(__file__), '..', 
                           'assembly', 'examples', 'hello_world.asm')
    
    machine_code = assembler.assemble_file(asm_file)
    
    # Run in VM
    vm = VM()
    vm.load_program(machine_code)
    vm.run()
    
    # Check output
    output = vm.get_output()
    assert output == "Hello, World!\n", f"Expected 'Hello, World!\\n', got {repr(output)}"
    
    print("✓ Hello World program test passed")


def test_counter():
    """Test counter program."""
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'assembly'))
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'vm'))
    
    from assembler import Assembler
    from emulator import VM
    
    assembler = Assembler()
    asm_file = os.path.join(os.path.dirname(__file__), '..', 
                           'assembly', 'examples', 'counter.asm')
    
    machine_code = assembler.assemble_file(asm_file)
    
    vm = VM()
    vm.load_program(machine_code)
    vm.run()
    
    output = vm.get_output()
    assert output == "0123456789\n", f"Expected '0123456789\\n', got {repr(output)}"
    
    print("✓ Counter program test passed")


if __name__ == "__main__":
    print("\nNAND Compute Test Suite")
    print("=" * 50)
    
    try:
        test_nand()
        test_basic_gates()
        test_composite_gates()
        test_adders()
        test_alu()
        test_hello_world()
        test_counter()
        
        print("=" * 50)
        print("✓ All tests passed!")
        print("\nYour computer built from NAND gates is working! 🎉")
        
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
