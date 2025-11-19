"""
Arithmetic Components - Adders and ALU

Building binary arithmetic from logic gates.
"""

import sys
sys.path.append('..')

from logic import AND, OR, XOR, NOT, NOT_n, AND_n, OR_n


def half_adder(a: bool, b: bool) -> tuple[bool, bool]:
    """
    Half Adder: Adds two single bits.
    
    Returns: (sum, carry)
    
    Truth Table:
    A | B | SUM | CARRY
    --|---|-----|------
    0 | 0 |  0  |  0
    0 | 1 |  1  |  0
    1 | 0 |  1  |  0
    1 | 1 |  0  |  1
    
    sum = XOR(a, b)
    carry = AND(a, b)
    """
    sum_bit = XOR(a, b)
    carry = AND(a, b)
    return (sum_bit, carry)


def full_adder(a: bool, b: bool, carry_in: bool) -> tuple[bool, bool]:
    """
    Full Adder: Adds three single bits (includes carry-in).
    
    Returns: (sum, carry_out)
    
    This is the building block for multi-bit addition.
    """
    # First half adder: add a and b
    sum1, carry1 = half_adder(a, b)
    
    # Second half adder: add sum1 and carry_in
    sum_out, carry2 = half_adder(sum1, carry_in)
    
    # Carry out if either half adder produced a carry
    carry_out = OR(carry1, carry2)
    
    return (sum_out, carry_out)


def add_n(a: list[bool], b: list[bool]) -> list[bool]:
    """
    N-bit ripple carry adder.
    
    Adds two n-bit numbers represented as lists of bools.
    LSB is at index 0.
    
    Returns: n+1 bits (result with potential overflow bit)
    """
    n = len(a)
    assert len(b) == n, "Both inputs must be same length"
    
    result = []
    carry = False
    
    for i in range(n):
        sum_bit, carry = full_adder(a[i], b[i], carry)
        result.append(sum_bit)
    
    # Add final carry bit
    result.append(carry)
    
    return result


def increment_n(a: list[bool]) -> list[bool]:
    """
    Increment an n-bit number by 1.
    
    This is useful for the program counter.
    """
    n = len(a)
    one = [True] + [False] * (n - 1)  # Binary 1
    return add_n(a, one)[:n]  # Discard overflow


def negate_n(a: list[bool]) -> list[bool]:
    """
    Two's complement negation of n-bit number.
    
    -a = NOT(a) + 1
    """
    n = len(a)
    not_a = NOT_n(a)
    one = [True] + [False] * (n - 1)
    return add_n(not_a, one)[:n]  # Discard overflow


def sub_n(a: list[bool], b: list[bool]) -> list[bool]:
    """
    N-bit subtraction: a - b
    
    Subtraction using two's complement: a - b = a + (-b)
    """
    n = len(a)
    assert len(b) == n, "Both inputs must be same length"
    
    neg_b = negate_n(b)
    return add_n(a, neg_b)[:n]  # Discard overflow


def zero_n(bits: list[bool]) -> bool:
    """
    Check if n-bit number is zero.
    
    Returns True if all bits are False.
    """
    result = bits[0]
    for bit in bits[1:]:
        result = OR(result, bit)
    return NOT(result)


def negative_n(bits: list[bool]) -> bool:
    """
    Check if n-bit two's complement number is negative.
    
    In two's complement, MSB = 1 means negative.
    """
    return bits[-1]  # MSB


if __name__ == "__main__":
    print("Arithmetic Components\n")
    
    # Test half adder
    print("Half Adder:")
    print("A | B | SUM | CARRY")
    print("--|---|-----|------")
    for a in [False, True]:
        for b in [False, True]:
            sum_bit, carry = half_adder(a, b)
            print(f"{int(a)} | {int(b)} |  {int(sum_bit)}  |  {int(carry)}")
    
    # Test full adder
    print("\nFull Adder (C_in = 0):")
    print("A | B | SUM | C_out")
    print("--|---|-----|------")
    for a in [False, True]:
        for b in [False, True]:
            sum_bit, carry = full_adder(a, b, False)
            print(f"{int(a)} | {int(b)} |  {int(sum_bit)}  |  {int(carry)}")
    
    # Test 8-bit addition
    print("\n8-bit Addition Examples:")
    
    def bits_to_int(bits):
        """Convert bit list to integer (unsigned)."""
        return sum(b << i for i, b in enumerate(bits))
    
    def int_to_bits(value, n=8):
        """Convert integer to n-bit list."""
        return [(value >> i) & 1 for i in range(n)]
    
    test_cases = [
        (5, 3),
        (15, 1),
        (127, 1),
        (100, 55),
    ]
    
    for a_val, b_val in test_cases:
        a_bits = int_to_bits(a_val)
        b_bits = int_to_bits(b_val)
        result = add_n(a_bits, b_bits)
        result_val = bits_to_int(result)
        
        print(f"{a_val} + {b_val} = {result_val} (overflow={int(result[-1])})")
    
    # Test subtraction
    print("\n8-bit Subtraction Examples:")
    for a_val, b_val in test_cases:
        a_bits = int_to_bits(a_val)
        b_bits = int_to_bits(b_val)
        result = sub_n(a_bits, b_bits)
        result_val = bits_to_int(result)
        
        # Handle two's complement for display
        if negative_n(result):
            result_val = result_val - 256
        
        print(f"{a_val} - {b_val} = {result_val}")
