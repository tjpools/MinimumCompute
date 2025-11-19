"""
Arithmetic Logic Unit (ALU)

The ALU performs arithmetic and logical operations.
This is the computational heart of the CPU.
"""

import sys
sys.path.append('..')

from logic import AND_n, OR_n, XOR_n, NOT_n, MUX_n
from .adder import add_n, sub_n, zero_n, negative_n


class ALU:
    """
    8-bit Arithmetic Logic Unit
    
    Operations:
    - ADD: a + b
    - SUB: a - b
    - AND: a & b (bitwise)
    - OR:  a | b (bitwise)
    - XOR: a ^ b (bitwise)
    - NOT: ~a (bitwise)
    - PASS_A: output = a
    - PASS_B: output = b
    - ZERO: output = 0
    """
    
    def __init__(self, n_bits=8):
        self.n_bits = n_bits
        self.a = [False] * n_bits
        self.b = [False] * n_bits
        self.output = [False] * n_bits
        self.zero_flag = False
        self.negative_flag = False
    
    def compute(self, a: list[bool], b: list[bool], opcode: int) -> list[bool]:
        """
        Perform ALU operation.
        
        Args:
            a: First operand (n-bit)
            b: Second operand (n-bit)
            opcode: Operation code (0-8)
                0: ADD
                1: SUB
                2: AND
                3: OR
                4: XOR
                5: NOT a
                6: PASS_A
                7: PASS_B
                8: ZERO
        
        Returns:
            Result (n-bit) and sets flags
        """
        assert len(a) == self.n_bits and len(b) == self.n_bits
        
        self.a = a
        self.b = b
        
        # Perform operation based on opcode
        if opcode == 0:  # ADD
            result = add_n(a, b)[:self.n_bits]
        elif opcode == 1:  # SUB
            result = sub_n(a, b)
        elif opcode == 2:  # AND
            result = AND_n(a, b)
        elif opcode == 3:  # OR
            result = OR_n(a, b)
        elif opcode == 4:  # XOR
            result = XOR_n(a, b)
        elif opcode == 5:  # NOT
            result = NOT_n(a)
        elif opcode == 6:  # PASS_A
            result = a[:]
        elif opcode == 7:  # PASS_B
            result = b[:]
        elif opcode == 8:  # ZERO
            result = [False] * self.n_bits
        else:
            raise ValueError(f"Invalid opcode: {opcode}")
        
        self.output = result
        
        # Set flags
        self.zero_flag = zero_n(result)
        self.negative_flag = negative_n(result)
        
        return result
    
    def get_flags(self) -> dict:
        """Return current ALU flags."""
        return {
            'zero': self.zero_flag,
            'negative': self.negative_flag
        }
    
    def __repr__(self):
        """String representation of ALU state."""
        a_val = sum(b << i for i, b in enumerate(self.a))
        b_val = sum(b << i for i, b in enumerate(self.b))
        out_val = sum(b << i for i, b in enumerate(self.output))
        
        return (f"ALU({self.n_bits}-bit)\n"
                f"  A = {a_val:3d} (0x{a_val:02X})\n"
                f"  B = {b_val:3d} (0x{b_val:02X})\n"
                f"  Out = {out_val:3d} (0x{out_val:02X})\n"
                f"  Flags: Z={int(self.zero_flag)} N={int(self.negative_flag)}")


# Operation name mapping
ALU_OPS = {
    'ADD': 0,
    'SUB': 1,
    'AND': 2,
    'OR': 3,
    'XOR': 4,
    'NOT': 5,
    'PASS_A': 6,
    'PASS_B': 7,
    'ZERO': 8
}

ALU_OP_NAMES = {v: k for k, v in ALU_OPS.items()}


if __name__ == "__main__":
    print("ALU (Arithmetic Logic Unit)\n")
    
    def int_to_bits(value, n=8):
        """Convert integer to n-bit list."""
        return [bool((value >> i) & 1) for i in range(n)]
    
    def bits_to_int(bits):
        """Convert bit list to integer."""
        return sum(b << i for i, b in enumerate(bits))
    
    def signed_value(bits):
        """Interpret as two's complement signed integer."""
        val = bits_to_int(bits)
        if negative_n(bits):
            val = val - (1 << len(bits))
        return val
    
    # Create 8-bit ALU
    alu = ALU(n_bits=8)
    
    # Test cases
    test_cases = [
        (42, 18, 'ADD'),
        (100, 25, 'SUB'),
        (0b11110000, 0b10101010, 'AND'),
        (0b11110000, 0b10101010, 'OR'),
        (0b11110000, 0b10101010, 'XOR'),
        (0b10101010, 0, 'NOT'),
        (123, 0, 'PASS_A'),
        (0, 234, 'PASS_B'),
    ]
    
    print("Operation Tests:")
    print("=" * 60)
    
    for a_val, b_val, op_name in test_cases:
        a_bits = int_to_bits(a_val)
        b_bits = int_to_bits(b_val)
        
        result = alu.compute(a_bits, b_bits, ALU_OPS[op_name])
        result_val = bits_to_int(result)
        result_signed = signed_value(result)
        
        flags = alu.get_flags()
        
        print(f"\n{op_name}:")
        print(f"  A = {a_val:3d} (0x{a_val:02X}, 0b{a_val:08b})")
        print(f"  B = {b_val:3d} (0x{b_val:02X}, 0b{b_val:08b})")
        print(f"  Result = {result_val:3d} (0x{result_val:02X}, "
              f"0b{result_val:08b}) [signed: {result_signed}]")
        print(f"  Flags: Zero={flags['zero']}, Negative={flags['negative']}")
    
    print("\n" + "=" * 60)
    print("ALU Ready for Integration into CPU!")
